// app/dashboard/page.tsx
'use client'

import { useLanguage } from '@/context/LanguageContext'
import { useEffect, useState } from 'react'
import { farmerAPI, fieldAPI, insuranceAPI } from '@/lib/api'
import { Farmer, Field, InsuranceClaim } from '@/lib/types'
import LoadingSpinner from '@/components/LoadingSpinner'
import { motion } from 'framer-motion'

interface Stat {
  icon: string
  label: string
  value: string | number
}

export default function Dashboard() {
  const { t } = useLanguage()
  const [farmer, setFarmer] = useState<Farmer | null>(null)
  const [fields, setFields] = useState<Field[]>([])
  const [claims, setClaims] = useState<InsuranceClaim[]>([])
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        const [farmerRes, fieldsRes, claimsRes] = await Promise.all([
          farmerAPI.get('FAR-0001'),
          fieldAPI.getByFarmer('FAR-0001'),
          insuranceAPI.listClaims(),
        ])

        setFarmer(farmerRes.data)
        setFields(fieldsRes.data)
        setClaims(claimsRes.data)
      } catch (error) {
        console.error('Error:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) return <LoadingSpinner />

  const approvedClaims = claims.filter(c => c.status === 'APPROVED').length
  const totalPayout = claims
    .filter(c => c.status === 'APPROVED')
    .reduce((sum, c) => sum + c.payout, 0)

  const stats: Stat[] = [
    { icon: '🌾', label: t('dashboard.myFields'), value: fields.length },
    { icon: '✅', label: t('dashboard.claimsApproved'), value: approvedClaims },
    { icon: '💰', label: t('dashboard.totalPayouts'), value: `₹${totalPayout.toLocaleString()}` },
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12"
      >
        <h1 className="text-4xl font-bold text-primary mb-4">
          {t('dashboard.welcome')}, {farmer?.name}! 👋
        </h1>
        <p className="text-gray-600">Farmer ID: {farmer?.farmer_id}</p>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid md:grid-cols-3 gap-8 mb-12">
        {stats.map((stat, i) => (
          <motion.div
            key={i}
            whileHover={{ scale: 1.05 }}
            className="bg-gradient-to-br from-primary to-secondary text-white p-8 rounded-lg shadow-lg"
          >
            <div className="text-4xl mb-2">{stat.icon}</div>
            <p className="text-opacity-80 text-white mb-2">{stat.label}</p>
            <p className="text-3xl font-bold">{stat.value}</p>
          </motion.div>
        ))}
      </div>

      {/* Fields List */}
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-primary mb-6">{t('dashboard.myFields')}</h2>

        {fields.length === 0 ? (
          <p className="text-gray-600">No fields registered yet</p>
        ) : (
          <div className="grid md:grid-cols-2 gap-6">
            {fields.map((field) => (
              <motion.div
                key={field.field_id}
                whileHover={{ y: -5 }}
                className="border-2 border-primary rounded-lg p-6"
              >
                <h3 className="text-xl font-bold text-primary mb-2">{field.field_id}</h3>
                <p className="text-gray-600">🌾 Crop: {field.crop}</p>
                <p className="text-gray-600">📏 Size: {field.size_acres} acres</p>
                <p className="text-gray-600">📍 Location: {field.location}</p>
                <p className="text-gray-600">🛰️ NDVI: {field.latest_ndvi || 'N/A'}</p>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
