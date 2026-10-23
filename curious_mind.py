# ============================================================
# 🧠 ระบบ "ขี้สงสัย" — Curious Mind System
# สงสัย → เรียนรู้ → จดจำ → ปรับตัวเอง → พัฒนาต่ออัตโนมัติ
# ============================================================

import json
import os
from datetime import datetime
from pathlib import Path
from collections import Counter

__version__ = "1.0.0-curious"

class CuriousMind:
    """
    ระบบที่มีความสงสัยเป็นจุดเริ่มต้น
    1. ตั้งคำถาม → 2. ค้นหาคำตอบ → 3. เรียนรู้ → 4. บันทึก → 5. ปรับปรุง
    """
    
    def __init__(self, data_dir="./curious_mind"):
        self.data_dir = Path(data_dir)
        self._init_storage()
        
        self.questions_path = self.data_dir / "questions.json"
        self.knowledge_path = self.data_dir / "knowledge.json"
        self.improvements_path = self.data_dir / "improvements.json"
        self.cycles_path = self.data_dir / "learning_cycles.json"
        
        self.state = {
            "curiosity_level": 0,
            "knowledge_growth": 0,
            "questions_asked": 0,
            "answers_found": 0
        }
        
        print("🧠 Curious Mind — ระบบขี้สงสัย เริ่มทำงานแล้ว")
        print(f"📂 ที่เก็บข้อมูล: {self.data_dir.resolve()}")
        print("✨ พร้อมที่จะสงสัย เรียนรู้ และเติบโตไปเรื่อยๆ\n")
    
    def _init_storage(self):
        self.data_dir.mkdir(exist_ok=True)
        files = {
            "questions.json": {"pending": [], "answered": [], "abandoned": []},
            "knowledge.json": {
                "topics": {},
                "connections": [],
                "last_updated": None
            },
            "improvements.json": {
                "adjustments": [],
                "patterns_found": [],
                "version": __version__
            },
            "learning_cycles.json": {
                "cycles": [],
                "total_cycles": 0
            }
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
    # ❓ ส่วนที่ 1: ตั้งคำถาม — เมื่อสงสัย ให้ถาม
    # ═══════════════════════════════════════════════════════════
    def wonder(self, question, context=None, priority=1):
        """
        บันทึกความสงสัย
        :param priority: 1=ทั่วไป, 2=สำคัญ, 3=สำคัญที่สุด
        """
        data = self._load(self.questions_path)
        
        question_entry = {
            "id": len(data["pending"]) + len(data["answered"]) + 1,
            "question": question,
            "context": context,
            "asked_at": datetime.now().isoformat(),
            "priority": priority,
            "status": "pending",
            "answer": None,
            "source": None
        }
        
        data["pending"].append(question_entry)
        self._save(self.questions_path, data)
        
        self.state["curiosity_level"] += priority
        self.state["questions_asked"] += 1
        
        stars = "⭐" * priority
        print(f"{stars} สงสัย: {question}")
        return question_entry["id"]
    
    def generate_related_questions(self, topic, count=3):
        """สร้างคำถามที่เกี่ยวข้องอัตโนมัติ"""
        templates = [
            f"อะไรคือ {topic}?",
            f"ทำไม {topic} ถึงสำคัญ?",
            f"{topic} สามารถนำไปใช้ทำอะไรได้บ้าง?",
            f"มีข้อจำกัดอะไรของ {topic} ไหม?",
            f"{topic} สามารถพัฒนาไปในทิศทางไหนได้อีก?"
        ]
        selected = templates[:count]
        ids = []
        for q in selected:
            qid = self.wonder(q, context=f"auto-generated from topic: {topic}")
            ids.append(qid)
        return ids
    
    # ═══════════════════════════════════════════════════════════
    # 💡 ส่วนที่ 2: หาคำตอบ — เมื่อมีคำตอบ ให้เรียนรู้
    # ═══════════════════════════════════════════════════════════
    def learn_answer(self, question_id, answer, source="direct_input", confidence=1.0):
        """บันทึกคำตอบและเปลี่ยนความสงสัยให้เป็นความรู้"""
        data = self._load(self.questions_path)
        
        # หาคำถามที่ตรงกับ ID
        found = None
        for i, q in enumerate(data["pending"]):
            if q["id"] == question_id:
                found = data["pending"].pop(i)
                break
        
        if not found:
            for i, q in enumerate(data["answered"]):
                if q["id"] == question_id:
                    found = q
                    break
        
        if not found:
            print(f"❌ ไม่พบคำถาม ID: {question_id}")
            return False
        
        # อัปเดตคำถาม
        found["answer"] = answer
        found["status"] = "answered"
        found["answered_at"] = datetime.now().isoformat()
        found["source"] = source
        found["confidence"] = confidence
        
        data["answered"].append(found)
        self._save(self.questions_path, data)
        
        # เพิ่มเข้าสู่คลังความรู้
        self._add_to_knowledge(found["question"], answer, confidence)
        
        self.state["answers_found"] += 1
        print(f"✅ เรียนรู้แล้ว: {found['question']}")
        print(f"   คำตอบ: {answer}")
        return True
    
    def _add_to_knowledge(self, question, answer, confidence):
        """ย้ายคำตอบเข้าสู่ฐานความรู้"""
        knowledge = self._load(self.knowledge_path)
        
        topic = self._extract_topic(question)
        knowledge["topics"][topic] = {
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "learned_at": datetime.now().isoformat(),
            "times_referenced": 0
        }
        knowledge["last_updated"] = datetime.now().isoformat()
        self._save(self.knowledge_path, knowledge)
        self.state["knowledge_growth"] += 1
    
    def _extract_topic(self, question):
        """แยกหัวข้อจากคำถาม — อย่างง่าย"""
        q = question.replace("?", "").replace("อะไรคือ", "").replace("ทำไม", "").strip()
        return q if q else question[:30]
    
    # ═══════════════════════════════════════════════════════════
    # 🔄 ส่วนที่ 3: วิเคราะห์และปรับตัว — เรียนรู้จากสิ่งที่เรียนรู้
    # ═══════════════════════════════════════════════════════════
    def reflect_and_adjust(self):
        """
        ทบทวนสิ่งที่เรียนรู้:
        - มีเรื่องไหนที่ยังสงสัยต่อ?
        - มีความเชื่อมโยงอะไรระหว่างเรื่องที่เรียนรู้ไหม?
        - ควรถามอะไรต่อ?
        """
        questions = self._load(self.questions_path)
        knowledge = self._load(self.knowledge_path)
        improvements = self._load(self.improvements_path)
        
        print("\n" + "=" * 50)
        print("🔍 กำลังทบทวนและปรับตัว...")
        print("=" * 50)
        
        adjustments = []
        
        # 1. ถามต่อจากเรื่องที่เพิ่งเรียนรู้
        recent_topics = list(knowledge["topics"].keys())[-3:]
        for topic in recent_topics:
            new_q = f"สามารถนำ {topic} ไปประยุกต์ใช้งานจริงได้อย่างไรบ้าง?"
            qid = self.wonder(new_q, context="auto-followup")
            adjustments.append({
                "type": "followup_question",
                "detail": f"ถามต่อ: {new_q}",
                "triggered_by": topic
            })
        
        # 2. ค้นหาความเชื่อมโยงระหว่างความรู้
        all_topics = list(knowledge["topics"].keys())
        if len(all_topics) >= 2:
            for i in range(len(all_topics)-1):
                t1, t2 = all_topics[i], all_topics[i+1]
                connection = f"ความสัมพันธ์ระหว่าง '{t1}' กับ '{t2}'"
                if connection not in [c.get("type") for c in improvements["patterns_found"]]:
                    improvements["patterns_found"].append({
                        "type": connection,
                        "found_at": datetime.now().isoformat(),
                        "note": "พบความเชื่อมโยงระหว่างหัวข้อ"
                    })
        
        # 3. บันทึกการปรับปรุง
        improvements["adjustments"].extend(adjustments)
        self._save(self.improvements_path, improvements)
        
        print(f"📋 สร้างคำถามต่อ: {len(adjustments)} ข้อ")
        print(f"🔗 พบรูปแบบ/ความเชื่อมโยงใหม่: {len(improvements['patterns_found'])} รายการ")
        print("✅ ทบทวนและปรับตัวเสร็จสิ้น\n")
        return adjustments
    
    # ═══════════════════════════════════════════════════════════
    # 📊 ส่วนที่ 4: บันทึกผลลัพธ์และวิเคราะห์ความก้าวหน้า
    # ═══════════════════════════════════════════════════════════
    def record_cycle(self, cycle_name, outcome, notes=""):
        """บันทึกผลลัพธ์แต่ละรอบการเรียนรู้เพื่อพัฒนาต่อยอด"""
        cycles = self._load(self.cycles_path)
        
        cycle_record = {
            "cycle_id": cycles["total_cycles"] + 1,
            "name": cycle_name,
            "timestamp": datetime.now().isoformat(),
            "outcome": outcome,  # success / partial / failed
            "notes": notes,
            "stats": self.state.copy()
        }
        
        cycles["cycles"].append(cycle_record)
        cycles["total_cycles"] += 1
        self._save(self.cycles_path, cycles)
        
        print(f"📝 บันทึกรอบที่ {cycle_record['cycle_id']}: {cycle_name} → {outcome}")
        return cycle_record["cycle_id"]
    
    def get_progress_report(self):
        """สร้างรายงานความก้าวหน้าเพื่อพัฒนาต่อ"""
        questions = self._load(self.questions_path)
        knowledge = self._load(self.knowledge_path)
        cycles = self._load(self.cycles_path)
        
        pending = len(questions["pending"])
        answered = len(questions["answered"])
        total = pending + answered
        
        report = {
            "total_questions": total,
            "answered": answered,
            "pending": pending,
            "completion_rate": f"{(answered/total*100):.1f}%" if total > 0 else "0%",
            "knowledge_topics": len(knowledge["topics"]),
            "learning_cycles": cycles["total_cycles"],
            "curiosity_score": self.state["curiosity_level"],
            "knowledge_growth": self.state["knowledge_growth"]
        }
        return report
    
    # ═══════════════════════════════════════════════════════════
    # 🚀 รอบทำงานอัตโนมัติเต็มรูปแบบ
    # ═══════════════════════════════════════════════════════════
    def auto_cycle(self, new_topics=None):
        """
        รอบการทำงานอัตโนมัติ:
        สงสัย → เรียนรู้ → ทบทวน → ปรับปรุง → บันทึกผล
        """
        print("\n" + "█"*60)
        print("🔄 เริ่มรอบการเรียนรู้อัตโนมัติ")
        print("█"*60)
        
        # 1. สร้างความสงสัยจากหัวข้อใหม่
        if new_topics:
            print("\n📌 สร้างความสงสัยจากหัวข้อใหม่...")
            for topic in new_topics:
                self.generate_related_questions(topic, count=2)
        
        # 2. ทบทวนและถามต่อ
        self.reflect_and_adjust()
        
        # 3. บันทึกผลลัพธ์
        report = self.get_progress_report()
        cycle_id = self.record_cycle(
            cycle_name=f"Auto-Cycle {report['learning_cycles'] + 1}",
            outcome="completed",
            notes=f"ถาม:{report['total_questions']} ตอบ:{report['answered']} เรียนรู้:{report['knowledge_topics']} หัวข้อ"
        )
        
        # 4. แสดงผล
        print("\n" + "="*50)
        print("📊 รายงานความก้าวหน้า")
        print("="*50)
        for k, v in report.items():
            print(f"   {k}: {v}")
        print("="*50)
        print(f"✅ รอบที่ {cycle_id} เสร็จสมบูรณ์\n")
        return cycle_id


# ============================================================
# 🚀 เริ่มทำงาน
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("🧠 CURIOUS MIND — ระบบขี้สงสัย")
    print("  สงสัย → เรียนรู้ → จดจำ → ปรับตัวเอง → พัฒนาต่อ")
    print("="*60 + "\n")
    
    # สร้างระบบ
    mind = CuriousMind()
    
    # ── ตัวอย่างการใช้งาน ──
    print("📌 === ตัวอย่าง: เริ่มต้นด้วยความสงสัย ===")
    
    # 1. เริ่มจากการสงสัย
    q1 = mind.wonder("Vider คืออะไร?", context="หัวข้อหลักของระบบ", priority=3)
    q2 = mind.wonder("จุดประสงค์ของ Vider คืออะไร?", priority=2)
    
    # 2. เมื่อมีคำตอบ → บันทึกและเรียนรู้
    mind.learn_answer(q1, "Vider คือระบบที่รวบรวมและเชื่อมต่อความสามารถของเทคโนโลยีต่างๆ", confidence=0.95)
    mind.learn_answer(q2, "เพื่อให้แต่ละระบบทำงานร่วมกันได้ดียิ่งขึ้น", confidence=0.9)
    
    # 3. รอบอัตโนมัติ: ทบทวน → ถามต่อ → บันทึกผล
    mind.auto_cycle(new_topics=["การเรียนรู้", "ระบบอัตโนมัติ"])
    
    # 4. ดูรายงาน
    print("📂 ฐานความรู้ทั้งหมด:")
    knowledge = mind._load(mind.knowledge_path)
    for topic, data in knowledge["topics"].items():
        print(f"   • {topic}: {data['answer'][:50]}...")
    
    print("\n✨ พร้อมทำงานต่อแล้ว! เมื่อไหร่ก็ตามที่มีสิ่งใหม่ๆ ให้สงสัย")
    print("   ใช้ mind.wonder('คำถาม') แล้ว mind.learn_answer(id, 'คำตอบ')")
    print("   หรือ mind.auto_cycle(['หัวข้อ']) เพื่อรันทั้งระบบอัตโนมัติ")

