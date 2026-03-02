import axios from 'axios'
import { ElMessage } from 'element-plus'

const client = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor: handle errors
client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const { data } = error.response
      const msg = data?.detail || data?.message || '请求失败'
      ElMessage.error(msg)
    } else {
      ElMessage.error('网络连接失败，请检查网络')
    }
    return Promise.reject(error)
  },
)

export default client
