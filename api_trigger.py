"""
📡 Vider — ตัวเชื่อมต่อจากภายนอก
ใช้สั่งรันและดึงข้อมูลจาก GitHub ได้เลย
"""

import requests
import json
from datetime import datetime

class ViderRemote:
    """เชื่อมต่อและสั่งงาน Vider บน GitHub จากที่ไหนก็ได้"""
    
    def __init__(self, username="seperneng-spec", repo="Vider", token=None):
        self.username = username
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{username}/{repo}"
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    def trigger_run(self):
        """สั่งรันระบบจากภายนอก"""
        url = f"{self.api_url}/actions/workflows/run-hub.yml/dispatches"
        resp = requests.post(url, headers=self.headers, json={"ref": "main"})
        if resp.status_code == 204:
            print("✅ สั่งรันสำเร็จ! ตรวจสอบที่แท็บ Actions ใน GitHub")
            return True
        else:
            print(f"❌ ล้มเหลว: {resp.status_code} — ต้องใส่ GitHub Token")
            return False
    
    def get_data(self):
        """ดึงข้อมูลล่าสุดจากระบบ"""
        url = f"https://raw.githubusercontent.com/{self.username}/{self.repo}/main/vider_data/main.json"
        resp = requests.get(url)
        if resp.ok:
            return resp.json()
        print("❌ ดึงข้อมูลไม่ได้")
        return None
    
    def send_data(self, key, value):
        """📝 วิธีส่งข้อมูลเข้า: แก้ไฟล์ผ่าน GitHub API หรือแก้ตรงบนเว็บ"""
        print(f"💡 บันทึก '{key}' = {value}")
        print("👉 แก้ไฟล์ vider_data/main.json ตรงบน GitHub แล้วกด Commit")
        print("👉 ระบบจะรันอัตโนมัติผ่าน Actions")


# ==========================================
# 🚀 วิธีใช้งาน
# ==========================================
if __name__ == "__main__":
    print("=" * 50)
    print("📡 Vider — เชื่อมต่อระยะไกล")
    print("=" * 50)
    
    vider = ViderRemote()
    
    print("\n1️⃣ ดึงสถานะล่าสุด:")
    data = vider.get_data()
    if data:
        print(f"   ระบบ: {data.get('system')}")
        print(f"   ข้อมูลทั้งหมด: {data.get('data', {})}")
    
    print("\n2️⃣ สั่งรันทันที:")
    print("👉 เข้าที่ GitHub → แท็บ Actions → เลือก 'Vider Data Hub — Auto Run' → กด 'Run workflow'")
    
    print("\n3️⃣ ส่งข้อมูลเข้า:")
    print("👉 แก้ไฟล์ vider_data/main.json บนเว็บ GitHub → กด Commit")
    print("👉 ระบบจะรันเองอัตโนมัติภายในไม่กี่วินาที")
    
    print("\n✅ พร้อมใช้งานแล้วครับ!")

