import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'MindForge - Mental Health & Wellness',
  description: 'Your personal mental health companion with AI-powered insights and exercises',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
          {children}
        </div>
      </body>
    </html>
  );
}
