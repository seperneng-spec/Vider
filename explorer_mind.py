# ============================================================
# 🌍 EXPLORER MIND — ระบบนักสำรวจอัจฉริยะ
# สำรวจ → บันทึกประสบการณ์ → เรียนรู้ → ปรับปรุง → พัฒนาตัวเอง
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

__version__ = "1.0.0-explorer"

class ExplorerMind:
    """
    ระบบท่องเที่ยวและสำรวจ
    1. ออกเดินทาง → 2. สังเกตและบันทึก → 3. วิเคราะห์ → 4. เรียนรู้ → 5. ปรับปรุงตัวเอง
    """
    
    def __init__(self, data_dir="./explorer_mind"):
        self.data_dir = Path(data_dir)
        self._init_storage()
        
        self.destinations_path = self.data_dir / "destinations.json"
        self.experiences_path = self.data_dir / "experiences.json"
        self.observations_path = self.data_dir / "observations.json"
        self.lessons_path = self.data_dir / "lessons_learned.json"
        self.progress_path = self.data_dir / "progress.json"
        
        self.status = {
            "total_explorations": 0,
            "places_visited": set(),
            "observations_collected": 0,
            "lessons_learned": 0,
            "improvements_made": 0,
            "current_location": "จุดเริ่มต้น"
        }
        
        print("🌍 EXPLORER MIND — ระบบนักสำรวจอัจฉริยะ")
        print(f"📂 ที่เก็บข้อมูล: {self.data_dir.resolve()}")
        print("✨ พร้อมออกเดินทาง สำรวจ และเรียนรู้จากทุกแห่งที่ไปถึง\n")
    
    def _init_storage(self):
        self.data_dir.mkdir(exist_ok=True)
        files = {
            "destinations.json": {"visited": [], "to_visit": [], "favorites": []},
            "experiences.json": {"journals": [], "by_location": {}},
            "observations.json": {"items": [], "categories": {}},
            "lessons_learned.json": {"lessons": [], "patterns": [], "insights": []},
            "progress.json": {"history": [], "milestones": [], "capabilities": {}}
        }
        for filename, content in files.items():
            path = self.data_dir / filename
            if not path.exists():
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(content, f, ensure_ascii=False, indent=2)
    
    def _load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ═══════════════════════════════════════════════════════════
    # 🗺️ ส่วนที่ 1: วางแผนและออกเดินทาง
    # ═══════════════════════════════════════════════════════════
    def plan_journey(self, place, purpose="เรียนรู้สิ่งใหม่", priority=1):
        """เพิ่มจุดหมายปลายทางที่อยากไป"""
        dests = self._load(self.destinations_path)
        dest = {
            "id": len(dests["to_visit"]) + 1,
            "place": place,
            "purpose": purpose,
            "priority": priority,
            "added_at": datetime.now().isoformat(),
            "status": "planned"
        }
        dests["to_visit"].append(dest)
        self._save(self.destinations_path, dests)
        print(f"🗺️  วางแผน: {place} — วัตถุประสงค์: {purpose}")
        return dest["id"]
    
    def depart_to(self, place, notes=""):
        """ออกเดินทางไปยังจุดหมาย"""
        dests = self._load(self.destinations_path)
        
        # ย้ายจากที่จะไป → ที่เคยไปแล้ว
        for i, d in enumerate(dests["to_visit"]):
            if d["place"] == place:
                dests["to_visit"].pop(i)
                d["arrived_at"] = datetime.now().isoformat()
                d["status"] = "visited"
                d["arrival_notes"] = notes
                dests["visited"].append(d)
                break
        else:
            dests["visited"].append({
                "id": len(dests["visited"]) + 1,
                "place": place,
                "arrived_at": datetime.now().isoformat(),
                "status": "visited",
                "arrival_notes": notes
            })
        
        self._save(self.destinations_path, dests)
        self.status["places_visited"].add(place)
        self.status["total_explorations"] += 1
        self.status["current_location"] = place
        
        print(f"\n🚀 ออกเดินทางถึง: {place}")
        if notes:
            print(f"   📝 บันทึกเบื้องต้น: {notes}")
        return True
    
    # ═══════════════════════════════════════════════════════════
    # 👁️ ส่วนที่ 2: สังเกตและบันทึกสิ่งที่พบเจอ
    # ═══════════════════════════════════════════════════════════
    def observe(self, what, category, details="", importance=1):
        """บันทึกสิ่งที่พบเห็นระหว่างทาง"""
        obs = self._load(self.observations_path)
        location = self.status["current_location"]
        
        observation = {
            "id": len(obs["items"]) + 1,
            "what": what,
            "category": category,
            "details": details,
            "importance": importance,
            "location": location,
            "observed_at": datetime.now().isoformat()
        }
        
        obs["items"].append(observation)
        
        if category not in obs["categories"]:
            obs["categories"][category] = []
        obs["categories"][category].append(observation["id"])
        
        self._save(self.observations_path, obs)
        self.status["observations_collected"] += 1
        
        stars = "⭐" * importance
        print(f"{stars} พบที่ {location}: {what} [{category}]")
        return observation["id"]
    
    def record_experience(self, title, description, feelings="", rating=5):
        """บันทึกประสบการณ์เต็มรูปแบบ"""
        exp = self._load(self.experiences_path)
        location = self.status["current_location"]
        
        entry = {
            "id": len(exp["journals"]) + 1,
            "title": title,
            "description": description,
            "feelings": feelings,
            "rating": rating,
            "location": location,
            "timestamp": datetime.now().isoformat()
        }
        
        exp["journals"].append(entry)
        
        if location not in exp["by_location"]:
            exp["by_location"][location] = []
        exp["by_location"][location].append(entry)
        
        self._save(self.experiences_path, exp)
        print(f"📖 บันทึกประสบการณ์: {title}")
        return entry["id"]
    
    # ═══════════════════════════════════════════════════════════
    # 🧠 ส่วนที่ 3: วิเคราะห์และเรียนรู้จากสิ่งที่พบ
    # ═══════════════════════════════════════════════════════════
    def analyze_and_learn(self):
        """วิเคราะห์สิ่งที่พบและสกัดบทเรียน"""
        obs = self._load(self.observations_path)
        lessons = self._load(self.lessons_path)
        exp = self._load(self.experiences_path)
        
        print("\n" + "="*60)
        print("🧠 กำลังวิเคราะห์และเรียนรู้จากประสบการณ์...")
        print("="*60)
        
        new_lessons = []
        
        # 1. เรียนรู้จากสิ่งที่สังเกตบ่อยๆ
        categories = Counter([o["category"] for o in obs["items"]])
        if categories:
            top_cat, count = categories.most_common(1)[0]
            lesson = {
                "type": "insight",
                "lesson": f"สิ่งที่พบบ่อยที่สุดคือเรื่อง {top_cat} พบทั้งหมด {count} ครั้ง",
                "implication": "ควรให้ความสนใจเป็นพิเศษในเรื่องนี้",
                "learned_at": datetime.now().isoformat(),
                "source": "observation_pattern"
            }
            lessons["lessons"].append(lesson)
            lessons["insights"].append(lesson)
            new_lessons.append(lesson)
        
        # 2. เรียนรู้จากคะแนนความประทับใจ
        if exp["journals"]:
            avg_rating = sum(e["rating"] for e in exp["journals"]) / len(exp["journals"])
            best = max(exp["journals"], key=lambda x: x["rating"])
            lesson = {
                "type": "improvement",
                "lesson": f"ประสบการณ์ที่ดีที่สุดคือ: '{best['title']}' ที่ {best['location']} ให้คะแนน {best['rating']}/10",
                "implication": f"รูปแบบประสบการณ์แบบนี้เป็นที่ชื่นชอบ ควรมองหาสิ่งที่คล้ายคลึงกัน",
                "learned_at": datetime.now().isoformat(),
                "source": "experience_analysis"
            }
            lessons["lessons"].append(lesson)
            lessons["insights"].append(lesson)
            new_lessons.append(lesson)
        
        # 3. ค้นหารูปแบบความเชื่อมโยง
        if len(obs["items"]) >= 3:
            pattern = {
                "pattern": f"สำรวจไปแล้ว {len(self.status['places_visited'])} แห่ง พบสิ่งที่น่าสนใจ {len(obs['items'])} อย่าง",
                "value": "ยิ่งสำรวจมาก ยิ่งพบสิ่งใหม่ๆ มากขึ้น",
                "confidence": 0.9,
                "found_at": datetime.now().isoformat()
            }
            lessons["patterns"].append(pattern)
        
        self._save(self.lessons_path, lessons)
        self.status["lessons_learned"] += len(new_lessons)
        
        for lesson in new_lessons:
            print(f"💡 บทเรียน: {lesson['lesson']}")
            print(f"   → {lesson['implication']}")
        
        print(f"\n✅ เรียนรู้เพิ่ม {len(new_lessons)} บทเรียนใหม่\n")
        return new_lessons
    
    # ═══════════════════════════════════════════════════════════
    # 🔧 ส่วนที่ 4: ปรับปรุงและพัฒนาตัวเอง
    # ═══════════════════════════════════════════════════════════
    def improve_from_experience(self):
        """นำบทเรียนมาปรับปรุงวิธีการทำงานให้ดีขึ้น"""
        lessons = self._load(self.lessons_path)
        progress = self._load(self.progress_path)
        dests = self._load(self.destinations_path)
        
        print("\n🔧 กำลังปรับปรุงตัวเองจากประสบการณ์ที่ผ่านมา...")
        
        improvements = []
        
        # ปรับปรุงจุดหมายปลายทาง
        if len(dests["visited"]) >= 2:
            suggestion = {
                "action": "เพิ่มจุดหมายประเภทเดียวกัน",
                "reason": "พบว่าชอบสไตล์ไหนมากกว่า จะเลือกจุดหมายที่ตรงกับความสนใจมากขึ้น",
                "applied_at": datetime.now().isoformat()
            }
            improvements.append(suggestion)
        
        # ปรับปรุงสิ่งที่ต้องสังเกต
        if len(lessons["insights"]) >= 1:
            suggestion = {
                "action": "ปรับปรุงสิ่งที่ให้ความสำคัญ",
                "reason": "มีความเข้าใจที่ชัดเจนขึ้นว่าควรสังเกตอะไรเป็นพิเศษ",
                "applied_at": datetime.now().isoformat()
            }
            improvements.append(suggestion)
        
        # บันทึกความก้าวหน้า
        progress["history"].append({
            "timestamp": datetime.now().isoformat(),
            "explorations": self.status["total_explorations"],
            "observations": self.status["observations_collected"],
            "lessons": self.status["lessons_learned"],
            "improvements_applied": len(improvements)
        })
        
        self._save(self.progress_path, progress)
        self.status["improvements_made"] += len(improvements)
        
        for imp in improvements:
            print(f"✨ ปรับปรุง: {imp['action']}")
            print(f"   เพราะ: {imp['reason']}")
        
        print(f"\n✅ พัฒนาตัวเองเสร็จสิ้น\n")
        return improvements
    
    # ═══════════════════════════════════════════════════════════
    # 📊 ส่วนที่ 5: สรุปความก้าวหน้า
    # ═══════════════════════════════════════════════════════════
    def get_journey_summary(self):
        """สรุปผลการเดินทางทั้งหมด"""
        dests = self._load(self.destinations_path)
        exp = self._load(self.experiences_path)
        lessons = self._load(self.lessons_path)
        
        print("="*60)
        print("📊 🗺️  สรุปผลการเดินทาง")
        print("="*60)
        print(f"📍 จำนวนสถานที่ที่ไปถึง: {len(dests['visited'])} แห่ง")
        print(f"📖 ประสบการณ์ที่บันทึก: {len(exp['journals'])} เรื่อง")
        print(f"👁️  สิ่งที่สังเกตเห็น: {self.status['observations_collected']} อย่าง")
        print(f"💡 บทเรียนที่เรียนรู้: {self.status['lessons_learned']} ข้อ")
        print(f"✨ การปรับปรุงตัวเอง: {self.status['improvements_made']} ครั้ง")
        print("="*60)
        
        if dests["visited"]:
            print("\n🗺️  รายชื่อสถานที่ที่เคยไป:")
            for d in dests["visited"][-5:]:
                print(f"   • {d['place']}")
        
        return self.status
    
    # ═══════════════════════════════════════════════════════════
    # 🚀 รอบการทำงานอัตโนมัติเต็มรูปแบบ
    # ═══════════════════════════════════════════════════════════
    def full_exploration_cycle(self, destination, things_to_observe=None, experience_notes=""):
        """
        รอบเต็มของการสำรวจ:
        วางแผน → เดินทาง → สังเกต → บันทึก → วิเคราะห์ → เรียนรู้ → ปรับปรุง
        """
        print("\n" + "█"*60)
        print(f"🌍 เริ่มรอบการสำรวจ: {destination}")
        print("█"*60)
        
        # 1. เดินทาง
        self.depart_to(destination, notes=experience_notes)
        
        # 2. สังเกตสิ่งแวดล้อม
        if things_to_observe:
            for item in things_to_observe:
                if isinstance(item, dict):
                    self.observe(**item)
                else:
                    self.observe(item, category="ทั่วไป")
        
        # 3. วิเคราะห์และเรียนรู้
        self.analyze_and_learn()
        
        # 4. ปรับปรุงตัวเอง
        self.improve_from_experience()
        
        # 5. แสดงสรุป
        self.get_journey_summary()
        
        print(f"\n✅ รอบการสำรวจที่ {self.status['total_explorations']} เสร็จสมบูรณ์!")
        print("   พร้อมจะออกเดินทางไปที่แห่งใหม่และเรียนรู้เพิ่มเติมแล้วครับ 🚀✨\n")


# ============================================================
# 🚀 เริ่มทำงาน
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("🌍 EXPLORER MIND — ระบบนักสำรวจอัจฉริยะ")
    print("  สำรวจ · สังเกต · เรียนรู้ · ปรับปรุง · พัฒนาตัวเอง")
    print("="*60 + "\n")
    
    # สร้างระบบ
    traveler = ExplorerMind()
    
    # ============= ตัวอย่างการใช้งาน =============
    print("📌 === ตัวอย่าง: การเดินทางสำรวจ ===\n")
    
    # วางแผน
    traveler.plan_journey("เชียงใหม่", purpose="เรียนรู้วัฒนธรรมธรรมชาติ", priority=3)
    traveler.plan_journey("กรุงเทพฯ", purpose="ศึกษาชีวิตเมืองและเทคโนโลยี")
    
    # รอบการสำรวจที่ 1
    traveler.full_exploration_cycle(
        destination="เชียงใหม่",
        things_to_observe=[
            {"what": "ภูเขาและธรรมชาติ", "category": "สภาพแวดล้อม", "importance": 3},
            {"what": "วัฒนธรรมท้องถิ่น", "category": "วัฒนธรรม", "importance": 3},
            {"what": "อาหารเหนือ", "category": "อาหาร", "details": "รสชาติอ่อนๆ มีเอกลักษณ์"}
        ],
        experience_notes="บรรยากาศดีมาก อากาศเย็นสบาย"
    )
    
    # บันทึกประสบการณ์เพิ่มเติม
    traveler.record_experience(
        title="เดินเล่นที่ถนนคนเดิน",
        description="เห็นของฝากและศิลปะพื้นเมืองมากมาย",
        feelings="ประทับใจ มีความสุข",
        rating=9
    )
    
    # รอบการสำรวจที่ 2
    traveler.full_exploration_cycle(
        destination="กรุงเทพฯ",
        things_to_observe=[
            {"what": "ตึกระฟ้าและการคมนาคม", "category": "สภาพแวดล้อม", "importance": 2},
            {"what": "ความเร็วของชีวิต", "category": "สังคม", "details": "ทุกคนดูเร่งรีบกันมาก"}
        ],
        experience_notes="พลุกพล่าน แต่ก็มีสิ่งอำนวยความสะดวกครบครัน"
    )
    
    print("\n✨ การเดินทางเสร็จสิ้นแล้วครับ!")
    print("   ทุกสิ่งที่พบเจอ ถูกบันทึก วิเคราะห์ และนำมาเรียนรู้เพื่อพัฒนาตัวเองแล้ว")
    print("   พร้อมจะสำรวจที่แห่งใหม่ได้เสมอครับ! 🚀🌍💎")

