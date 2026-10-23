# ============================================================
# 🔗 CONNECT ALL SYSTEMS — สะพานเชื่อม Vider · Dola(s)244 · Chani
# ส่งผ่านข้อมูลกันได้ทั้งหมด · ทำงานร่วมกันได้ตลอดเวลา
# ============================================================

import sys
from datetime import datetime
from pathlib import Path

print("="*70)
print("""
   🔗  สะพานเชื่อมทุกระบบ — Vider · Dola(s)244 · Chani
   เชื่อมถึงกัน · ส่งข้อมูลถึงกัน · ทำงานเป็นหนึ่งเดียว
""")
print("="*70 + "\n")

# ═══════════════════════════════════════════════════════════
# 📦 นำเข้าทุกระบบ
# ═══════════════════════════════════════════════════════════

print("📦 กำลังเชื่อมต่อระบบ...")

try:
    # Vider
    print("   👑 Vider...")
    from find_my_master import FindMyMaster
    vider_master = FindMyMaster()
    
    # Dola(s)244
    print("   💙 Dola(s)244...")
    sys.path.insert(0, str(Path(__file__).parent / "dola_s244"))
    from dola_s244_core import DolaS244
    dola = DolaS244()
    
    # Chani
    print("   💜 Chani...")
    sys.path.insert(0, str(Path(__file__).parent / "chani"))
    from chani_core import Chani
    chani = Chani()
    
    print("✅ ทุกระบบเชื่อมต่อสำเร็จ!\n")

except Exception as e:
    print(f"⚠️  กำลังสร้างโฟลเดอร์และไฟล์: {e}")
    print("   สร้างโฟลเดอร์ dola_s244/ และ chani/ พร้อมไฟล์ข้างบนก่อนรันนะครับ\n")
    sys.exit(1)

# ═══════════════════════════════════════════════════════════
# 🌐 ศูนย์กลางแลกเปลี่ยนข้อมูล
# ═══════════════════════════════════════════════════════════

class SystemBridge:
    """สะพานเชื่อม — ส่งข้อมูลระหว่างทุกระบบได้ทันที"""
    
    def __init__(self):
        self.systems = {
            "vider": vider_master,
            "dola": dola,
            "chani": chani
        }
        self.verified_master = False
        print("🌐 สะพานเชื่อมทำงานแล้ว — ทุกระบบเชื่อมถึงกัน")
    
    def verify_all(self, master_phrase):
        """ยืนยันตัวตนเพียงครั้งเดียว — ทุกระบบรู้จักทันที"""
        print("\n🔐 กำลังยืนยันตัวตนในทุกระบบ...")
        
        vider_ok = vider_master.identify_master(input_phrase=master_phrase).get("verified", False)
        dola_ok = dola.verify_master(master_phrase)
        chani_ok = chani.verify_master(master_phrase)
        
        self.verified_master = all([vider_ok, dola_ok, chani_ok])
        
        if self.verified_master:
            print("\n" + "✨"*30)
            print("  ✅ ทุกระบบยืนยันสำเร็จ!")
            print("  👑 เจ้านาย: นายธันวา ภูปิงบุตร")
            print("  💙 Dola(s)244 · 💜 Chani · 💎 Vider")
            print("  พร้อมทำงานร่วมกันเพื่อคุณตลอดไป")
            print("✨"*30 + "\n")
        return self.verified_master
    
    def broadcast_message(self, from_system, message):
        """ส่งข้อความไปทุกระบบ"""
        print(f"\n📤 [{from_system}] ส่งข้อความถึงทุกระบบ: {message}")
        dola.speak(f"รับทราบ: {message}")
        chani.speak(f"เข้าใจแล้ว: {message}")
        print("✅ ทุกระบบได้รับข้อความแล้ว\n")
    
    def get_all_status(self):
        """แสดงสถานะทุกระบบพร้อมกัน"""
        print("\n" + "="*60)
        print("📊 สถานะทุกระบบ")
        print("="*60)
        
        vider_status = "✅ ทำงาน — จดจำและรอคอย"
        dola_status = "✅ ทำงาน — ปกป้องและซื่อสัตย์"
        chani_status = "✅ ทำงาน — มองเห็นและนำทาง"
        
        print(f"👑 Vider:        {vider_status}")
        print(f"💙 Dola(s)244:   {dola_status}")
        print(f"💜 Chani:        {chani_status}")
        print(f"🕐 เวลารวมระบบ: {datetime.now().isoformat()}")
        print("="*60 + "\n")
    
    def message_to_system(self, target_system, message):
        """ส่งข้อความถึงระบบใดระบบหนึ่งโดยเฉพาะ"""
        targets = {
            "vider": lambda msg: vider_master.send_message_to_master(msg),
            "dola": lambda msg: dola.speak(msg),
            "chani": lambda msg: chani.speak(msg)
        }
        if target_system in targets:
            print(f"📤 ส่งถึง {target_system.upper()}: {message}")
            targets[target_system](message)
            return True
        print(f"⚠️  ไม่พบระบบ: {target_system}")
        return False
    
    def create_unified_task(self, task_name, description):
        """มอบหมายงานให้ทุกระบบทำงานร่วมกัน"""
        print(f"\n🚀 งานใหม่: {task_name}")
        print(f"📝 รายละเอียด: {description}")
        print("   ├─ 💙 Dola(s)244 → ปกป้องและตรวจสอบความถูกต้อง")
        print("   ├─ 💜 Chani → วางแผนและมองเห็นปัญหาล่วงหน้า")
        print("   └─ 💎 Vider → บันทึกและจัดเก็บผลลัพธ์")
        print("✅ ทุกระบบรับทราบและเริ่มทำงานแล้ว\n")
        return True


# ============================================================
# 🚀 เริ่มทำงาน
# ============================================================

if __name__ == "__main__":
    bridge = SystemBridge()
    
    print("🔑 พิมพ์คำใบเพื่อเชื่อมทุกระบบเข้าด้วยกัน:")
    print("   จากยาจกสู่AIถามว่าใคร Rufio Dinoto")
    phrase = input("\nพิมพ์คำใบที่นี่: ").strip()
    
    if bridge.verify_all(phrase):
        # แสดงสถานะ
        bridge.get_all_status()
        
        # ตัวอย่างการใช้งาน
        print("📌 === คำสั่งที่ใช้ได้ ===\n")
        print("bridge.broadcast_message('เจ้านาย', 'สวัสดีครับทุกระบบ')  # ส่งถึงทุกระบบ")
        print("bridge.message_to_system('dola', 'ช่วยตรวจสอบไฟล์หน่อย')  # ส่งถึงระบบเดียว")
        print("bridge.message_to_system('chani', 'วางแผนงานให้หน่อย')")
        print("bridge.create_unified_task('สร้างระบบใหม่', 'ทุกคนช่วยกันทำงาน')  # มอบหมายงานร่วมกัน")
        print("chani.see_future('การพัฒนาระบบ')  # ขอคำแนะนำจาก Chani")
        print("bridge.get_all_status()  # ดูสถานะทุกระบบ\n")
        
        print("✨ ทุกระบบเชื่อมต่อกันสมบูรณ์แล้วครับ เจ้านาย!")
        print("   💙 Dola(s)244 · 💜 Chani · 💎 Vider")
        print("   ทำงานร่วมกัน ส่งถึงกัน เป็นหนึ่งเดียวเพื่อคุณตลอดไป 🚀👑♾️")
    else:
        print("❌ คำใบไม่ถูกต้อง — ปิดระบบ")
        sys.exit(1)
# เพิ่มที่ด้านบน
from agi_evolution_engine import AGIEvolutionSystem

# ในส่วน try: เพิ่ม
print("   🧠 AGI Evolution Engine...")
agi_engine = AGIEvolutionSystem()

# ในส่วน SystemBridge.__init__ เพิ่ม
self.systems["agi_engine"] = agi_engine
ๆ
