import { useEffect, useState } from 'react'

import { mockApi } from '../api/client.js'

function getDateAfterDays(days) {
  const date = new Date()
  date.setDate(date.getDate() + days)
  return date.toISOString().slice(0, 10)
}

function getAvailableDates() {
  return Array.from({ length: 30 }, (_, index) => getDateAfterDays(index))
}

export default function SlotPicker() {
  const availableDates = getAvailableDates()
  const [dateFrom, setDateFrom] = useState(availableDates[0])
  const [packageCode, setPackageCode] = useState('')
  const [slots, setSlots] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let active = true
    setLoading(true)
    mockApi.getSlots({ dateFrom, packageCode: packageCode || 'unspecified' }).then((result) => {
      if (active) {
        setSlots(result.slots)
        setLoading(false)
      }
    })
    return () => {
      active = false
    }
  }, [dateFrom, packageCode])

  return (
    <section className="min-h-screen bg-slate-100 px-4 py-8 text-slate-900 sm:px-8">
      <div className="mx-auto max-w-5xl">
        <header className="mb-8 border-b border-slate-300 pb-6">
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-teal-700">
            Booking / UC-01
          </p>
          <p className="mt-3 text-sm font-medium text-slate-500">ระบบจองคิวตรวจสุขภาพ</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">
            เลือกแพ็กเกจและช่วงเวลาตรวจ
          </h1>
          <p className="mt-3 max-w-2xl text-slate-600">
            เลือกวันภายใน 30 วันข้างหน้า แล้วตรวจสอบที่นั่งคงเหลือของแต่ละช่วงเวลา
          </p>
        </header>

        <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
          <aside className="h-fit border border-slate-200 bg-white p-5 shadow-sm">
            <label className="block text-sm font-semibold text-slate-700" htmlFor="package-code">
              รหัสแพ็กเกจ
            </label>
            <input
              id="package-code"
              className="mt-2 w-full border border-slate-300 px-3 py-2 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
              value={packageCode}
              onChange={(event) => setPackageCode(event.target.value)}
              placeholder="กรอกรหัสแพ็กเกจ"
            />

            <label className="mt-6 block text-sm font-semibold text-slate-700" htmlFor="booking-date">
              วันที่ตรวจ
            </label>
            <select
              id="booking-date"
              className="mt-2 w-full border border-slate-300 bg-white px-3 py-2 outline-none focus:border-teal-600 focus:ring-2 focus:ring-teal-100"
              value={dateFrom}
              onChange={(event) => setDateFrom(event.target.value)}
            >
              {availableDates.map((date) => (
                <option key={date} value={date}>{date}</option>
              ))}
            </select>
            <p className="mt-3 text-xs leading-5 text-slate-500">ระบบแสดงวันตรวจที่เลือกได้ตั้งแต่วันนี้ถึง 30 วันข้างหน้า</p>
          </aside>

          <div>
            <div className="mb-4 flex items-end justify-between gap-4">
              <div>
                <h2 className="text-xl font-bold">ช่วงเวลาที่ว่าง</h2>
                <p className="mt-1 text-sm text-slate-500">วันที่ {dateFrom}</p>
              </div>
              <span className="text-sm text-slate-500">{slots.length} ช่วงเวลา</span>
            </div>

            {loading ? (
              <p className="border border-slate-200 bg-white p-6 text-slate-500">กำลังโหลดช่วงเวลา...</p>
            ) : (
              <div className="grid gap-3 sm:grid-cols-2">
                {slots.map((slot) => (
                  <button
                    type="button"
                    key={slot.id}
                    className="border border-slate-200 bg-white p-5 text-left shadow-sm transition hover:border-teal-600 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-teal-500"
                    disabled={slot.remaining === 0}
                  >
                    <span className="block text-2xl font-bold text-slate-900">{slot.start_time} น.</span>
                    <span className="mt-2 block text-sm text-teal-700">
                      {slot.remaining > 0 ? `เหลือ ${slot.remaining} ที่นั่ง` : 'เต็มแล้ว'}
                    </span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}
