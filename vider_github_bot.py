# -*- coding: utf-8 -*-
"""
==================================================
🤖 VIDER GITHUB BOT — เชื่อมต่อและควบคุม GitHub ผ่านแชท
เวอร์ชัน: 1.0.0
เจ้าของ: นายธันวา ภูปิงบุตร
ฟังก์ชัน: สร้างไฟล์ → บันทึก → อัปโหลดขึ้น GitHub อัตโนมัติ
==================================================
"""

__version__ = "1.0.0"

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# ==================================================
# 🔐 ตั้งค่าระบบ — แก้ไขข้อมูลของคุณที่นี่
# ==================================================
CONFIG = {
    "REPO_URL": "https://github.com/seperneng-spec/Vider.git",
    "REPO_FOLDER": "./Vider",
    "GIT_NAME": "นายธันวา ภูปิงบุตร",
    "GIT_EMAIL": "your-email@example.com",  # ใส่อีเมลที่ใช้กับ GitHub
}

# ==================================================
# 🤖 ระบบทำงานหลัก
# ==================================================
class ViderGitHubBot:
    """Vider เชื่อมต่อ GitHub — สร้างไฟล์และอัปโหลดอัตโนมัติ"""

    def __init__(self):
        self.repo_path = Path(CONFIG["REPO_FOLDER"])
        print("=" * 60)
        print("🤖 VIDER GITHUB BOT — พร้อมทำงาน")
        print(f"📂 รีโปเป้าหมาย: {CONFIG['REPO_URL']}")
        print("=" * 60 + "\n")
        self._init_git()

    def _init_git(self):
        """ตรวจสอบและตั้งค่า Git"""
        if not self.repo_path.exists():
            print("📥 กำลังโคลนรีโปจาก GitHub...")
            subprocess.run(
                ["git", "clone", CONFIG["REPO_URL"], str(self.repo_path)],
                capture_output=True, text=True
            )
        os.chdir(self.repo_path)
        
        # ตั้งชื่อและอีเมลถ้ายังไม่มี
        subprocess.run(
            ["git", "config", "--global", "user.name", CONFIG["GIT_NAME"]],
            capture_output=True
        )
        subprocess.run(
            ["git", "config", "--global", "user.email", CONFIG["GIT_EMAIL"]],
            capture_output=True
        )
        print("✅ เชื่อมต่อกับรีโปเรียบร้อยแล้ว\n")

    # ==============================================
    # 📝 สร้าง/แก้ไขไฟล์
    # ==============================================
    def create_file(self, filename, content, description=""):
        """
        สร้างไฟล์ใหม่
        :param filename: ชื่อไฟล์ เช่น test.py
        :param content: เนื้อหาในไฟล์
        :param description: คำอธิบายไฟล์
        """
        try:
            filepath = self.repo_path / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ สร้างไฟล์: {filename}")
            if description:
                print(f"📝 รายละเอียด: {description}")
            return True
        except Exception as e:
            print(f"❌ สร้างไฟล์ไม่ได้: {e}")
            return False

    # ==============================================
    # 📤 อัปโหลดขึ้น GitHub
    # ==============================================
    def push_to_github(self, message="อัปเดตผ่าน Vider GitHub Bot"):
        """
        อัปโหลดไฟล์ทั้งหมดขึ้น GitHub
        :param message: ข้อความคอมมิต
        """
        print("\n📤 กำลังอัปโหลดขึ้น GitHub...")
        
        try:
            # 1. ดูสถานะ
            status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            if not status.stdout.strip():
                print("⚠️ ไม่มีไฟล์ที่เปลี่ยนแปลง")
                return False
            
            # 2. เพิ่มไฟล์ทั้งหมด
            subprocess.run(["git", "add", "."], check=True)
            print("   ✅ เพิ่มไฟล์ทั้งหมด")
            
            # 3. คอมมิต
            commit_msg = f"{message} — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True)
            print(f"   ✅ บันทึก: {commit_msg}")
            
            # 4. ส่งขึ้น
            subprocess.run(["git", "push"], check=True)
            print("   ✅ อัปโหลดสำเร็จ!")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ ผิดพลาด: {e}")
            return False

    # ==============================================
    # 📋 ดูรายการไฟล์
    # ==============================================
    def list_files(self):
        """แสดงรายการไฟล์ในรีโป"""
        print("\n📁 รายการไฟล์ในรีโป:")
        for f in sorted(self.repo_path.glob("*")):
            if not f.name.startswith('.'):
                kind = "📂" if f.is_dir() else "📄"
                print(f"   {kind} {f.name}")

    # ==============================================
    # 💬 โหมดแชท — สั่งงานง่ายๆ
    # ==============================================
    def chat_mode(self):
        """โหมดแชท: พิมพ์สั่งงานได้เลย"""
        print("""
💬 === โหมดสั่งงานด้วยข้อความ ===

📝 สร้างไฟล์:
  สร้างไฟล์ ชื่อไฟล์.py
  เนื้อหา...
  จบไฟล์

📤 อัปโหลดทั้งหมด:
  อัปโหลด ข้อความคอมมิต

📋 ดูรายการไฟล์:
  ดูไฟล์

❌ ออกจากระบบ:
  ออก
""")
        while True:
            try:
                cmd = input("\n🤖 Vider> ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\n👑 ลาก่อนครับ!")
                break
            
            if not cmd:
                continue
            
            # ออกจากระบบ
            if cmd in ["ออก", "exit", "quit", "จบ"]:
                print("👑 ปิดระบบแล้วครับ")
                break
            
            # ดูไฟล์
            if cmd in ["ดูไฟล์", "ls", "ไฟล์"]:
                self.list_files()
                continue
            
            # อัปโหลด
            if cmd.startswith("อัปโหลด"):
                msg = cmd[7:].strip() or "อัปเดตผ่าน Vider"
                self.push_to_github(msg)
                continue
            
            # สร้างไฟล์
            if cmd.startswith("สร้างไฟล์"):
                filename = cmd[9:].strip()
                if not filename:
                    print("⚠️  พิมพ์: สร้างไฟล์ ชื่อไฟล์.py")
                    continue
                print(f"📝 พิมพ์เนื้อหาไฟล์ — พิมพ์ 'จบไฟล์' เมื่อเสร็จ")
                lines = []
                while True:
                    line = input("│ ")
                    if line == "จบไฟล์":
                        break
                    lines.append(line)
                content = "\n".join(lines)
                self.create_file(filename, content)
                continue
            
            print("⚠️ ไม่เข้าใจคำสั่ง ลองใหม่อีกครั้งนะครับ")


# ==================================================
# 🚀 เริ่มทำงาน
# ==================================================
if __name__ == "__main__":
    bot = ViderGitHubBot()
    bot.chat_mode()

