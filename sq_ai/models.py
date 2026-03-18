from pydantic import BaseModel, Field
from typing import List, Optional

class SpiritualLogos(BaseModel):
    """
    닌사호아 원주님의 로고스 데이터를 다차원 에너지 구조로 정의하는 핵심 스키마
    """
    # 1. 원본 데이터
    source_text: str = Field(..., description="원주님 말씀 원문 및 대화 내용")
    
    # 2. 수련 주기 및 층위 (Order, Balance, Harmony)
    training_stage: str = Field(..., description="예: 질서 과정(63일), 균형 과정(63일), 조화 과정")
    
    # 3. 에너지 섹터 및 주파수 매핑
    sector_number: int = Field(..., description="1~9 섹터 번호 (예: 1)")
    color_frequency: str = Field(..., description="주파수 색상 (예: Red)")
    solfeggio_hz: Optional[str] = Field(None, description="솔페지오 주파수 (예: 396Hz, Do)")
    
    # 4. 실천적 수련 도구
    mantra_sound: str = Field(..., description="관련 소리/진언 (예: 오~, 훔-아-옴 3부 호흡)")
    core_theme: str = Field(..., description="주제어 (예: 생명의 빛의 질서 속에 나는 존재한다)")
    
    # 5. 에너지 작용점 및 현상
    body_anchor: str = Field(..., description="인체 작용 지점 (예: 하단전, 꼬리뼈, 미골)")
    expected_feedback: List[str] = Field(default_factory=list, description="예상되는 수련 현상 (예: 무거움, 짓눌림, 접지 현상)")

    class Config:
        schema_extra = {
            "example": {
                "source_text": "제1섹터 수련 시 몸이 무겁게 느껴지는 것은 지구와의 접지입니다.",
                "training_stage": "질서 과정(63일)",
                "sector_number": 1,
                "color_frequency": "Red",
                "solfeggio_hz": "396Hz",
                "mantra_sound": "오~",
                "core_theme": "생명의 빛의 질서 속에 나는 존재한다",
                "body_anchor": "미골 (꼬리뼈)",
                "expected_feedback": ["무거움", "짓눌림", "강력한 접지"]
            }
        }
