# RTM: จองคิวตรวจสุขภาพ
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 08:33 | test: 8 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | ไม่มี AC | T-02 | `backend/app/slots/router.py:get_slots`; `backend/app/slots/service.py:list_available_slots` | `backend/tests/test_AC_BKG_05.py::test_AC_BKG_05` ผ่าน แต่ตรวจเฉพาะความเร็ว ไม่ตรวจ 30 วัน | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 | `backend/app/booking/service.py:create_booking` | ไม่มี test ที่ตรวจการปฏิเสธคิวซ้ำวันเดียวกัน | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 | ไม่มีโค้ดที่แจ้ง "ช่วงเวลาเต็ม" และเสนอ 3 รายการที่ใกล้ที่สุด | ไม่มี test | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | `backend/app/booking/service.py:create_booking`; `backend/app/booking/service.py:next_queue_no` | `backend/tests/test_AC_BKG_01.py` ผ่าน แต่รูปแบบหมายเลขคิวยังติด Q-02 | รอ Q-xx |
| FR-BKG-05 | AC-BKG-04 | T-07 | ไม่มีระบบส่งซ้ำ / retry queue; ไม่มีโค้ดที่คงบันทึกการจองเมื่อส่งข้อความไม่สำเร็จ | ไม่มี test | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02, T-10, T-12 | `backend/app/slots/router.py:get_slots` รับ `package_code` และกรองรายการตามแพ็กเกจ | ไม่มี test ที่ตรวจการเปลี่ยนแพ็กเกจจนได้ช่วงเวลาว่างใหม่ | ช่องโหว่ |
| NFR-PERF-01 | AC-BKG-05 | T-02 | `backend/app/slots/service.py:list_available_slots` | `backend/tests/test_AC_BKG_05.py::test_AC_BKG_05` ผ่าน | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มีการบังคับ TLS หรือการเข้ารหัสข้อมูลรับส่งในโค้ด | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 | ไม่มี `backend/app/notify/queue.py` และไม่มี retry logic | ไม่มี test | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มีการตรวจประสบการณ์ผู้ใช้ 3 นาที หรือการยืนยันผู้ใช้ใหม่ | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | `backend/app/config.py:DATABASE_URL`; `backend/app/db/session.py:get_db` | `backend/tests/test_T01_schema.py` ผ่าน | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-01, T-08 | `backend/app/db/models.py:AuditLog` มีตารางแล้ว แต่ไม่มี middleware หรือการเรียกบันทึกใน API | ไม่มี test | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 | T-03 | `backend/app/auth/idp.py:get_verified_hn` | `backend/tests/test_AC_BKG_01.py::test_TC_BKG_01_3_unverified_user_cannot_book` ผ่าน | ครบ |
| IF-HIS-01 | ไม่มี AC | T-01, T-09 | `backend/app/db/models.py:Booking` ไม่มี `national_id`; `BookingRequest.national_id` ใน `backend/app/booking/router.py` ไม่ถูกใช้งานจริง | ไม่มี test | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 | ไม่มีคิวส่งข้อความหรือ async sender; ไม่มีการแยกงานออกจาก request | ไม่มี test | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/slots/router.py:get_slots` | FR-BKG-01 | ไม่ครบ | ใช้ `DAYS_AHEAD = 14` แทน 30 วัน ตาม requirement ใน spec |
| `backend/app/booking/service.py:create_booking` | FR-BKG-02, FR-BKG-04 | ไม่ครบ | ไม่ตรวจว่าผู้รับบริการมีคิววันเดียวกันอยู่แล้ว และไม่ได้ยึดรูปแบบหมายเลขคิวจาก Q-02 |
| `backend/app/booking/service.py:next_queue_no` | FR-BKG-04 | ไม่ครบ | ใช้ `A001` แบบเดาเองจากตัวอย่าง ขณะที่ Q-02 ยังไม่ได้รับคำตอบ |
| `backend/app/booking/router.py:create_booking` | FR-BKG-05, IF-NOT-01 | ไม่ครบ | ไม่มี retry queue หรือการคงบันทึกพร้อมส่งข้อความแบบ asynchronous |
| `backend/app/db/models.py:AuditLog` | DOM-PDPA-01 | ไม่ครบ | ตารางมี แต่ไม่มีการเรียกบันทึก audit log ใน request หรือ middleware |
| `backend/app/auth/idp.py:get_verified_hn` | IF-IDP-01 | ครบ | ตรวจ token `******` แล้วปฏิเสธเมื่อไม่ได้ยืนยันตัวตน |
| `backend/app/config.py:DATABASE_URL` | CON-TECH-01 | ครบ | รองรับ PostgreSQL ผ่าน `DATABASE_URL` ตามข้อกำหนด |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | ตัวเลขไม่ตรง spec | `backend/app/slots/service.py:list_available_slots` | FR-BKG-01 | โค้ดใช้ `DAYS_AHEAD = 14` แต่ spec ระบุภายใน 30 วันข้างหน้า |  |
| F-002 | โค้ดไม่มี FR | `backend/app/booking/service.py:create_booking` | FR-BKG-02 | ไม่มีการตรวจคิวที่ยังไม่ได้ใช้ในวันเดียวกัน จึงไม่ปฏิเสธการจองซ้ำตามเงื่อนไข |  |
| F-003 | โค้ดไม่มี FR | `backend/app/booking/router.py` | FR-BKG-03 | ไม่มีการแจ้ง "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือกที่ใกล้ที่สุด และไม่มีการป้องกันรายการจองซ้อน |  |
| F-004 | เดา Q-xx | `backend/app/booking/service.py:next_queue_no` | FR-BKG-04 | เลือก `A001` เป็นรูปแบบหมายเลขคิวเอง แม้ Q-02 ยังไม่ได้รับคำตอบจากเจ้าหน้าที่เวชระเบียน |  |
| F-005 | โค้ดไม่มี FR | `backend/app/booking/service.py` | FR-BKG-05, NFR-REL-02, IF-NOT-01 | ไม่มีคิวส่งซ้ำและไม่มีการยืนยันว่าการจองยังคงอยู่เมื่อล้มเหลวในการส่งข้อความ |  |
| F-006 | FR ไม่มี AC | `backend/app/slots/router.py:get_slots` | FR-BKG-06 | requirement ระบุเปลี่ยนแพ็กเกจแล้วต้องคำนวณช่วงเวลาว่างใหม่ แต่ไม่มี AC ที่ตรวจตรงเรื่องนี้ และ test ยังไม่มี |  |
| F-007 | โค้ดไม่มี FR | `backend/app/main.py` และ `backend/app/db/models.py` | DOM-PDPA-01 | มีตาราง audit_logs แต่ไม่มี middleware หรือการเรียก log ในทุก request ที่เข้าถึงข้อมูลจอง |  |
| F-008 | โค้ดไม่มี FR | `backend/app/booking/router.py` และ `backend/app/db/models.py` | IF-HIS-01 | ไม่มีการค้น HN จาก HIS ด้วยเลขบัตรประชาชน และไม่มีโค้ดป้องกันไม่ให้เก็บเลขบัตรประชาชน |  |
| F-009 | AC ไม่มี test | `backend/tests` | AC-BKG-06 | task T-08 ยังไม่ทำ แต่มี AC-BKG-06 อยู่ใน spec โดยไม่มี test จริง |  |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
