// components/Navbar.tsx
'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useLanguage } from '@/context/LanguageContext'
import LanguageSwitcher from './LanguageSwitcher'
import { FaBars, FaTimes } from 'react-icons/fa'

interface NavItem {
  label: string
  path: string
}

export default function Navbar() {
  const { t } = useLanguage()
  const [isOpen, setIsOpen] = useState<boolean>(false)

  const navItems: NavItem[] = [
    { label: t('nav.home'), path: '/' },
    { label: t('nav.dashboard'), path: '/dashboard' },
    { label: t('nav.fileClaim'), path: '/claim' },
    { label: t('nav.satellite'), path: '/satellite' },
    { label: t('nav.prices'), path: '/prices' },
    { label: t('nav.blockchain'), path: '/blockchain' },
  ]

  return (
    <nav className="bg-gradient-to-r from-primary to-secondary shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link href="/" className="flex items-center gap-2">
            <span className="text-3xl">🌾</span>
            <span className="text-white font-bold text-xl">GreenChain</span>
          </Link>

          <div className="hidden md:flex items-center gap-8">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className="text-white hover:bg-white hover:bg-opacity-20 px-3 py-2 rounded transition"
              >
                {item.label}
              </Link>
            ))}
          </div>

          <LanguageSwitcher />

          <button
            className="md:hidden text-white"
            onClick={() => setIsOpen(!isOpen)}
          >
            {isOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>

        {isOpen && (
          <div className="md:hidden bg-primary bg-opacity-90 pb-4">
            {navItems.map((item) => (
              <Link
                key={item.path}
                href={item.path}
                className="block text-white px-4 py-2 hover:bg-white hover:bg-opacity-10"
                onClick={() => setIsOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}
