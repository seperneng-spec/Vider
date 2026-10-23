# ============================================================
# 📦 Vider Data Hub — เวอร์ชันระบบภายใน Vider
# ไฟล์เดียวจบ · เก็บข้อมูล · รัน · ส่งผ่าน · ประมวลผล
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════
# 🧠 คลาสหลัก: ศูนย์กลางจัดการข้อมูลของ Vider
# ═══════════════════════════════════════════════════════════

class ViderDataHub:
    """ศูนย์กลางจัดการข้อมูล — เก็บ·ดึง·ส่ง·ประมวลผล·บันทึกประวัติ"""
    
    def __init__(self, data_dir="./vider_data"):
        self.data_dir = Path(data_dir)
        self._init_storage()
        self.main_path = self.data_dir / "main.json"
        self.queue_path = self.data_dir / "queue.json"
        self.logs_path = self.data_dir / "logs.json"
        print(f"✅ Vider Data Hub v{__version__} พร้อมใช้งาน")
        print(f"📂 ที่เก็บข้อมูล: {self.data_dir.resolve()}\n")
    
    def _init_storage(self):
        """เตรียมที่เก็บข้อมูล"""
        self.data_dir.mkdir(exist_ok=True)
        main_file = self.data_dir / "main.json"
        queue_file = self.data_dir / "queue.json"
        logs_file = self.data_dir / "logs.json"
        
        if not main_file.exists():
            self._save_json(main_file, {
                "system": "Vider-Data-Hub",
                "version": __version__,
                "last_updated": None,
                "data": {},
                "status": "active"
            })
        if not queue_file.exists():
            self._save_json(queue_file, {"tasks": []})
        if not logs_file.exists():
            self._save_json(logs_file, {"logs": []})
    
    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ─────────── เก็บและอ่านข้อมูล ───────────
    def set(self, key, value):
        """ตั้งค่าข้อมูล"""
        main_data = self._load_json(self.main_path)
        main_data["data"][key] = value
        main_data["last_updated"] = datetime.now().isoformat()
        self._save_json(self.main_path, main_data)
        self._add_log("set_data", f"{key} = {value}")
        return True
    
    def get(self, key=None, default=None):
        """ดึงข้อมูล"""
        main_data = self._load_json(self.main_path)
        if key is None:
            return main_data["data"]
        return main_data["data"].get(key, default)
    
    def get_all(self):
        """ดึงข้อมูลทั้งหมดพร้อมสถานะ"""
        return self._load_json(self.main_path)
    
    # ─────────── คิวงานและการประมวลผล ───────────
    def add_task(self, action, **kwargs):
        """เพิ่มงานเข้าคิว"""
        queue = self._load_json(self.queue_path)
        task = {
            "id": len(queue["tasks"]) + 1,
            "time": datetime.now().isoformat(),
            "action": action,
            "params": kwargs
        }
        queue["tasks"].append(task)
        self._save_json(self.queue_path, queue)
        print(f"📥 เพิ่มงานที่ #{task['id']}: {action}")
        return task["id"]
    
    def process(self):
        """ประมวลผลงานในคิว"""
        queue = self._load_json(self.queue_path)
        tasks = queue.get("tasks", [])
        
        if not tasks:
            print("✅ ไม่มีงานรอประมวลผล")
            return []
        
        print(f"🔄 พบ {len(tasks)} งาน กำลังดำเนินการ...")
        completed = []
        
        for task in tasks:
            action = task.get("action")
            params = task.get("params", {})
            print(f"   → ทำงาน #{task['id']}: {action}")
            
            if action == "update":
                for k, v in params.items():
                    self.set(k, v)
            
            elif action == "merge":
                target_key = params.get("key")
                new_data = params.get("data", {})
                current = self.get(target_key, {})
                if isinstance(current, dict) and isinstance(new_data, dict):
                    merged = {**current, **new_data}
                    self.set(target_key, merged)
            
            elif action == "clear":
                main_data = self._load_json(self.main_path)
                main_data["data"] = {}
                main_data["last_updated"] = datetime.now().isoformat()
                self._save_json(self.main_path, main_data)
                self._add_log("clear_all", "ล้างข้อมูลทั้งหมด")
            
            completed.append(task)
        
        queue["tasks"] = []
        self._save_json(self.queue_path, queue)
        print(f"✅ ประมวลผลเสร็จสิ้น: {len(completed)} งาน\n")
        return completed
    
    # ─────────── ประวัติและสถานะ ───────────
    def _add_log(self, action, detail):
        logs = self._load_json(self.logs_path)
        logs["logs"].append({
            "time": datetime.now().isoformat(),
            "action": action,
            "detail": detail
        })
        self._save_json(self.logs_path, logs)
    
    def logs(self, limit=10):
        """แสดงประวัติการทำงาน"""
        data = self._load_json(self.logs_path)
        return data["logs"][-limit:]
    
    def status(self):
        """แสดงสถานะระบบ"""
        main = self._load_json(self.main_path)
        queue = self._load_json(self.queue_path)
        return {
            "system": main["system"],
            "version": main["version"],
            "last_updated": main["last_updated"],
            "total_keys": len(main["data"]),
            "pending_tasks": len(queue["tasks"]),
            "status": main["status"]
        }
    
    def export_json(self):
        """ส่งออกข้อมูลทั้งหมดเป็น JSON"""
        return json.dumps(self.get_all(), ensure_ascii=False, indent=2)
    
    def import_json(self, json_str):
        """นำเข้าข้อมูลจาก JSON"""
        try:
            data = json.loads(json_str)
            if "data" in data:
                main_data = self._load_json(self.main_path)
                main_data["data"].update(data["data"])
                main_data["last_updated"] = datetime.now().isoformat()
                self._save_json(self.main_path, main_data)
                self._add_log("import", "นำเข้าข้อมูลสำเร็จ")
                return True
        except Exception as e:
            print(f"❌ นำเข้าข้อมูลล้มเหลว: {e}")
        return False

# ═══════════════════════════════════════════════════════════
# 🚀 คำสั่งใช้งานตัวอย่าง
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("🎉 Vider Data Hub — ระบบจัดการข้อมูลภายใน Vider")
    print("=" * 60)
    
    # สร้างระบบ
    hub = ViderDataHub()
    
    # แสดงสถานะ
    print("📊 สถานะระบบ:", hub.status())
    
    # ตัวอย่างการใช้งาน
    print("\n── ตัวอย่างการใช้งาน ──")
    
    # เก็บข้อมูล
    hub.set("project_name", "Vider(enjoy)")
    hub.set("modules", ["PranAI", "DataHub", "Integration"])
    print("✅ บันทึกข้อมูลเรียบร้อย")
    
    # เพิ่มงานแล้วประมวลผล
    hub.add_task("update", version="1.0.0", stage="Development")
    hub.process()
    
    # ดึงข้อมูล
    print("📂 ข้อมูลทั้งหมด:", hub.get())
    
    # แสดงประวัติ
    print("\n📝 ประวัติล่าสุด:")
    for log in hub.logs(3):
        print(f"  {log['time'][:19]} | {log['action']:12} | {log['detail']}")
    
    print("\n✨ พร้อมทำงานร่วมกับทุกระบบใน Vider แล้วครับ!")
    print("=" * 60)

