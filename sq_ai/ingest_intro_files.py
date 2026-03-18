import os
import json
import re
from typing import List
from models import SpiritualLogos

def ingest_files(file_paths: List[str]):
    all_logos = []
    
    for path in file_paths:
        if not os.path.exists(path):
            print(f"File not found: {path}")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 간단한 섹션별 분절 (실제로는 더 정교한 NLP 모델을 사용하게 됩니다)
        # 예시: "제1섹터", "제2섹터" 등 키워드 기준 분절
        sections = re.split(r'(제\s?[0-9]\s?섹터|삼율 호흡|회로도 상징)', content)
        
        current_title = ""
        for i, part in enumerate(sections):
            if i % 2 == 1:
                current_title = part
                continue
            
            text = part.strip()
            if len(text) < 50: continue # 너무 짧은 텍스트 제외
            
            # 메타데이터 추론 (Rule-based)
            sector_match = re.search(r'제\s?([0-9])\s?섹터', current_title)
            sector_num = int(sector_match.group(1)) if sector_match else 0
            
            color = "Unknown"
            if sector_num == 1: color = "Red"
            elif sector_num == 2: color = "Orange"
            
            logos = SpiritualLogos(
                source_text=f"[{current_title}] {text[:500]}...", # 텍스트 일부
                training_stage="질서" if "질서" in text else "균형",
                sector_number=sector_num,
                color_frequency=color,
                mantra_sound="오~" if sector_num == 1 else "아~",
                core_theme=f"{current_title}에 관한 안내",
                body_anchor="미골" if sector_num == 1 else "하단전",
                expected_feedback=["접지"] if sector_num == 1 else ["균형"]
            )
            all_logos.append(logos.dict())
            
    # JSON 파일로 저장
    output_path = r'd:\페르미아\가람\sq_ai\data.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_logos, f, ensure_ascii=False, indent=4)
        
    print(f"Successfully ingested {len(all_logos)} items to {output_path}")

if __name__ == "__main__":
    base_path = r'd:\페르미아\가람\회로도관련'
    # 000부터 006까지 포함하도록 수정
    files = [os.path.join(base_path, f"회로도소개 - {str(i).zfill(3)}.txt") for i in range(7)]
    ingest_files(files)
