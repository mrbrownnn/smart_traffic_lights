import { NextResponse } from 'next/server';

const API_BASE_URL = 'https://congregative-pathognomonically-madelene.ngrok-free.dev';

export async function GET() {
  try {
    const response = await fetch(`${API_BASE_URL}/status`, {
      headers: {
        'ngrok-skip-browser-warning': 'true',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      throw new Error('Failed to fetch from backend');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('API proxy error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch traffic light status' },
      { status: 500 }
    );
  }
}
