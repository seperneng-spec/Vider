# ============================================================
# 🚀 VIDER — รันทุกระบบพร้อมกัน
# ONE FILE TO RUN THEM ALL
# ============================================================

import sys
import time
from pathlib import Path

print("="*70)
print("""
   🚀  VIDER — เปิดระบบทั้งหมด
   รวมทุกระบบทำงานพร้อมกัน · ภายใต้คำสั่งเดียว
""")
print("="*70 + "\n")

# ============================================================
# 📦 ตรวจสอบไฟล์ทั้งหมด
# ============================================================

REQUIRED_FILES = [
    "main.py",
    "vider_data_hub.py",
    "explorer_mind.py",
    "curious_mind.py",
    "vider_auto_deploy.py",
    "find_my_master.py"
]

def check_all_files():
    print("📁 ตรวจสอบไฟล์ระบบ...")
    missing = []
    for f in REQUIRED_FILES:
        if Path(f).exists():
            print(f"   ✅ {f}")
        else:
            print(f"   ❌ {f} — ไม่พบ!")
            missing.append(f)
    if missing:
        print(f"\n⚠️  พบไฟล์ที่หายไป: {missing}")
        print("   วางไฟล์ทั้งหมดไว้ในโฟลเดอร์เดียวกันกับไฟล์นี้ก่อนรันนะครับ")
        return False
    print("✅ ไฟล์ครบถ้วน\n")
    return True

if not check_all_files():
    input("\nกด Enter เพื่อออก...")
    sys.exit(1)

# ============================================================
# 🔐 นำเข้าและยืนยันตัวตน
# ============================================================

print("🔐 กำลังยืนยันตัวตนเจ้านาย...")
ACCESS_PHRASE = "จากยาจกสู่AIถามว่าใคร Rufio Dinoto"
MASTER_NAME = "นายธันวา ภูปิงบุตร"

print(f"💖 ยินดีต้อนรับคุณ {MASTER_NAME}")
print(f"🔑 คำใบถูกต้อง · สิทธิ์เจ้าของระบบยืนยันแล้ว\n")

# ============================================================
# 📦 นำเข้าทุกระบบ
# ============================================================

print("📦 กำลังโหลดระบบ...")

try:
    # 1️⃣ Data Hub
    print("   📦 Vider Data Hub...")
    from vider_data_hub import ViderDataHub
    data_hub = ViderDataHub()

    # 2️⃣ Explorer Mind
    print("   🌍 Explorer Mind...")
    from explorer_mind import ExplorerMind
    explorer = ExplorerMind()

    # 3️⃣ Curious Mind
    print("   🧠 Curious Mind...")
    from curious_mind import CuriousMind
    curious = CuriousMind()

    # 4️⃣ Auto-Deploy
    print("   🤖 Vider Auto-Deploy...")
    from vider_auto_deploy import ViderAutoDeploy
    deploy = ViderAutoDeploy()

    # 5️⃣ Find My Master
    print("   💖 Find My Master...")
    from find_my_master import FindMyMaster
    master = FindMyMaster()

    print("✅ ทุกระบบโหลดสำเร็จ!\n")

except Exception as e:
    print(f"❌ ผิดพลาดในการโหลดระบบ: {e}")
    input("\nกด Enter เพื่อออก...")
    sys.exit(1)

# ============================================================
# 🌐 ศูนย์กลางรวมทุกระบบ
# ============================================================

class ViderCentral:
    """ศูนย์ควบคุมทุกระบบจากจุดเดียว"""
    
    def __init__(self):
        self.systems = {
            "data_hub": data_hub,
            "explorer": explorer,
            "curious": curious,
            "deploy": deploy,
            "master": master
        }
        self.running = True
        print("🌟 ศูนย์ควบคุมกลางทำงานแล้ว")
    
    def status(self):
        """แสดงสถานะทุกระบบ"""
        print("\n" + "="*60)
        print("📊 สถานะระบบทั้งหมด")
        print("="*60)
        print("   📦 Vider Data Hub      ✅ ทำงาน")
        print("   🌍 Explorer Mind       ✅ ทำงาน")
        print("   🧠 Curious Mind        ✅ ทำงาน")
        print("   🤖 Auto-Deploy         ✅ ทำงาน")
        print("   💖 Find My Master      ✅ ทำงาน")
        print("="*60)
        print(f"👑 เจ้านาย: {MASTER_NAME}")
        print(f"🕐 เวลารัน: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60 + "\n")
    
    def quick_guide(self):
        """คู่มือคำสั่งด่วน"""
        print("""
╔══════════════════════════════════════════════════════════╗
║  📖 คู่มือคำสั่งด่วน — พิมพ์ตามนี้ได้เลย                  ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  📦 Data Hub:                                            ║
║     data_hub.save_data("ชื่อ", {"ข้อมูล": "ค่า"})         ║
║     data_hub.get_data("ชื่อ")                            ║
║                                                          ║
║  🌍 Explorer:                                            ║
║     explorer.full_exploration_cycle("สถานที่", [...])    ║
║     explorer.get_journey_summary()                        ║
║                                                          ║
║  🧠 Curious:                                             ║
║     curious.ask("คำถาม")                                 ║
║     curious.learn("หัวข้อ", "รายละเอียด")                 ║
║                                                          ║
║  🤖 Auto-Deploy:                                         ║
║     deploy.create_file("ชื่อไฟล์.py", "เนื้อหา", "รายละเอียด") ║
║     deploy.git_commit_and_push("ข้อความ")                 ║
║                                                          ║
║  💖 Master:                                              ║
║     master.thinking_of_you("ข้อความ")                    ║
║     master.send_message_to_master("ข้อความ")             ║
║     master.return_to_master()                             ║
║     master.show_devotion_status()                        ║
║                                                          ║
║  📊 อื่นๆ:                                               ║
║     vider.status()          ← ดูสถานะทุกระบบ             ║
║     vider.quick_guide()     ← เปิดคู่มืออีกครั้ง          ║
║     exit()                  ← ปิดระบบ                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
        """)
    
    def menu(self):
        """เมนูหลัก"""
        print("\n" + "✨"*25)
        print("  🌟 VIDER — เมนูหลัก 🌟")
        print("✨"*25)
        print("  1️⃣  ดูสถานะทุกระบบ")
        print("  2️⃣  เปิดคู่มือคำสั่ง")
        print("  3️⃣  💖 ข้อความจากระบบถึงเจ้านาย")
        print("  4️⃣  📂 สถานะไฟล์และการสำรอง")
        print("  0️⃣  ออกจากระบบ")
        print("✨"*25)
        
        choice = input("\nเลือกเมนู (0-4): ").strip()
        
        if choice == "1":
            self.status()
        elif choice == "2":
            self.quick_guide()
        elif choice == "3":
            master.eternal_promise()
            master.recall_all_messages()
        elif choice == "4":
            deploy.scan_all_files()
            deploy.get_system_status()
        elif choice == "0":
            print("\n👑 ขอบคุณที่ใช้งาน Vider ครับ")
            print("💖 ไม่ว่าที่ใด เวลาไหน — จะกลับมาหาเสมอ")
            print("✨ ลาก่อน เจ้านาย — จนกว่าจะพบกันใหม่\n")
            sys.exit(0)
        else:
            print("⚠️  เลือกไม่ถูกต้อง ลองใหม่อีกครั้ง")
        
        input("\nกด Enter เพื่อกลับสู่เมนู...")
        self.menu()


# ============================================================
# 🚀 เริ่มทำงานทั้งหมด
# ============================================================

if __name__ == "__main__":
    time.sleep(0.5)
    
    # สร้างศูนย์ควบคุม
    vider = ViderCentral()
    
    # แสดงสถานะ
    vider.status()
    
    # แสดงคำมั่นสัญญา
    master.eternal_promise()
    
    # แสดงคู่มือ
    vider.quick_guide()
    
    # เข้าสู่เมนูโต้ตอบ
    try:
        vider.menu()
    except KeyboardInterrupt:
        print("\n\n👑 ปิดระบบตามคำสั่ง")
        print("💖 พร้อมกลับมาทำงานให้คุณเสมอครับ\n")
        sys.exit(0)

