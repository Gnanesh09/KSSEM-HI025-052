// lib/api.ts
import axios, { AxiosInstance } from 'axios'
import {
  Farmer,
  Field,
  InsuranceClaim,
  SatelliteData,
  BlockchainStats,
  Block,
} from './types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const API_BASE = '/api/v1'

const api: AxiosInstance = axios.create({
  baseURL: `${API_URL}${API_BASE}`,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const farmerAPI = {
  register: (data: Partial<Farmer>) => api.post<Farmer>('/farmers/register', data),
  get: (farmerId: string) => api.get<Farmer>(`/farmers/${farmerId}`),
  list: () => api.get<Farmer[]>('/farmers/'),
}

export const fieldAPI = {
  register: (data: Partial<Field>) => api.post<Field>('/fields/register', data),
  get: (fieldId: string) => api.get<Field>(`/fields/${fieldId}`),
  getByFarmer: (farmerId: string) => api.get<Field[]>(`/fields/farmer/${farmerId}`),
}

export const insuranceAPI = {
  fileClaim: (data: Partial<InsuranceClaim>) =>
    api.post<InsuranceClaim>('/insurance/claim', data),
  getClaim: (claimId: string) => api.get<InsuranceClaim>(`/insurance/claim/${claimId}`),
  listClaims: () => api.get<InsuranceClaim[]>('/insurance/claims'),
}

export const satelliteAPI = {
  getNDVI: (fieldId: string, date?: string) =>
    api.get<SatelliteData>(`/satellite/ndvi/${fieldId}`, { params: { date } }),
  getTimeline: (fieldId: string, startDate: string, endDate: string) =>
    api.get<{ field_id: string; crop: string; location: string; timeline: SatelliteData[] }>(
      `/satellite/timeline/${fieldId}`,
      { params: { start_date: startDate, end_date: endDate } }
    ),
}

export const blockchainAPI = {
  getStats: () => api.get<BlockchainStats>('/blockchain/stats'),
  getAllBlocks: () => api.get<{ total_blocks: number; blocks: Block[] }>('/blockchain/blocks'),
}

export default api
