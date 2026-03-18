import os
import json
from typing import List, Dict, Any
try:
    from .models import SpiritualLogos
    from .prompts import CORE_SYSTEM_PROMPT, SECTOR_SPECIFIC_GUIDES
except ImportError:
    from models import SpiritualLogos
    from prompts import CORE_SYSTEM_PROMPT, SECTOR_SPECIFIC_GUIDES

class SQARIPipeline:
    """
    Spiritual Quality AI (SQ-AI) RAG 파이프라인
    닌사호아 원주님의 철학을 바탕으로 다차원 메타데이터 필터링 및 추론을 수행합니다.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.data_path = os.path.join(os.path.dirname(__file__), 'data.json')
        self.knowledge_base: List[SpiritualLogos] = []
        self._load_data()

    def _load_data(self):
        """저장된 JSON 데이터를 로드합니다."""
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
                self.knowledge_base = [SpiritualLogos(**item) for item in raw_data]
            print(f"Loaded {len(self.knowledge_base)} items from knowledge base.")

    def analyze_query_intent(self, query: str) -> Dict[str, Any]:
        """
        사용자의 질문에서 에너지 섹터, 수련 단계 등 의도를 추출합니다.
        (실제 환경에서는 LLM 기반 Intent Classifier를 사용합니다)
        """
        intent = {
            "query": query,
            "detected_sector": None,
            "detected_stage": None
        }
        
        # 간단한 키워드 기반 의도 파악 예시
        if "무거워" in query or "짓눌려" in query or "1섹터" in query:
            intent["detected_sector"] = 1
            intent["detected_stage"] = "질서"
        elif "2섹터" in query or "나다" in query:
            intent["detected_sector"] = 2
            intent["detected_stage"] = "질서"
            
        return intent

    def search_with_metadata_filter(self, intent: Dict[str, Any]) -> List[SpiritualLogos]:
        """
        의도(Intent)에 기반하여 메타데이터 필터링을 동반한 검색을 수행합니다.
        """
        if not self.knowledge_base:
            return []
            
        # 메타데이터 기반 필터링 검색
        results = [
            item for item in self.knowledge_base
            if (intent["detected_sector"] is None or item.sector_number == intent["detected_sector"])
        ]
        
        # 간단한 키워드 매칭 추가 (실제로는 벡터 검색)
        query = intent["query"]
        if query:
            results = [
                item for item in results
                if any(kw in item.source_text for kw in query.split())
            ]
            
        return results[:3] # 상위 3개 반환

    def generate_spiritual_response(self, query: str, context: List[SpiritualLogos]) -> str:
        """
        검색된 문맥과 시스템 프롬프트를 조합하여 최종 답변을 생성합니다.
        """
        if not context:
            return "죄송합니다. 원주님의 로고스 아카이브에서 적절한 안내를 찾지 못했습니다. 마음을 고르고 다시 질문해 주십시오."

        # 시스템 프롬프트 및 섹터 가이드 획득
        sector_num = context[0].sector_number
        sector_guide = SECTOR_SPECIFIC_GUIDES.get(sector_num, "")
        
        # 문맥 데이터 결합 (최대 2개 정도가 적당)
        context_snippets = "\n".join([f"- {c.source_text}" for c in context[:2]])

        # 최종 응답 조립
        divider = "=" * 50
        response = f"""
{divider}
[SQ-AI: 안내자의 목소리]
{divider}

{sector_guide}

질문하신 내용과 관련하여 아카이브된 닌사호아 원주님의 로고스입니다:
{context_snippets}

이것은 "{context[0].core_theme}"의 질서 아래 일어나는 자연스러운 현상입니다.
불안해하지 마시고, {context[0].mantra_sound} 소리와 함께 호흡하며 존재의 질서를 느껴보십시오.

"질서와 균형과 조화 속에, 당신은 생명의 빛입니다."
{divider}
"""
        return response.strip()

    def run(self, query: str) -> str:
        """
        전체 파이프라인 실행 프로세스
        """
        try:
            # 1. 의도 분석
            intent = self.analyze_query_intent(query)
            
            # 2. 메타데이터 필터링 검색
            context = self.search_with_metadata_filter(intent)
            
            # 3. 영적 추론 및 답변 생성
            return self.generate_spiritual_response(query, context)
        except Exception as e:
            return f"알 수 없는 오류가 발생했습니다: {str(e)}. '질서'의 마음으로 시스템을 다시 점검해 주세요."

# 테스트 실행
if __name__ == "__main__":
    pipeline = SQARIPipeline()
    test_queries = [
        "1섹터 수련 중인데 몸이 너무 무겁고 짓눌려요.",
        "나는 나 스스로 존재하는 나다... 2섹터에 대해 알려줘."
    ]
    for q in test_queries:
        print(f"\n[USER]: {q}")
        print(pipeline.run(q))
