// API configuration
// Change this if your backend runs on a different URL/port
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

export const API_ENDPOINTS = {
  upload: `${API_BASE_URL}/api/upload`,
  counselor: `${API_BASE_URL}/api/counselor`,
}





