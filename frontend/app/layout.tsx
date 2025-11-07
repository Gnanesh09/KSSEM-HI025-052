// app/layout.tsx
import type { Metadata } from 'next'
import './styles/globals.css'
import { LanguageProvider } from '@/context/LanguageContext'
import Navbar from '@/components/Navbar'

export const metadata: Metadata = {
  title: 'GreenChain - Blockchain Crop Insurance',
  description: 'Instant verification. Zero fraud. Fair payouts.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <LanguageProvider>
          <Navbar />
          <main className="min-h-screen bg-light">
            {children}
          </main>
        </LanguageProvider>
      </body>
    </html>
  )
}
