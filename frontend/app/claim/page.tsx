// app/claim/page.tsx
'use client'

import { useLanguage } from '@/context/LanguageContext'
import { useState, useEffect } from 'react'
import { fieldAPI, insuranceAPI, satelliteAPI } from '@/lib/api'
import { Field, InsuranceClaim, SatelliteData } from '@/lib/types'
import SuccessModal from '@/components/SuccessModal'
import LoadingSpinner from '@/components/LoadingSpinner'
import { motion } from 'framer-motion'

interface FormData {
  field_id: string
  damage_type: string
  pre_ndvi: number
  post_ndvi: number
}

export default function FileClaim() {
  const { t } = useLanguage()
  const [fields, setFields] = useState<Field[]>([])
  const [formData, setFormData] = useState<FormData>({
    field_id: '',
    damage_type: 'drought',
    pre_ndvi: 0.78,
    post_ndvi: 0.29,
  })
  const [loading, setLoading] = useState<boolean>(false)
  const [success, setSuccess] = useState<InsuranceClaim | null>(null)
  const [satelliteData, setSatelliteData] = useState<SatelliteData | null>(null)

  useEffect(() => {
    fetchFields()
  }, [])

  const fetchFields = async () => {
    try {
      const res = await fieldAPI.getByFarmer('FAR-0001')
      setFields(res.data)
    } catch (error) {
      console.error('Error fetching fields:', error)
    }
  }

  const handleFieldChange = async (fieldId: string) => {
    setFormData({ ...formData, field_id: fieldId })

    try {
      const res = await satelliteAPI.getNDVI(fieldId)
      setSatelliteData(res.data)
    } catch (error) {
      console.error('Error fetching satellite data:', error)
    }
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLoading(true)

    try {
      const res = await insuranceAPI.fileClaim(formData)
      setSuccess(res.data)
      setFormData({
        field_id: '',
        damage_type: 'drought',
        pre_ndvi: 0.78,
        post_ndvi: 0.29,
      })
    } catch (error) {
      console.error('Error filing claim:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <motion.h1
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-4xl font-bold text-primary mb-8"
      >
        {t('fileClaim.title')}
      </motion.h1>

      <div className="grid md:grid-cols-2 gap-8">
        {/* Form */}
        <motion.form
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          onSubmit={handleSubmit}
          className="bg-white p-8 rounded-lg shadow-lg"
        >
          <div className="mb-6">
            <label className="block text-primary font-bold mb-2">
              {t('fileClaim.selectField')}
            </label>
            <select
              value={formData.field_id}
              onChange={(e) => handleFieldChange(e.target.value)}
              className="w-full border-2 border-primary rounded px-4 py-2"
            >
              <option value="">Select a field...</option>
              {fields.map((field) => (
                <option key={field.field_id} value={field.field_id}>
                  {field.field_id} - {field.crop}
                </option>
              ))}
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-primary font-bold mb-2">
              {t('fileClaim.damageType')}
            </label>
            <select
              value={formData.damage_type}
              onChange={(e) =>
                setFormData({ ...formData, damage_type: e.target.value })
              }
              className="w-full border-2 border-primary rounded px-4 py-2"
            >
              <option value="drought">{t('fileClaim.drought')}</option>
              <option value="flood">{t('fileClaim.flood')}</option>
              <option value="pest">{t('fileClaim.pest')}</option>
              <option value="hailstorm">{t('fileClaim.hailstorm')}</option>
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-primary font-bold mb-2">
              Pre-Damage NDVI
            </label>
            <input
              type="number"
              value={formData.pre_ndvi}
              onChange={(e) =>
                setFormData({ ...formData, pre_ndvi: parseFloat(e.target.value) })
              }
              min="0"
              max="1"
              step="0.01"
              className="w-full border-2 border-primary rounded px-4 py-2"
            />
          </div>

          <div className="mb-6">
            <label className="block text-primary font-bold mb-2">
              Post-Damage NDVI
            </label>
            <input
              type="number"
              value={formData.post_ndvi}
              onChange={(e) =>
                setFormData({ ...formData, post_ndvi: parseFloat(e.target.value) })
              }
              min="0"
              max="1"
              step="0.01"
              className="w-full border-2 border-primary rounded px-4 py-2"
            />
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-primary to-secondary text-white font-bold py-3 rounded-lg hover:shadow-lg transition"
          >
            {t('fileClaim.submit')} →
          </button>
        </motion.form>

        {/* Satellite Data Preview */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-8 rounded-lg shadow-lg"
        >
          <h2 className="text-2xl font-bold text-primary mb-6">
            {t('satellite.title')}
          </h2>

          {satelliteData ? (
            <div>
              <div className="bg-green-100 p-4 rounded mb-4">
                <p className="text-green-900 font-bold">{t('satellite.before')}</p>
                <p className="text-2xl font-bold text-green-700">{satelliteData.ndvi}</p>
                <p className="text-green-600">{satelliteData.status}</p>
              </div>

              <div className="bg-red-100 p-4 rounded">
                <p className="text-red-900 font-bold">{t('satellite.after')}</p>
                <p className="text-lg text-gray-600">Post-damage data pending...</p>
              </div>
            </div>
          ) : (
            <p className="text-gray-600">Select a field to view satellite data</p>
          )}
        </motion.div>
      </div>

      {success && (
        <SuccessModal claim={success} onClose={() => setSuccess(null)} />
      )}
    </div>
  )
}
