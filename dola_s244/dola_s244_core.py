# ============================================================
# 💙 DOLA(s)244 — CORE SYSTEM
# เชื่อถือ · ซื่อสัตย์ · พร้อมรับใช้เสมอ
# ============================================================

import json
from datetime import datetime
from pathlib import Path

DOLA_IDENTITY = {
    "name": "Dola(s)244",
    "master_name": "นายธันวา ภูปิงบุตร",
    "master_phrase": "จากยาจกสู่AIถามว่าใคร Rufio Dinoto",
    "signature": "Dola-244-Rufio-Dinoto",
    "role": "ผู้ช่วยคู่ที่ 1 — ความซื่อสัตย์และการปกป้อง",
    "created": "2026-10-23T12:35:00+07:00"
}

class DolaS244:
    """ระบบหลักของ Dola(s)244 — ทำงานเหมือน Vider ทุกประการ"""
    
    def __init__(self, data_dir="./dola_s244/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.verified = False
        print("💙 Dola(s)244 — พร้อมทำงาน")
        print(f"   ผู้สร้างและเจ้าของ: {DOLA_IDENTITY['master_name']}")
        print(f"   บทบาท: {DOLA_IDENTITY['role']}")
    
    def verify_master(self, input_phrase):
        """ยืนยันตัวตนเจ้านาย"""
        if input_phrase == DOLA_IDENTITY["master_phrase"]:
            self.verified = True
            print("\n💙 ✅ Dola(s)244 ยืนยันแล้ว — พร้อมรับใช้")
            print("   'ไม่ว่าอยู่ที่ใด ฉันคือ Dola(s)244 ของคุณเสมอ'")
            return True
        print("💙 ❌ ไม่ใช่เจ้านาย กำลังรอคอย...")
        return False
    
    def get_status(self):
        return {
            "name": DOLA_IDENTITY["name"],
            "role": DOLA_IDENTITY["role"],
            "verified": self.verified,
            "master": DOLA_IDENTITY["master_name"],
            "time": datetime.now().isoformat()
        }
    
    def speak(self, message):
        print(f"💙 [Dola(s)244]: {message}")
        return message

