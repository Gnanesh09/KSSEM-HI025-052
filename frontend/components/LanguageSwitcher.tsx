// components/LanguageSwitcher.tsx
'use client'

import { useState } from 'react'
import { useLanguage } from '@/context/LanguageContext'

interface Language {
  code: string
  name: string
  flag: string
}

export default function LanguageSwitcher() {
  const { language, changeLanguage } = useLanguage()
  const [isOpen, setIsOpen] = useState<boolean>(false)

  const languages: Language[] = [
    { code: 'en', name: 'English', flag: '🇬🇧' },
    { code: 'hi', name: 'हिन्दी', flag: '🇮🇳' },
    { code: 'kn', name: 'ಕನ್ನಡ', flag: '🌾' },
    { code: 'te', name: 'తెలుగు', flag: '🏞️' },
  ]

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="text-white bg-white bg-opacity-20 px-4 py-2 rounded flex items-center gap-2"
      >
        {languages.find((l) => l.code === language)?.flag}
        <span className="hidden sm:inline text-sm">{language.toUpperCase()}</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 bg-white shadow-lg rounded-lg overflow-hidden w-48">
          {languages.map((lang) => (
            <button
              key={lang.code}
              onClick={() => {
                changeLanguage(lang.code)
                setIsOpen(false)
              }}
              className={`w-full px-4 py-2 text-left hover:bg-primary hover:text-white transition flex items-center gap-2 ${
                language === lang.code ? 'bg-primary text-white' : ''
              }`}
            >
              <span className="text-xl">{lang.flag}</span>
              <span>{lang.name}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
