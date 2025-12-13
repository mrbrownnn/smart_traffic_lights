import { NextResponse } from 'next/server';

const API_BASE_URL = 'https://congregative-pathognomonically-madelene.ngrok-free.dev';

export async function POST() {
  try {
    const response = await fetch(`${API_BASE_URL}/enable_ai`, {
      method: 'POST',
      headers: {
        'ngrok-skip-browser-warning': 'true',
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      throw new Error('Failed to enable AI mode');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Enable AI error:', error);
    return NextResponse.json(
      { error: 'Failed to enable AI mode' },
      { status: 500 }
    );
  }
}
