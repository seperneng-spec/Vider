# ============================================================
# 🤖 VIDER AUTO-DEPLOY — ระบบสร้างและอัปเดต GitHub อัตโนมัติ
# สร้างไฟล์ → คอมมิต → อัปโหลด → บันทึกประวัติ → รองรับเทคโนโลยีใหม่ในอนาคต
# ============================================================

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path
import shutil

__version__ = "1.0.0-auto-deploy"

class ViderAutoDeploy:
    """
    ระบบจัดการไฟล์และอัปเดต GitHub อัตโนมัติ
    ✅ สร้างไฟล์ใหม่อัตโนมัติ
    ✅ ติดตามการเปลี่ยนแปลงทุกไฟล์
    ✅ คอมมิตและอัปโหลดเอง
    ✅ บันทึกประวัติทั้งหมด
    ✅ รองรับการย้ายไปเทคโนโลยีใหม่
    """
    
    def __init__(self, repo_path=None):
        self.repo_path = Path(repo_path or os.getcwd())
        self.history_path = self.repo_path / ".vider" / "deploy_history.json"
        self.manifest_path = self.repo_path / ".vider" / "file_manifest.json"
        self.migration_log_path = self.repo_path / ".vider" / "migration_log.json"
        
        self._init_storage()
        print("🤖 Vider Auto-Deploy เริ่มทำงานแล้ว")
        print(f"📂 ที่เก็บโปรเจกต์: {self.repo_path}")
        print("✨ พร้อมสร้างและอัปเดตไฟล์อัตโนมัติ\n")
    
    def _init_storage(self):
        Path(self.history_path.parent).mkdir(exist_ok=True)
        
        if not self.history_path.exists():
            self._save_json(self.history_path, {
                "system_created": datetime.now().isoformat(),
                "commits": [],
                "total_files_created": 0,
                "total_updates": 0
            })
        
        if not self.manifest_path.exists():
            self._save_json(self.manifest_path, {
                "files": {},
                "technologies": {
                    "current": "python-git",
                    "supported": ["python", "markdown", "yaml", "json", "text"],
                    "migrations": []
                },
                "last_scan": None
            })
        
        if not self.migration_log_path.exists():
            self._save_json(self.migration_log_path, {
                "migrations": [],
                "backup_locations": [],
                "compatibility_notes": []
            })
    
    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ═══════════════════════════════════════════════════════════
    # 📝 ส่วนที่ 1: สร้างไฟล์ใหม่อัตโนมัติ
    # ═══════════════════════════════════════════════════════════
    def create_file(self, file_path, content="", description="", auto_commit=True):
        """
        สร้างไฟล์ใหม่และบันทึกลงระบบ
        :param file_path: ที่อยู่ไฟล์ เช่น "systems/new_module.py"
        :param content: เนื้อหาไฟล์
        :param description: คำอธิบายไฟล์
        :param auto_commit: อัปโหลดขึ้น GitHub ทันทีหรือไม่
        """
        full_path = self.repo_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        rel_path = str(file_path)
        manifest = self._load_json(self.manifest_path)
        manifest["files"][rel_path] = {
            "created": datetime.now().isoformat(),
            "description": description,
            "last_modified": datetime.now().isoformat(),
            "size": len(content),
            "type": self._detect_file_type(str(file_path))
        }
        manifest["last_scan"] = datetime.now().isoformat()
        self._save_json(self.manifest_path, manifest)
        
        print(f"📝 สร้างไฟล์: {file_path}")
        if description:
            print(f"   📌 {description}")
        
        if auto_commit:
            self.git_commit_and_push(f"✨ เพิ่มไฟล์ใหม่: {file_path} — {description}")
        
        return True
    
    def _detect_file_type(self, filename):
        """ตรวจสอบประเภทไฟล์"""
        ext = Path(filename).suffix.lower()
        types = {
            ".py": "Python",
            ".md": "Markdown",
            ".json": "JSON",
            ".yml": "YAML",
            ".yaml": "YAML",
            ".html": "HTML",
            ".css": "CSS",
            ".js": "JavaScript",
            ".txt": "Text",
            ".gitignore": "Config"
        }
        return types.get(ext, "Unknown")
    
    # ═══════════════════════════════════════════════════════════
    # 🔄 ส่วนที่ 2: อัปเดตไฟล์ที่มีอยู่แล้ว
    # ═══════════════════════════════════════════════════════════
    def update_file(self, file_path, new_content, update_note="", auto_commit=True):
        """อัปเดตเนื้อหาไฟล์ที่มีอยู่แล้ว"""
        full_path = self.repo_path / file_path
        
        if not full_path.exists():
            print(f"⚠️  ไฟล์ไม่มีอยู่: {file_path} → จะสร้างใหม่แทน")
            return self.create_file(file_path, new_content, update_note, auto_commit)
        
        with open(full_path, 'r', encoding='utf-8') as f:
            old_content = f.read()
        
        if old_content == new_content:
            print(f"ℹ️  ไฟล์ไม่มีการเปลี่ยนแปลง: {file_path}")
            return False
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        manifest = self._load_json(self.manifest_path)
        if str(file_path) in manifest["files"]:
            manifest["files"][str(file_path)]["last_modified"] = datetime.now().isoformat()
            manifest["files"][str(file_path)]["update_note"] = update_note
        self._save_json(self.manifest_path, manifest)
        
        print(f"✏️  อัปเดต: {file_path}")
        if update_note:
            print(f"   📌 {update_note}")
        
        if auto_commit:
            self.git_commit_and_push(f"🔄 อัปเดต: {file_path} — {update_note}")
        
        return True
    
    # ═══════════════════════════════════════════════════════════
    # 🚀 ส่วนที่ 3: คอมมิตและอัปโหลดขึ้น GitHub อัตโนมัติ
    # ═══════════════════════════════════════════════════════════
    def git_commit_and_push(self, message="🔄 อัปเดตผ่าน Vider Auto-System"):
        """ทำการคอมมิตและส่งขึ้น GitHub อัตโนมัติ"""
        try:
            os.chdir(self.repo_path)
            
            # ตรวจสอบสถานะ
            result = subprocess.run(["git", "status", "--porcelain"], 
                                    capture_output=True, text=True)
            if not result.stdout.strip():
                print("ℹ️  ไม่มีการเปลี่ยนแปลงใหม่")
                return False
            
            # เพิ่มไฟล์ทั้งหมด
            subprocess.run(["git", "add", "."], check=True)
            
            # คอมมิต
            subprocess.run(["git", "commit", "-m", message], check=True)
            
            # บันทึกประวัติ
            history = self._load_json(self.history_path)
            commit_info = {
                "id": len(history["commits"]) + 1,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
            history["commits"].append(commit_info)
            history["total_updates"] += 1
            self._save_json(self.history_path, history)
            
            # ส่งขึ้น
            print("⬆️  กำลังส่งขึ้น GitHub...")
            push_result = subprocess.run(["git", "push"], capture_output=True, text=True)
            
            if push_result.returncode == 0:
                print(f"✅ สำเร็จ: {message}")
                return True
            else:
                print(f"⚠️  แจ้งเตือน: {push_result.stderr.strip()[:100]}")
                return False
        
        except subprocess.CalledProcessError as e:
            print(f"❌ ผิดพลาด Git: {e}")
            return False
        except Exception as e:
            print(f"❌ ผิดพลาด: {e}")
            return False
    
    # ═══════════════════════════════════════════════════════════
    # 🌐 ส่วนที่ 4: สแกนและบันทึกสภาพระบบทั้งหมด
    # ═══════════════════════════════════════════════════════════
    def scan_all_files(self):
        """สแกนไฟล์ทั้งหมดและบันทึกรายการปัจจุบัน"""
        print("\n🔍 กำลังสแกนไฟล์ทั้งหมดในระบบ...")
        
        manifest = self._load_json(self.manifest_path)
        manifest["files"] = {}
        
        exclude_dirs = {".git", ".vider", "__pycache__"}
        exclude_exts = {".pyc"}
        
        count = 0
        for root, dirs, files in os.walk(self.repo_path):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            rel_root = Path(root).relative_to(self.repo_path)
            
            for file in files:
                if Path(file).suffix in exclude_exts:
                    continue
                file_path = rel_root / file if str(rel_root) != "." else Path(file)
                full_path = self.repo_path / file_path
                
                manifest["files"][str(file_path)] = {
                    "created": datetime.fromtimestamp(full_path.stat().st_ctime).isoformat(),
                    "last_modified": datetime.fromtimestamp(full_path.stat().st_mtime).isoformat(),
                    "size": full_path.stat().st_size,
                    "type": self._detect_file_type(file),
                    "description": "ไฟล์ที่มีอยู่แล้ว"
                }
                count += 1
        
        manifest["last_scan"] = datetime.now().isoformat()
        self._save_json(self.manifest_path, manifest)
        
        print(f"✅ สแกนเสร็จสิ้น: พบ {count} ไฟล์")
        return count
    
    # ═══════════════════════════════════════════════════════════
    # 🔮 ส่วนที่ 5: รองรับการย้ายไปเทคโนโลยีใหม่ในอนาคต
    # ═══════════════════════════════════════════════════════════
    def prepare_migration(self, target_tech, backup_path=None):
        """
        เตรียมข้อมูลทั้งหมดเพื่อย้ายไปเทคโนโลยีใหม่
        บันทึกทุกอย่างไว้ครบถ้วน ไม่สูญเสียข้อมูล
        """
        print(f"\n🔮 กำลังเตรียมการย้ายไป: {target_tech}")
        
        # 1. สแกนไฟล์ทั้งหมดก่อนย้าย
        total_files = self.scan_all_files()
        
        # 2. สร้างข้อมูลสำรอง
        if not backup_path:
            backup_path = self.repo_path / "backups" / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        backup_path = Path(backup_path)
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # คัดลอกไฟล์ทั้งหมด (ยกเว้น backups และ .git)
        manifest = self._load_json(self.manifest_path)
        copied = 0
        for file_path in manifest["files"].keys():
            src = self.repo_path / file_path
            dst = backup_path / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            copied += 1
        
        # บันทึกข้อมูลการย้าย
        migration_log = self._load_json(self.migration_log_path)
        migration_record = {
            "migration_date": datetime.now().isoformat(),
            "target_technology": target_tech,
            "backup_location": str(backup_path),
            "files_backed_up": copied,
            "total_files": total_files,
            "status": "backup_completed",
            "compatibility_notes": "ทุกไฟล์ถูกเก็บไว้ครบถ้วน สามารถย้อนกลับได้ทุกเมื่อ"
        }
        migration_log["migrations"].append(migration_record)
        migration_log["backup_locations"].append(str(backup_path))
        self._save_json(self.migration_log_path, migration_log)
        
        # อัปเดตข้อมูลเทคโนโลยี
        manifest["technologies"]["migrations"].append({
            "from": manifest["technologies"]["current"],
            "to": target_tech,
            "date": datetime.now().isoformat(),
            "backup_reference": str(backup_path)
        })
        manifest["technologies"]["current"] = target_tech
        self._save_json(self.manifest_path, manifest)
        
        print(f"✅ สำรองข้อมูลเสร็จสิ้น")
        print(f"📂 ที่อยู่ข้อมูลสำรอง: {backup_path}")
        print(f"📦 จำนวนไฟล์ที่เก็บไว้: {copied}")
        print(f"🔄 สามารถย้อนกลับได้ตลอดเวลา")
        
        return {
            "backup_path": str(backup_path),
            "files_count": copied,
            "migration_id": len(migration_log["migrations"])
        }
    
    def get_system_status(self):
        """แสดงสถานะทั้งหมดของระบบ"""
        history = self._load_json(self.history_path)
        manifest = self._load_json(self.manifest_path)
        
        print("\n" + "="*60)
        print("📊 สถานะระบบ Vider Auto-Deploy")
        print("="*60)
        print(f"📅 สร้างระบบเมื่อ: {history['system_created']}")
        print(f"📁 จำนวนไฟล์ทั้งหมด: {len(manifest['files'])}")
        print(f"🔄 จำนวนครั้งที่อัปเดต: {history['total_updates']}")
        print(f"📝 จำนวนคอมมิต: {len(history['commits'])}")
        print(f"🌐 เทคโนโลยีปัจจุบัน: {manifest['technologies']['current']}")
        print(f"🚀 รองรับเทคโนโลยี: {', '.join(manifest['technologies']['supported'])}")
        print(f"🔮 ประวัติการย้าย: {len(manifest['technologies']['migrations'])} ครั้ง")
        print("="*60)
        
        return {
            "total_files": len(manifest["files"]),
            "total_commits": len(history["commits"]),
            "tech_stack": manifest["technologies"]["current"]
        }


# ============================================================
# 🚀 เริ่มทำงาน
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("🤖 VIDER AUTO-DEPLOY — ระบบอัตโนมัติสร้างและอัปเดต GitHub")
    print("  สร้างไฟล์ · อัปเดต · คอมมิต · สำรอง · ย้ายเทคโนโลยี")
    print("="*60 + "\n")
    
    # เริ่มระบบ
    deploy = ViderAutoDeploy()
    
    # สแกนไฟล์ครั้งแรก
    deploy.scan_all_files()
    
    # ตัวอย่างการใช้งาน
    print("\n📌 === ตัวอย่างคำสั่งที่ใช้ได้ ===\n")
    print("สร้างไฟล์ใหม่:")
    print("  deploy.create_file('ชื่อไฟล์.py', 'เนื้อหา', 'คำอธิบาย')")
    print("\nอัปเดตไฟล์:")
    print("  deploy.update_file('ชื่อไฟล์.py', 'เนื้อหาใหม่', 'แก้ไขอะไร')")
    print("\nส่งขึ้น GitHub ด้วยตัวเอง:")
    print("  deploy.git_commit_and_push('ข้อความคอมมิต')")
    print("\nเตรียมย้ายไปเทคโนโลยีใหม่:")
    print("  deploy.prepare_migration('ชื่อเทคโนโลยี', 'ที่อยู่สำรอง')")
    print("\nดูสถานะระบบ:")
    print("  deploy.get_system_status()")
    
    # สร้างโฟลเดอร์ตัวอย่างระบบใหม่
    print("\n✨ พร้อมทำงานแล้ว! ทุกการเปลี่ยนแปลงจะถูกบันทึกและส่งขึ้น GitHub อัตโนมัติ")
    print("   ข้อมูลทั้งหมดจะถูกเก็บไว้ เพื่อย้ายไปเทคโนโลยีใหม่ในอนาคตได้ตลอดไป 🚀💎")

