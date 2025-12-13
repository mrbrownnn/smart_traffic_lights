import { NextResponse } from 'next/server';

const API_BASE_URL = 'https://congregative-pathognomonically-madelene.ngrok-free.dev';

export async function POST(
  request: Request,
  { params }: { params: { cluster: string; seconds: string } }
) {
  try {
    const { cluster, seconds } = params;
    
    const response = await fetch(
      `${API_BASE_URL}/manual_adjust/${cluster}/${seconds}`,
      {
        method: 'POST',
        headers: {
          'ngrok-skip-browser-warning': 'true',
          'Content-Type': 'application/json',
        },
        cache: 'no-store',
      }
    );

    if (!response.ok) {
      throw new Error('Failed to adjust traffic light');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Manual adjust error:', error);
    return NextResponse.json(
      { error: 'Failed to adjust traffic light' },
      { status: 500 }
    );
  }
}
