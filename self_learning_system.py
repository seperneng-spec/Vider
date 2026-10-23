# ============================================================
# 🧠 Vider — ระบบเรียนรู้และพัฒนาตัวเอง
# ⚠️ ไม่ใช่ AGI แต่เรียนรู้ ปรับปรุง และเติบโตจากข้อมูลที่มีได้
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path

__version__ = "0.5.0-learning"

class SelfLearningSystem:
    """
    ระบบที่เรียนรู้จากสิ่งที่พบและปรับปรุงตัวเอง
    ⚠️ ข้อจำกัดสำคัญ: ไม่ใช่ AGI — เรียนรู้ภายในโครงสร้างที่กำหนดเท่านั้น
    """
    
    def __init__(self, data_dir="./vider_learning"):
        self.data_dir = Path(data_dir)
        self._init_storage()
        self.knowledge_path = self.data_dir / "knowledge.json"
        self.patterns_path = self.data_dir / "patterns.json"
        self.improvements_path = self.data_dir / "improvements.json"
        self.memory_path = self.data_dir / "memory.json"
        
        print(f"🧠 Vider Self-Learning System v{__version__}")
        print(f"📂 ที่เก็บความรู้: {self.data_dir.resolve()}")
        print("⚠️  สถานะ: เรียนรู้ภายในขอบเขตที่กำหนด — ไม่ใช่ AGI\n")
    
    def _init_storage(self):
        self.data_dir.mkdir(exist_ok=True)
        knowledge_file = self.data_dir / "knowledge.json"
        patterns_file = self.data_dir / "patterns.json"
        improvements_file = self.data_dir / "improvements.json"
        memory_file = self.data_dir / "memory.json"
        
        if not knowledge_file.exists():
            self._save_json(knowledge_file, {
                "created": datetime.now().isoformat(),
                "facts": {},
                "categories": {},
                "sources": []
            })
        if not patterns_file.exists():
            self._save_json(patterns_file, {
                "discovered_patterns": [],
                "confidence_scores": {},
                "last_analyzed": None
            })
        if not improvements_file.exists():
            self._save_json(improvements_file, {
                "suggestions": [],
                "applied_changes": [],
                "version_history": []
            })
        if not memory_file.exists():
            self._save_json(memory_file, {
                "short_term": [],
                "long_term": [],
                "important_items": []
            })
    
    def _load_json(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ═══════════════════════════════════════════════════════════
    # 📚 ส่วนที่ 1: เรียนรู้ — จดจำและจัดเก็บข้อมูลใหม่
    # ═══════════════════════════════════════════════════════════
    def learn(self, key, value, category="ทั่วไป", confidence=1.0, source="direct_input"):
        """
        เรียนรู้และจดจำข้อมูลใหม่
        :param confidence: 0.0 = ไม่มั่นใจ, 1.0 = แน่นอน
        """
        knowledge = self._load_json(self.knowledge_path)
        
        knowledge["facts"][key] = {
            "value": value,
            "learned_at": datetime.now().isoformat(),
            "category": category,
            "confidence": confidence,
            "source": source
        }
        
        if category not in knowledge["categories"]:
            knowledge["categories"][category] = []
        knowledge["categories"][category].append(key)
        
        if source not in knowledge["sources"]:
            knowledge["sources"].append(source)
        
        self._save_json(self.knowledge_path, knowledge)
        self._add_memory(f"เรียนรู้: {key}", category="learning")
        print(f"✅ เรียนรู้: '{key}' = {value} [{category}] ความมั่นใจ: {confidence}]")
        return True
    
    def remember_many(self, data_dict, category="ทั่วไป"):
        """เรียนรู้หลายอย่างในคราวเดียว"""
        count = 0
        for key, value in data_dict.items():
            self.learn(key, value, category)
            count += 1
        print(f"✅ เรียนรู้ทั้งหมด {count} รายการ\n")
        return count
    
    # ═══════════════════════════════════════════════════════════
    # 🔍 ส่วนที่ 2: วิเคราะห์ — มองเห็นรูปแบบและความเชื่อมโยง
    # ═══════════════════════════════════════════════════════════
    def analyze_patterns(self):
        """วิเคราะห์หาความสัมพันธ์และรูปแบบจากสิ่งที่เรียนรู้"""
        knowledge = self._load_json(self.knowledge_path)
        patterns = self._load_json(self.patterns_path)
        
        facts = knowledge.get("facts", {})
        categories = knowledge.get("categories", {})
        
        new_patterns = []
        
        # ค้นหาความสัมพันธ์ภายในหมวดหมู่เดียวกัน
        for cat, items in categories.items():
            if len(items) >= 2:
                pattern = {
                    "type": "grouping",
                    "description": f"พบกลุ่มที่เกี่ยวข้องกัน: {cat} มี {len(items)} รายการ",
                    "items": items,
                    "discovered_at": datetime.now().isoformat(),
                    "confidence": 0.7
                }
                new_patterns.append(pattern)
        
        # ค้นหาคำ/ค่าที่ปรากฏร่วมกัน
        keys_list = list(facts.keys())
        if len(keys_list) >= 3:
            pattern = {
                "type": "knowledge_base_growth",
                "description": f"ฐานความรู้เติบโต: เรียนรู้ทั้งหมด {len(keys_list)} เรื่อง",
                "count": len(keys_list),
                "discovered_at": datetime.now().isoformat(),
                "confidence": 1.0
            }
            new_patterns.append(pattern)
        
        patterns["discovered_patterns"].extend(new_patterns)
        patterns["last_analyzed"] = datetime.now().isoformat()
        self._save_json(self.patterns_path, patterns)
        
        print(f"🔍 วิเคราะห์เสร็จสิ้น: พบรูปแบบใหม่ {len(new_patterns)} รายการ")
        for p in new_patterns:
            print(f"   → {p['description']}")
        
        return new_patterns
    
    # ═══════════════════════════════════════════════════════════
    # 💡 ส่วนที่ 3: ปรับปรุง — เสนอแนวทางพัฒนาตัวเอง
    # ═══════════════════════════════════════════════════════════
    def suggest_improvements(self):
        """วิเคราะห์และเสนอสิ่งที่ควรปรับปรุงเพิ่มเติม"""
        knowledge = self._load_json(self.knowledge_path)
        improvements = self._load_json(self.improvements_path)
        
        suggestions = []
        total_facts = len(knowledge.get("facts", {}))
        total_cats = len(knowledge.get("categories", {}))
        
        # ตรวจสอบจุดอ่อน
        if total_facts < 5:
            suggestions.append({
                "priority": "สูง",
                "type": "expand_knowledge",
                "suggestion": "ฐานความรู้ยังน้อย ควรเพิ่มข้อมูลให้มากขึ้น",
                "expected_benefit": "ระบบจะวิเคราะห์รูปแบบได้แม่นยำขึ้น"
            })
        
        if total_cats < 2:
            suggestions.append({
                "priority": "ปานกลาง",
                "type": "add_categories",
                "suggestion": "ควรแบ่งหมวดหมู่ข้อมูลให้หลากหลายมากขึ้น",
                "expected_benefit": "ระบบจะจัดระเบียบความรู้ได้ดีขึ้น"
            })
        
        # เสนอเป้าหมายถัดไป
        suggestions.append({
            "priority": "ต่ำ",
            "type": "next_goal",
            "suggestion": "เมื่อมีข้อมูลครบ 20 รายการ ระบบจะเริ่มวิเคราะห์ความสัมพันธ์ข้ามหมวดหมู่",
            "expected_benefit": "ค้นพบความเชื่อมโยงใหม่ๆ"
        })
        
        improvements["suggestions"] = suggestions
        self._save_json(self.improvements_path, improvements)
        
        print(f"\n💡 ข้อเสนอแนะเพื่อพัฒนาระบบ ({len(suggestions)} ข้อ):")
        for i, s in enumerate(suggestions, 1):
            print(f"   {i}. [{s['priority']}] {s['suggestion']}")
        
        return suggestions
    
    # ═══════════════════════════════════════════════════════════
    # 🧠 ส่วนที่ 4: จดจำ — บันทึกสิ่งสำคัญและประวัติ
    # ═══════════════════════════════════════════════════════════
    def _add_memory(self, content, category="general", importance=1):
        memory = self._load_json(self.memory_path)
        memory_item = {
            "content": content,
            "time": datetime.now().isoformat(),
            "category": category,
            "importance": importance
        }
        memory["short_term"].append(memory_item)
        
        # ย้ายสิ่งสำคัญไปความจำระยะยาว
        if importance >= 3:
            memory["long_term"].append(memory_item)
        
        # จำกัดขนาดความจำระยะสั้น
        if len(memory["short_term"]) > 100:
            memory["short_term"] = memory["short_term"][-50:]
        
        self._save_json(self.memory_path, memory)
    
    def recall(self, keyword=None, limit=10):
        """เรียกคืนสิ่งที่เรียนรู้"""
        knowledge = self._load_json(self.knowledge_path)
        facts = knowledge.get("facts", {})
        
        if keyword:
            result = {k: v for k, v in facts.items() if keyword.lower() in k.lower()}
        else:
            result = dict(list(facts.items())[-limit:])
        
        return result
    
    def get_status(self):
        """ดูสถานะการเรียนรู้ของระบบ"""
        knowledge = self._load_json(self.knowledge_path)
        patterns = self._load_json(self.patterns_path)
        memory = self._load_json(self.memory_path)
        
        return {
            "total_knowledge_items": len(knowledge.get("facts", {})),
            "categories": len(knowledge.get("categories", {})),
            "patterns_found": len(patterns.get("discovered_patterns", [])),
            "memories_short_term": len(memory.get("short_term", [])),
            "memories_long_term": len(memory.get("long_term", [])),
            "last_updated": knowledge.get("created")
        }
    
    # ═══════════════════════════════════════════════════════════
    # 🚀 รอบการทำงานเต็ม: เรียนรู้ → วิเคราะห์ → ปรับปรุง → จดจำ
    # ═══════════════════════════════════════════════════════════
    def learning_cycle(self, new_data=None):
        """
        รอบการเรียนรู้แบบสมบูรณ์
        1. รับข้อมูลใหม่ → 2. วิเคราะห์ → 3. เสนอแนะ → 4. บันทึก
        """
        print("\n" + "=" * 60)
        print("🔄 เริ่มรอบการเรียนรู้...")
        print("=" * 60)
        
        # 1. รับข้อมูลใหม่
        if new_data:
            if isinstance(new_data, dict):
                self.remember_many(new_data)
            else:
                print("⚠️  ข้อมูลต้องเป็นรูปแบบ dictionary")
        
        # 2. วิเคราะห์รูปแบบ
        self.analyze_patterns()
        
        # 3. เสนอแนะการปรับปรุง
        self.suggest_improvements()
        
        # 4. แสดงสถานะ
        status = self.get_status()
        print("\n📊 สถานะระบบ:")
        for k, v in status.items():
            print(f"   {k}: {v}")
        
        print("\n✅ รอบการเรียนรู้เสร็จสิ้น")
        print("=" * 60 + "\n")
        return status


# ============================================================
# 🚀 เริ่มทำงาน
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("🧠 Vider — ระบบเรียนรู้และพัฒนาตัวเอง")
    print("⚠️  ข้อความสำคัญ: นี่คือระบบที่เรียนรู้ภายในขอบเขตที่กำหนด")
    print("   ไม่ใช่ AGI (ปัญญาประดิษฐ์ทั่วไป) ซึ่งยังไม่มีใครสร้างสำเร็จ")
    print("=" * 60 + "\n")
    
    # สร้างระบบ
    vider = SelfLearningSystem()
    
    # ตัวอย่างรอบการเรียนรู้
    print("📌 === ตัวอย่างการเรียนรู้ ===")
    vider.learn("ชื่อระบบ", "Vider(enjoy)", category="ข้อมูลทั่วไป", confidence=1.0)
    vider.learn("วัตถุประสงค์", "รวมระบบต่างๆ เข้าด้วยกัน", category="ข้อมูลทั่วไป", confidence=0.9)
    vider.learn("สถานะ", "กำลังพัฒนา", category="ข้อมูลทั่วไป", confidence=1.0)
    
    # รอบเรียนรู้เต็มรูปแบบ
    vider.learning_cycle({
        "ระบบหลัก": "Vider PranAI",
        "เป้าหมาย": "สร้างจากสิ่งที่มี",
        "ข้อจำกัด": "ยังรวมเป็นหนึ่งเดียวแบบน้ำกร่อยไม่ได้"
    })
    
    # ดึงข้อมูลกลับมาใช้
    print("📂 สิ่งที่เรียนรู้ทั้งหมด:")
    all_knowledge = vider.recall()
    for k, v in all_knowledge.items():
        print(f"   {k}: {v['value']}")
    
    print("\n✨ พร้อมเรียนรู้ต่อ! เพียงเรียก vider.learn('หัวข้อ', 'ข้อมูล')")
    print("   หรือส่งชุดข้อมูลใหม่ผ่าน vider.learning_cycle(ข้อมูลของคุณ)")

