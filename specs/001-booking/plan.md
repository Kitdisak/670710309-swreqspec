## 1. สรุปแนวทาง (5 บรรทัด)
ฟีเจอร์นี้ให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ แล้วได้รับหมายเลขคิวที่รีเซ็ตรายวัน
บริการหลักคือ Booking Service ที่ทำงานบนเซิร์ฟเวอร์เพื่อแสดงช่วงเวลาว่าง จัดการการจองแบบอะตอมิก และส่งงานแจ้งเตือนแบบ asynchronous
แนวทางคือใช้ฐานข้อมูล MySQL สำหรับข้อมูลถาวร, เก็บงานแจ้งเตือนในคิวแล้วให้ worker ส่งจริงแบบ background, และทำธุรกรรม DB เพื่อป้องกัน overbooking
การออกหมายเลขคิวจะเป็น counter รายวัน (รีเซ็ตรายวัน ตามเขตเวลา Asia/Bangkok) และการส่งข้อความเป็นงานแยกต่างหากที่รองรับ retry
แผนนี้อ้างอิง `SPEC-BKG-001` และ Assumptions / Open Questions ใน `spec.md`

## 2. เทคโนโลยีที่ใช้
สิ่งที่เลือก | มาจาก | หมายเหตุ
---|---|---
Backend: Python + FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | ค่าเริ่มต้นรายวิชา
Database: MySQL | CON-TECH-01 | ตามข้อกำหนด
Frontend: React (Vite) | ทีมเลือกเอง ไม่ได้มาจาก spec | ค่าเริ่มต้นรายวิชา
Notification queue: Redis (หรือ RabbitMQ) | ทีมเลือกเอง ไม่ได้มาจาก spec | ใช้สำหรับ `IF-NOT-01` แบบ asynchronous
Background worker: RQ / Celery (Python) | ทีมเลือกเอง ไม่ได้มาจาก spec | worker อ่านจากคิวและส่งข้อความ

## 3. โมเดลข้อมูล (entities และฟิลด์หลัก)
- `periods` — (id, date, start_time, end_time, quota) — รองรับ FR-BKG-01
- `quotas` — (id, period_id, package_id NULLABLE, remaining) — รองรับ FR-BKG-01, FR-BKG-06
- `bookings` — (id, hn, period_id, package_id, status, queue_number, created_at, created_by) — รองรับ FR-BKG-04, FR-BKG-02
	- ห้ามเก็บเลขบัตรประชาชน ตาม IF-HIS-01
- `daily_counters` — (date, counter) — เก็บค่าเพื่อสร้างหมายเลขคิวรีเซ็ตรายวัน — รองรับ ASM-03
- `booking_queue` — (id, booking_id, provider_payload, status, attempts, next_attempt_at) — รองรับ FR-BKG-05, NFR-REL-02
- `audit_logs` — (id, user, action, target_booking_id, timestamp) — รองรับ DOM-PDPA-01, AC-BKG-06

## 4. API / หน้าจอ (แต่ละรายการระบุ FR ที่รองรับ)
- GET /periods?from=YYYY-MM-DD&to=YYYY-MM-DD — คืนรายการช่วงเวลาและจำนวนที่นั่งที่เหลือ (รองรับ FR-BKG-01)
- POST /bookings — payload: {hn, period_id, package_id} — ตอบ: {booking_id, queue_number} (รองรับ FR-BKG-04, FR-BKG-02)
- GET /bookings/{id} — คืนสถานะการจองและหมายเลขคิว (รองรับ FR-BKG-04, FR-BKG-05)
- UI: หน้าเลือกแพ็กเกจ+วันที่+ช่วงเวลา — แสดง remaining ของแต่ละช่วง (รองรับ FR-BKG-01, FR-BKG-06)
- UI: หน้ายืนยันการจอง — แสดงหมายเลขคิวเมื่อสำเร็จ (รองรับ FR-BKG-04)

## 5. ตารางตรวจ Constraints
Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ
---|---|---
CON-TECH-01 | Database: MySQL; schema และ transactions | ใช้แล้ว
DOM-PDPA-01 | `audit_logs` เก็บผู้เข้าถึง เวลา และรหัสผู้รับบริการ | ใช้แล้ว
IF-IDP-01 | Middleware ตรวจผลยืนยันตัวตนก่อนเข้าถึง API | ใช้แล้ว
IF-HIS-01 | Integration: ดึง HN จาก HIS; ไม่เก็บเลขบัตรประชาชนใน `bookings` | ใช้แล้ว
IF-NOT-01 | Notification queue + background worker ส่ง SMS/LINE แบบ asynchronous | ใช้แล้ว

## 6. แผนทดสอบจาก Acceptance Criteria
AC ID | ชื่อ test | ทดสอบอย่างไร
---|---|---
AC-BKG-01 | test_AC_BKG_01_booking_commit | สร้างช่วงเวลา remaining=1 แล้ว POST /bookings; ยืนยัน transaction commit, ตรวจ `bookings` และ `periods.remaining==0`
AC-BKG-02 | test_AC_BKG_02_reject_duplicate_daily | สร้าง booking สำหรับ hn เดียวในวันเดียวกันแล้วพยายามสร้างอีกครั้ง => ควรถูกปฏิเสธและแสดงหมายเลขคิวเดิม
AC-BKG-03 | test_AC_BKG_03_nearby_periods | จำลองกรณี concurrent: remaining=1, user A ยืนยันสำเร็จ, user B ยืนยันตามมา => ตรวจแสดงข้อความ "ช่วงเวลาเต็ม" และเสนอ 3 ช่วงเวลาใกล้เคียง
AC-BKG-04 | test_AC_BKG_04_notify_queue | จำลอง provider ไม่ตอบ: POST /bookings แล้วตรวจว่า `booking_queue` มีรายการสำหรับ retry และ `next_attempt_at` ภายใน 5 นาที
AC-BKG-05 | test_AC_BKG_05_performance | โหลดเทสต์ GET /periods ที่ 200 concurrent users วัด p95 <= 2s
AC-BKG-06 | test_AC_BKG_06_audit_log | เปิดดูข้อมูลการจองแล้วตรวจ `audit_logs` บันทึกผู้เข้าถึง เวลา และรหัสผู้รับบริการ

## 7. ลำดับงาน (5-10 ขั้น)
1. ออกแบบ DB schema และ migration (FR-BKG-01, FR-BKG-04, DOM-PDPA-01)
2. พัฒนา GET /periods พร้อม caching และ indexing (FR-BKG-01, AC-BKG-05)
3. พัฒนา POST /bookings: transaction flow (check remaining -> decrement -> create booking -> increment daily counter) (FR-BKG-04, FR-BKG-02)
4. พัฒนา background worker สำหรับ `booking_queue` และ retry logic (FR-BKG-05, AC-BKG-04)
5. เพิ่ม integration กับ IF-HIS และ IF-IDP (IF-HIS-01, IF-IDP-01)
6. เขียน unit/integration tests และ mock providers (ทุก AC ที่เกี่ยวข้อง)
7. ทำ load testing และปรับ performance (AC-BKG-05)
8. เตรียม release checklist และ docs สำหรับทีมปฏิบัติการ

## 8. สิ่งที่ยังไม่ทำ
- Q-01 "ช่วงเวลาใกล้เคียง" (จาก `spec.md`) — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ

