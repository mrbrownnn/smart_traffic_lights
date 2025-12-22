import { NextResponse } from 'next/server';

const API_BASE_URL = 'https://congregative-pathognomonically-madelene.ngrok-free.dev';

export async function POST() {
  try {
    const response = await fetch(`${API_BASE_URL}/manual_reset`, {
      method: 'POST',
      headers: {
        'ngrok-skip-browser-warning': 'true',
        'Content-Type': 'application/json',
      },
      cache: 'no-store',
    });

    if (!response.ok) {
      throw new Error('Failed to reset traffic lights');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Manual reset error:', error);
    return NextResponse.json(
      { error: 'Failed to reset traffic lights' },
      { status: 500 }
    );
  }
}
