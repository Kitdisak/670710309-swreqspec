# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from app.db.models import Booking, Slot
from tests.conftest import AUTH


def test_AC_BKG_01(client, db, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    # Given: ผู้รับบริการยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: การจองถูกบันทึก และที่นั่งว่างของช่วงนั้นเป็น 0
    assert res.status_code == 201
    assert db.query(Booking).count() == 1
    assert res.json()["queue_no"] is not None
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_1_booking_success(client, db, make_slot):
    """TC-BKG-01-1: การจองสำเร็จเมื่อมีที่นั่งว่าง 1 ที่"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; แสดงหมายเลขคิว (รอ Q-02); ที่นั่งว่างของช่วงนั้นเป็น 0; ส่งคำขอส่งข้อความยืนยัน
    assert res.status_code == 201
    assert db.query(Booking).count() == 1
    assert res.json()["queue_no"] is not None
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_2_last_seat_booking(client, db, make_slot):
    """TC-BKG-01-2: การจองสำเร็จเมื่อเป็นที่นั่งสุดท้าย"""
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่ เป็นชั่วโมงสุดท้ายก่อนเต็ม
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; แสดงหมายเลขคิว (รอ Q-02); จำนวนที่นั่งคงเหลือของช่วงนั้นลดจาก 1 เป็น 0; ไม่สร้างรายการจองซ้อน
    assert res.status_code == 201
    assert db.query(Booking).count() == 1
    assert res.json()["queue_no"] is not None
    assert db.get(Slot, slot.id).remaining == 0


def test_TC_BKG_01_3_unverified_user_cannot_book(client, db, make_slot):
    """TC-BKG-01-3: ผู้ใช้ที่ยังไม่ยืนยันตัวตนไม่สามารถจองได้"""
    # Given: ผู้รับบริการยังไม่ได้ยืนยันตัวตนจากระบบยืนยันตัวตน
    slot = make_slot(start="09:00", remaining=1)

    # When: พยายามยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ไม่บันทึกการจอง; ไม่แสดงหมายเลขคิว; จบด้วยข้อปฏิเสธตาม IF-IDP-01
    assert res.status_code == 401
    assert res.json()["detail"] == "ยังไม่ได้ยืนยันตัวตน"
    assert db.query(Booking).count() == 0
    assert db.get(Slot, slot.id).remaining == 1
