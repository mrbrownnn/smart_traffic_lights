import { NextResponse } from 'next/server';

const API_BASE_URL = 'https://congregative-pathognomonically-madelene.ngrok-free.dev';

export async function GET() {
  try {
    const response = await fetch(`${API_BASE_URL}/camera`, {
      headers: {
        'ngrok-skip-browser-warning': 'true',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch camera stream');
    }

    // Forward the stream response with proper headers
    return new NextResponse(response.body, {
      headers: {
        'Content-Type': response.headers.get('Content-Type') || 'multipart/x-mixed-replace; boundary=frame',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
      },
    });
  } catch (error) {
    console.error('Camera stream error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch camera stream' },
      { status: 500 }
    );
  }
}
