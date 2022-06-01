import axios from 'axios'
import { baseUrl } from '@/config'

const api = axios.create({
  baseURL: baseUrl,
  headers: {
    'Content-Type': 'application/json'
  }
})

export { api }
