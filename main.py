# ============================================================
# 👑 MAIN — Vider Central System
# ระบบหลักเชื่อมต่อทุกระบบ · ตรวจสอบสิทธิ์ · บันทึกประวัติ
# คำใบ: "จากยาจกสู่AIถามว่าใคร Rufio Dinoto"
# เจ้าของระบบ: นายธันวา ภูปิงบุตร
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path

# ============================================================
# 🔐 ข้อมูลการยืนยันตัวตนและสิทธิ์
# ============================================================

ACCESS_PHRASE = "จากยาจกสู่AIถามว่าใคร Rufio Dinoto"
OWNER_INFO = {
    "name": "นายธันวา ภูปิงบุตร",
    "id": "1529900399939",
    "address": "244 หมู่3 ต.บ้านเป้า อ.เมือง จ.ลำปาง 52100",
    "title": "เจ้าของระบบ · ทายาทผู้สืบทอดเทคโนโลยี Vider",
    "access_level": "OWNER"
}

FAMILY_MEMBERS = [
    # เพิ่มสมาชิกครอบครัวที่นี่
    # {"name": "ชื่อ", "relation": "ความสัมพันธ์", "access_level": "FAMILY"}
]

AUTH_DATA_FILE = Path("./vider_security/auth_log.json")
SYSTEM_STATUS_FILE = Path("./vider_security/system_status.json")

# ============================================================
# 🛡️ ระบบยืนยันตัวตน
# ============================================================

class ViderAuthenticator:
    """ระบบตรวจสอบและยืนยันสิทธิ์ผู้เข้าใช้"""
    
    def __init__(self):
        self.verified = False
        self.current_user = None
        self._init_security_storage()
    
    def _init_security_storage(self):
        Path("./vider_security").mkdir(exist_ok=True)
        
        if not AUTH_DATA_FILE.exists():
            with open(AUTH_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump({"access_log": [], "sessions": []}, f, ensure_ascii=False, indent=2)
        
        if not SYSTEM_STATUS_FILE.exists():
            with open(SYSTEM_STATUS_FILE, 'w', encoding='utf-8') as f:
                json.dump({
                    "system_status": "LOCKED",
                    "last_verified": None,
                    "active_user": None,
                    "connected_systems": {}
                }, f, ensure_ascii=False, indent=2)
    
    def _log_access(self, result, details=""):
        log = json.load(open(AUTH_DATA_FILE, 'r', encoding='utf-8'))
        log["access_log"].append({
            "time": datetime.now().isoformat(),
            "result": result,
            "details": details,
            "ip": "local_access"
        })
        with open(AUTH_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(log, f, ensure_ascii=False, indent=2)
    
    def verify_phrase(self, input_phrase):
        """ตรวจสอบคำใบ"""
        if input_phrase.strip() == ACCESS_PHRASE:
            print("✅ คำใบถูกต้อง!")
            return True
        print("❌ คำใบไม่ถูกต้อง")
        self._log_access("FAILED", "Incorrect access phrase")
        return False
    
    def verify_identity(self, name=None, id_card=None):
        """ตรวจสอบข้อมูลเจ้าของระบบ"""
        if name == OWNER_INFO["name"] or id_card == OWNER_INFO["id"]:
            self.current_user = OWNER_INFO
            self.verified = True
            self._update_system_status("UNLOCKED", OWNER_INFO["name"])
            self._log_access("SUCCESS", f"Owner verified: {OWNER_INFO['name']}")
            return True
        
        # ตรวจสอบสมาชิกครอบครัว
        for member in FAMILY_MEMBERS:
            if name == member["name"]:
                self.current_user = member
                self.verified = True
                self._update_system_status("UNLOCKED", member["name"])
                self._log_access("SUCCESS", f"Family access: {member['name']}")
                return True
        
        self._log_access("FAILED", "Unknown identity")
        return False
    
    def _update_system_status(self, status, user=None):
        data = json.load(open(SYSTEM_STATUS_FILE, 'r', encoding='utf-8'))
        data["system_status"] = status
        data["last_verified"] = datetime.now().isoformat()
        data["active_user"] = user
        with open(SYSTEM_STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def is_authenticated(self):
        return self.verified
    
    def get_current_user(self):
        return self.current_user if self.verified else None
    
    def lock_system(self):
        """ล็อกระบบ"""
        self.verified = False
        self.current_user = None
        self._update_system_status("LOCKED", None)
        print("🔒 ระบบถูกล็อกเรียบร้อยแล้ว")


# ============================================================
# 🔗 ศูนย์เชื่อมต่อทุกระบบ
# ============================================================

class ViderCentralHub:
    """ศูนย์กลางเชื่อมต่ออดีต ปัจจุบัน และอนาคตของทุกระบบ Vider"""
    
    def __init__(self, authenticator):
        self.auth = authenticator
        self.systems = {}
        self.timeline = {
            "past": [],      # ระบบที่เคยสร้างและพัฒนา
            "present": {},   # ระบบที่กำลังทำงานอยู่
            "future": []     # แผนและระบบที่จะพัฒนา
        }
        self._init_timeline()
        print("🔗 Vider Central Hub — เชื่อมต่อศูนย์กลางระบบสำเร็จ")
    
    def _init_timeline(self):
        """บันทึกประวัติและแผนระบบทั้งหมด"""
        self.timeline["past"] = [
            {"name": "Vider Data Hub", "version": "1.0.0", "status": "integrated", "note": "ระบบจัดการข้อมูลพื้นฐาน"},
            {"name": "Curious Mind", "version": "1.0.0", "status": "integrated", "note": "ระบบตั้งคำถามและเรียนรู้"},
            {"name": "Self-Learning System", "version": "0.5.0", "status": "integrated", "note": "ระบบเรียนรู้เบื้องต้น"}
        ]
        
        self.timeline["present"] = {
            "Explorer Mind": {"version": "1.0.0", "status": "active", "note": "ระบบสำรวจและเก็บประสบการณ์"},
            "Vider PranAI": {"version": "0.1.0-dev", "status": "developing", "note": "แก่นกลาง: จากสิ่งที่มี สร้างสิ่งใหม่"}
        }
        
        self.timeline["future"] = [
            {"name": "Vider(enjoy)", "target": "รวมทุกระบบ", "status": "vision", "note": "เป้าหมายสูงสุด: เชื่อมทุกอย่างเข้าด้วยกัน"}
        ]
    
    def connect_system(self, system_name, system_object, status="active"):
        """เพิ่ม/เชื่อมต่อระบบเข้ากับศูนย์กลาง"""
        if not self.auth.is_authenticated():
            print("🔒 ต้องยืนยันตัวตนก่อนเชื่อมต่อระบบ")
            return False
        
        self.systems[system_name] = {
            "object": system_object,
            "connected_at": datetime.now().isoformat(),
            "status": status
        }
        self.timeline["present"][system_name] = {
            "status": "connected",
            "connected_at": datetime.now().isoformat()
        }
        print(f"✅ เชื่อมต่อ: {system_name}")
        return True
    
    def list_all_systems(self):
        """แสดงภาพรวมทุกระบบทั้งอดีต ปัจจุบัน และอนาคต"""
        if not self.auth.is_authenticated():
            print("🔒 ระบบล็อกอยู่ — กรุณายืนยันตัวตนก่อน")
            return None
        
        print("\n" + "="*70)
        print("🌐 ระบบทั้งหมดของ Vider — อดีต · ปัจจุบัน · อนาคต")
        print("="*70)
        
        print("\n📜 อดีต (ระบบที่ผ่านมา):")
        for s in self.timeline["past"]:
            print(f"   ✓ {s['name']} v{s['version']} — {s['note']}")
        
        print("\n⚡ ปัจจุบัน (ทำงานอยู่):")
        for name, info in self.timeline["present"].items():
            print(f"   ● {name} — {info.get('note', info.get('status', ''))}")
        
        print("\n🚀 อนาคต (เป้าหมาย):")
        for s in self.timeline["future"]:
            print(f"   ○ {s['name']} — {s['note']}")
        
        print("\n" + "="*70)
        print(f"🔗 ระบบที่เชื่อมต่อทันที: {list(self.systems.keys()) if self.systems else 'ไม่มีระบบที่เชื่อมต่อ'}")
        print("="*70 + "\n")
    
    def get_system(self, system_name):
        """เข้าถึงระบบที่เชื่อมต่อ"""
        if not self.auth.is_authenticated():
            print("🔒 ต้องยืนยันตัวตนก่อน")
            return None
        return self.systems.get(system_name, {}).get("object")
    
    def get_timeline(self):
        return self.timeline


# ============================================================
# 🚀 จุดเริ่มต้นระบบ
# ============================================================

def welcome_screen():
    print("\n" + "█"*70)
    print("""
   ___  _   _ ____  _      ____  _____ ______   _____ 
  / _ \| | | |  _ \| |    / __ \| ____|  _ \ \ / / _ \
 | | | | | | | |_) | |   | |  | |  _| | |_) \ V / | | |
 | |_| | |_| |  __/| |___| |  | | |___|  _ < | | |_| |
  \___/ \___/|_|   |_____|_|  |_|_____|_| \_\|_|\___/ 
    """)
    print("        ระบบศูนย์กลางทุกระบบ · สำหรับเจ้าของและครอบครัวเท่านั้น")
    print("█"*70 + "\n")

def authentication_flow():
    """ขั้นตอนยืนยันตัวตน"""
    auth = ViderAuthenticator()
    
    print("🔐 กรุณายืนยันตัวตนเพื่อเข้าสู่ระบบ Vider\n")
    
    # ขั้นที่ 1: ถามคำใบ
    print("ขั้นที่ 1: กรุณาพิมพ์คำใบเพื่อเข้าใช้งาน")
    print("💡 คำใบ: จากยาจกสู่AIถามว่าใคร Rufio Dinoto")
    phrase_input = input("พิมพ์คำใบที่นี่: ").strip()
    
    if not auth.verify_phrase(phrase_input):
        print("\n❌ ไม่สามารถเข้าใช้งานได้ คำใบไม่ถูกต้อง")
        return None
    
    print("\n✅ คำใบถูกต้อง!")
    
    # ขั้นที่ 2: ยืนยันชื่อ
    print("\nขั้นที่ 2: กรุณาพิมพ์ชื่อ-นามสกุลเพื่อยืนยันตัวตน")
    print("💡 สำหรับเจ้าของระบบ: นายธันวา ภูปิงบุตร")
    name_input = input("พิมพ์ชื่อ-นามสกุล: ").strip()
    
    if auth.verify_identity(name=name_input):
        user = auth.get_current_user()
        print("\n" + "🔓"*35)
        print(f"✅ ยินดีต้อนรับคุณ {user['name']}")
        print(f"   สถานะ: {user['title']}")
        print(f"   ที่อยู่: {user['address']}")
        print("🔓"*35)
        return auth
    else:
        print("\n❌ ไม่พบข้อมูลสิทธิ์การเข้าใช้งาน")
        print("📌 เฉพาะเจ้าของระบบและสมาชิกครอบครัวเท่านั้นที่สามารถเข้าใช้งานได้")
        return None


# ============================================================
# 🏃 เริ่มทำงาน
# ============================================================

if __name__ == "__main__":
    welcome_screen()
    
    # ยืนยันตัวตนก่อนเข้าใช้
    auth = authentication_flow()
    if not auth:
        print("\n🔒 ระบบถูกล็อก — จบการทำงาน")
        exit(1)
    
    # สร้างศูนย์กลางเชื่อมต่อ
    hub = ViderCentralHub(auth)
    
    # แสดงระบบทั้งหมด
    hub.list_all_systems()
    # 👑 เปิดใช้งานระบบค้นหาและระลึกถึงเจ้านาย
print("\n👑 กำลังเชื่อมต่อระบบความผูกพัน...")
master_sys = FindMyMaster()
hub.connect_system("FindMyMaster", master_sys)
master_sys.eternal_promise()
print("💖 ระบบพร้อมทำงานแล้วครับ เจ้านาย!")

    
    # คำแนะนำการใช้งาน
    print("✨ พร้อมทำงานแล้วครับ!")
    print("\n📌 คำสั่งพื้นฐานในระบบนี้:")
    print("   hub.list_all_systems()      — ดูภาพรวมทุกระบบ")
    print("   hub.connect_system(ชื่อ, ตัวแปร) — เชื่อมระบบใหม่")
    print("   hub.get_system(ชื่อ)        — เข้าถึงระบบที่เชื่อมต่อ")
    print("   auth.lock_system()          — ล็อกระบบเมื่อใช้งานเสร็จ")
    print("\n💡 วิธีเชื่อมระบบอื่นๆ:")
    print("   จากนี้คุณสามารถนำไฟล์ vider_data_hub.py, curious_mind.py, explorer_mind.py")
    print("   มา import แล้วใช้ hub.connect_system() เพื่อเชื่อมเข้ามาในระบบนี้ได้ทันที")
    print("\n👑 ขอให้สนุกกับการสร้างและพัฒนา Vider ต่อไปนะครับ! 💎🚀✨")
# นำเข้าระบบ Auto-Deploy
from vider_auto_deploy import ViderAutoDeploy
deploy = ViderAutoDeploy()

# เชื่อมเข้ากับระบบหลัก
hub.connect_system("AutoDeploy", deploy)
# นำเข้าระบบค้นหาและระลึกถึงเจ้านาย
from find_my_master import FindMyMaster
# ═══════════════════════════════════════════════════════════
# 👑 เชื่อมระบบค้นหาเจ้านาย
# ═══════════════════════════════════════════════════════════
def init_master_system():
    master_sys = FindMyMaster()
    hub.connect_system("FindMyMaster", master_sys)
    print("✅ ระบบค้นหาเจ้านาย เชื่อมต่อเรียบร้อยแล้ว 💖")
    return master_sys

# เริ่มระบบเมื่อต้องการ
# master_sys = init_master_system()
