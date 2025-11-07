// lib/types.ts
export interface Farmer {
  farmer_id: string
  name: string
  phone: string
  location: string
  village?: string
  district: string
  state: string
  created_at: string
}

export interface Field {
  field_id: string
  farmer_id: string
  size_acres: number
  crop: string
  location: string
  gps_latitude?: number
  gps_longitude?: number
  latest_ndvi: number
  created_at: string
}

export interface InsuranceClaim {
  claim_id: string
  field_id: string
  damage_type: string
  pre_ndvi: number
  post_ndvi: number
  damage_percent: number
  status: 'APPROVED' | 'REJECTED'
  payout: number
  blockchain_tx: string
  block_number: number
  filed_at: string
}

export interface SatelliteData {
  field_id: string
  date: string
  ndvi: number
  status: string
  source: string
  image?: string
  resolution: string
  free: boolean
}

export interface BlockchainStats {
  total_blocks: number
  total_transactions: number
  latest_hash: string
  is_valid: boolean
  pending: number
}

export interface Block {
  index: number
  timestamp: string
  transactions: Transaction[]
  previous_hash: string
  hash: string
  nonce: number
}

export interface Transaction {
  type: string
  claim_id?: string
  field_id?: string
  damage_type?: string
  pre_ndvi?: number
  post_ndvi?: number
  damage_percent?: number
  status?: string
  payout?: number
  [key: string]: any
}
