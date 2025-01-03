import { Providers } from '@/providers';
import { Navbar } from '@/components/layout/Navbar';
import { Inter } from 'next/font/google';
import { Toaster } from 'react-hot-toast';
import type { Metadata } from 'next';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'BoodschappenVergelijker',
  description: 'Vergelijk prijzen en vind de beste deals bij Nederlandse supermarkten',
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#ffffff',
  manifest: '/manifest.json',
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png'
  }
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="nl" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
            <Navbar />
            <main className="flex-grow container mx-auto px-4 py-8">
              {children}
            </main>
            <footer className="py-6 text-center text-sm text-gray-500 dark:text-gray-400">
              © {new Date().getFullYear()} BoodschappenVergelijker
            </footer>
          </div>
          <Toaster position="top-right" />
        </Providers>
      </body>
    </html>
  );
}