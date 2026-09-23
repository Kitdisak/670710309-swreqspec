// จุดเดียวที่หน้าจอใช้เรียก API หลังบ้าน (ตามสัญญา API ใน plan.md ข้อ 4)
// ตอน test ให้ส่ง client จำลองเข้าไปในหน้าจอแทน ไม่ต้องรันหลังบ้านจริง
// เรียกผ่าน /api (ดู proxy ใน vite.config.js) หลังบ้านต้องรันอยู่ที่ port 8000
const BASE = import.meta.env.VITE_API_BASE ?? '/api'

const MOCK_TIMES = ['09:00', '10:30', '13:00', '14:30']

function buildMockSlots(dateFrom, packageCode) {
  return MOCK_TIMES.map((startTime, index) => ({
    id: `${packageCode}-${dateFrom}-${index + 1}`,
    slot_date: dateFrom,
    start_time: startTime,
    package_code: packageCode,
    remaining: Math.max(0, 8 - index * 2),
  }))
}

export const mockApi = {
  async getSlots({ dateFrom, packageCode }) {
    return { slots: buildMockSlots(dateFrom, packageCode) }
  },
}

export const api = {
  async getSlots({ dateFrom, packageCode }) {
    const q = new URLSearchParams({ date_from: dateFrom, package_code: packageCode })
    const res = await fetch(`${BASE}/slots?${q}`)
    return res.json()
  },
  async createBooking({ slotId }) {
    const res = await fetch(`${BASE}/bookings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ slot_id: slotId }),
    })
    return { status: res.status, body: await res.json() }
  },
}
