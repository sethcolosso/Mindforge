'use client';

import { useState, useEffect } from 'react';

interface DashboardStats {
  total_moods: number;
  total_workouts: number;
  total_badges: number;
  avg_mood_score: number;
}

export default function Home() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch(`${apiUrl}/api/dashboard/stats/`);
        if (!response.ok) {
          throw new Error('Failed to fetch stats');
        }
        const data = await response.json();
        setStats(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [apiUrl]);

  return (
    <main className="min-h-screen">
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-pink-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">M</span>
            </div>
            <h1 className="text-2xl font-bold text-gray-900">MindForge</h1>
          </div>
          <div className="flex gap-4">
            <a href="#" className="text-gray-600 hover:text-gray-900 transition">Login</a>
            <a href="#" className="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition">Sign Up</a>
          </div>
        </div>
      </nav>

      <section className="max-w-6xl mx-auto px-6 py-20">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">Your Personal Mental Health Companion</h2>
          <p className="text-xl text-gray-600 mb-8">Track your mood, complete wellness exercises, and connect with mental health professionals</p>
          <button className="bg-indigo-600 text-white px-8 py-3 rounded-lg hover:bg-indigo-700 transition font-semibold">
            Get Started
          </button>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-16">
          <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-lg transition">
            <div className="text-gray-600 text-sm font-semibold mb-2">Mood Entries</div>
            <div className="text-4xl font-bold text-gray-900">
              {loading ? '...' : stats?.total_moods || 0}
            </div>
          </div>
          <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-lg transition">
            <div className="text-gray-600 text-sm font-semibold mb-2">Workouts Completed</div>
            <div className="text-4xl font-bold text-gray-900">
              {loading ? '...' : stats?.total_workouts || 0}
            </div>
          </div>
          <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-lg transition">
            <div className="text-gray-600 text-sm font-semibold mb-2">Badges Earned</div>
            <div className="text-4xl font-bold text-gray-900">
              {loading ? '...' : stats?.total_badges || 0}
            </div>
          </div>
          <div className="bg-white rounded-lg p-6 border border-gray-200 hover:shadow-lg transition">
            <div className="text-gray-600 text-sm font-semibold mb-2">Average Mood</div>
            <div className="text-4xl font-bold text-gray-900">
              {loading ? '...' : (stats?.avg_mood_score?.toFixed(1) || '0')}
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            Note: Could not connect to API. Make sure the Django server is running.
          </div>
        )}

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-lg p-8 border border-gray-200 hover:shadow-lg transition">
            <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Track Your Mood</h3>
            <p className="text-gray-600">Log your daily moods and gain insights into your emotional patterns</p>
          </div>
          <div className="bg-white rounded-lg p-8 border border-gray-200 hover:shadow-lg transition">
            <div className="w-12 h-12 bg-pink-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🧘</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Wellness Exercises</h3>
            <p className="text-gray-600">Practice guided exercises to improve focus, reduce anxiety, and find calm</p>
          </div>
          <div className="bg-white rounded-lg p-8 border border-gray-200 hover:shadow-lg transition">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">👥</span>
            </div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">Professional Support</h3>
            <p className="text-gray-600">Connect with qualified mental health professionals when you need support</p>
          </div>
        </div>
      </section>
    </main>
  );
}
