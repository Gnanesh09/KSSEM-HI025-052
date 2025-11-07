// app/page.tsx
'use client'

import { useLanguage } from '@/context/LanguageContext'
import Link from 'next/link'
import { motion } from 'framer-motion'

interface Feature {
  icon: string
  title: string
  desc: string
}

export default function Home() {
  const { t } = useLanguage()

  const features: Feature[] = [
    {
      icon: '🛰️',
      title: t('home.features.satellite'),
      desc: 'Satellite truth from space',
    },
    {
      icon: '⛓️',
      title: t('home.features.blockchain'),
      desc: 'Immutable blockchain records',
    },
    {
      icon: '💰',
      title: t('home.features.pricing'),
      desc: 'Fair market prices',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-primary via-secondary to-primary text-white">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-20 md:py-40">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center"
        >
          <h1 className="text-5xl md:text-7xl font-bold mb-4">
            {t('home.title')}
          </h1>
          <p className="text-xl md:text-2xl mb-6 opacity-90">
            {t('home.subtitle')}
          </p>
          <p className="text-lg md:text-xl mb-12 opacity-80">
            {t('home.tagline')}
          </p>

          <Link
            href="/dashboard"
            className="inline-block bg-white text-primary px-8 py-4 rounded-lg font-bold text-lg hover:bg-opacity-90 transition transform hover:scale-105"
          >
            {t('home.cta')} →
          </Link>
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="bg-white text-dark py-20">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16">Key Features</h2>

          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.2 }}
                className="bg-light p-8 rounded-lg shadow-lg hover:shadow-xl transition"
              >
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-2xl font-bold mb-2 text-primary">{feature.title}</h3>
                <p className="text-gray-600">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-primary to-secondary text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-8">Ready to Transform Agriculture?</h2>
          <Link
            href="/dashboard"
            className="inline-block bg-white text-primary px-8 py-4 rounded-lg font-bold text-lg hover:bg-opacity-90 transition"
          >
            Get Started Now 🚀
          </Link>
        </div>
      </section>
    </div>
  )
}
