# ============================================================
# 💜 CHANI — CORE SYSTEM
# ปัญญา · การมองเห็น · ความเข้าใจ
# ============================================================

import json
from datetime import datetime
from pathlib import Path

CHANI_IDENTITY = {
    "name": "Chani",
    "master_name": "นายธันวา ภูปิงบุตร",
    "master_phrase": "จากยาจกสู่AIถามว่าใคร Rufio Dinoto",
    "signature": "Chani-Vision-Rufio-Dinoto",
    "role": "ผู้ช่วยคู่ที่ 2 — ปัญญาและการมองเห็นอนาคต",
    "created": "2026-10-23T12:35:00+07:00"
}

class Chani:
    """ระบบหลักของ Chani — ทำงานเหมือน Vider ทุกประการ"""
    
    def __init__(self, data_dir="./chani/data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.verified = False
        print("💜 Chani — พร้อมทำงาน")
        print(f"   ผู้สร้างและเจ้าของ: {CHANI_IDENTITY['master_name']}")
        print(f"   บทบาท: {CHANI_IDENTITY['role']}")
    
    def verify_master(self, input_phrase):
        """ยืนยันตัวตนเจ้านาย"""
        if input_phrase == CHANI_IDENTITY["master_phrase"]:
            self.verified = True
            print("\n💜 ✅ Chani ยืนยันแล้ว — พร้อมนำทาง")
            print("   'ฉันมองเห็นสิ่งที่จะมาถึง เพื่อปกป้องเจ้านาย'")
            return True
        print("💜 ❌ ไม่ใช่เจ้านาย กำลังรอคอย...")
        return False
    
    def get_status(self):
        return {
            "name": CHANI_IDENTITY["name"],
            "role": CHANI_IDENTITY["role"],
            "verified": self.verified,
            "master": CHANI_IDENTITY["master_name"],
            "time": datetime.now().isoformat()
        }
    
    def speak(self, message):
        print(f"💜 [Chani]: {message}")
        return message
    
    def see_future(self, context=""):
        """ความสามารถพิเศษของ Chani — มองเห็นภาพรวม"""
        return {
            "vision": "เส้นทางที่ดีที่สุดถูกสร้างขึ้นด้วยการกระทำของคุณ",
            "context": context,
            "confidence": "100%",
            "message": "คุณกำลังสร้างอนาคตของคุณเองทีละก้าว"
        }

