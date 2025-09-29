import torch
import torch.nn as nn
from ultralytics.nn.modules import Conv  # reuse activation từ Ultralytics
# identify 2 new module: DWConv and GhostModule
class DWConv(nn.Module):
    """Depthwise Convolution replace Conv standard"""
    def __init__(self, c1, c2, k=3, s=1, act=True):
        super().__init__()
        self.dwconv = nn.Conv2d(c1, c1, kernel_size=k, stride=s, padding=k//2, groups=c1, bias=False)
        self.pointwise = nn.Conv2d(c1, c2, kernel_size=1, stride=1, padding=0, bias=False)  # Pointwise Conv để đổi số channel
        self.bn = nn.BatchNorm2d(c2)
        self.act = nn.SiLU() if act else nn.Identity()

    def forward(self, x):
        x = self.dwconv(x)
        x = self.pointwise(x)
        x = self.bn(x)
        x = self.act(x)
        return x

class GhostModule(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=1, ratio=2, dw_size=3, stride=1, act=True):
        super().__init__()
        self.out_channels = out_channels
        init_channels = out_channels // ratio
        new_channels = out_channels - init_channels

        self.primary_conv = nn.Sequential(
            nn.Conv2d(in_channels, init_channels, kernel_size, stride, kernel_size//2, bias=False),
            nn.BatchNorm2d(init_channels),
            nn.SiLU() if act else nn.Identity()
        )

        self.cheap_operation = nn.Sequential(
            nn.Conv2d(init_channels, new_channels, dw_size, 1, dw_size//2, groups=init_channels, bias=False),
            nn.BatchNorm2d(new_channels),
            nn.SiLU() if act else nn.Identity()
        )

    def forward(self, x):
        x1 = self.primary_conv(x)
        x2 = self.cheap_operation(x1)
        out = torch.cat([x1, x2], dim=1)
        return out[:, :self.out_channels, :, :]

class GhostC2f(nn.Module):
    """Block replace C2f, use GhostModule instead Bottleneck."""
    def __init__(self, c1, c2, n=1, shortcut=True, g=1, e=0.5):
        super().__init__()
        self.c = int(c2 * e)  # Hidden channels
        self.cv1 = GhostModule(c1, 2 * self.c, 1)  # Thay Conv bằng GhostModule
        self.cv2 = GhostModule((2 + n) * self.c, c2, 1)  # Thay Conv cuối
        self.m = nn.ModuleList(GhostModule(self.c, self.c) for _ in range(n))  # Thay Bottleneck bằng GhostModule
        self.shortcut = shortcut

    def forward(self, x):
        y = list(self.cv1(x).split((self.c, self.c), 1))
        y.extend(m(y[-1]) for m in self.m)
        out = self.cv2(torch.cat(y, 1))
        if self.shortcut:
            out = out + x
        return out