# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
Ultralytics neural network modules.

This module provides access to various neural network components used in Ultralytics models, including convolution
blocks, attention mechanisms, transformer components, and detection/segmentation heads.

Examples:
    Visualize a module with Netron
    >>> from ultralytics.nn.modules import Conv
    >>> import torch
    >>> import subprocess
    >>> x = torch.ones(1, 128, 40, 40)
    >>> m = Conv(128, 128)
    >>> f = f"{m._get_name()}.onnx"
    >>> torch.onnx.export(m, x, f)
    >>> subprocess.run(f"onnxslim {f} {f} && open {f}", shell=True, check=True)  # pip install onnxslim
"""

from .block import (
    
    
    
    CIB,
    DFL,
    PSA,
    SPP,
    SPPF,
    Attention,
    BNContrastiveHead,
    ContrastiveHead,
    MaxSigmoidAttnBlock,
    Proto,
)
from .conv import (
    CBAM,
    ChannelAttention,
    Concat,
    Conv,
    DWConv,
    LightConv,
    RepConv,
    SpatialAttention,
)
from .head import (
    
    
    Detect,
    YOLOE
    
)
from .transformer import (
    
    MLP,
    DeformableTransformerDecoder,
    DeformableTransformerDecoderLayer,
    LayerNorm2d,
    MLPBlock,
    MSDeformAttn,
    TransformerBlock,
    TransformerEncoderLayer,
    TransformerLayer,
)

__all__ = (
    "Conv",
    "LightConv",
    "RepConv",
    "DWConv",
    "DWConvTranspose2d",
    "ConvTranspose",
    "Focus",
    "GhostConv",
    "ChannelAttention",
    "SpatialAttention",
    "CBAM",
    "Concat",
    "TransformerLayer",
    "TransformerBlock",
    "MLPBlock",
    "LayerNorm2d",
    "DFL",
    "HGBlock",
    "HGStem",
    "SPP",
    "SPPF",
    "C1",
    "C2",
    "C3",
    "C2f",
    "C3k2",
    "SCDown",
    "Proto",
    "Detect",
    "TransformerEncoderLayer",
    "DeformableTransformerDecoder",
    "DeformableTransformerDecoderLayer",
    "MSDeformAttn",
    "MLP",
    "MaxSigmoidAttnBlock",
    "ContrastiveHead",
    "BNContrastiveHead",
    "CIB",
    "Attention",
    "PSA",

)
