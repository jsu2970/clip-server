# 정성우

import re
from typing import List

"""
텍스트를 정규화 하기 위한 함수이다.
대소문자, 공백 차이를 제거하여 키워드 매칭을 안정적으로 하기 위한 전처리이다.
"""
def _normalize_text(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s

"""
규칙 기반으로 카테고리를 분류하는 함수이다. 
매개변수로 챌린지 제목을 받아서 챌린지 제목에 특정 키워드가 포함되면 카테고리를 부여한다. 여러 카테고리가 매칭되면 전부 반환하며, 상위 1~2개로 제한하는 것도 가능하다.
"""
def map_title_to_categories(title: str) -> List[str]:
    t = _normalize_text(title)  # 챌린지 제목을 정규화 한다.

    # 매칭된 카테고리를 담는 리스트이다.
    matched = [] 
    # 각 카테고리의 키워드를 순회하며 하나라도 포함되면 카테고리를 매칭한다. 다중 카테고리를 허용한다.
    for cat, kws in CATEGORY_KEYWORDS.items():  # cat: 키값 (fitness), kws: 키워드 값 (운동, 헬스 ...)
        for kw in kws:  # 카테고리의 키워드 리스트를 하나씩 꺼낸다. (운동, 헬스, 다이어트 등)
            if _normalize_text(kw) in t:  # 챌린지 제목에 키워드 값이 포함되는지 검사한다.
                matched.append(cat)
                break

    if not matched:  # 매칭되는 카테고리가 하나도 없다면 generic으로 매칭한다.
        return ["generic"]

    # 너무 많은 카테고리가 걸리면 우선순위에 따라 개수를 제한한다. 카테고리 순서를 다르게 하므로써 우선순위를 바꿀 수 있다.
    return matched[:2]  # 2개로 제한한다.

"""
프롬프트 파일의 목적은 한국어로 들어오는 챌린지 제목을, CLIP이 잘 비교할 수 있는 ‘시각적 영어 문장 세트’로 변환하는 역할이다.

카테고리 프롬프트는 CLIP용 텍스트 후보 집합이다.
CLIP는 이미지 임베딩과 텍스트 임베딩을 통해 유사도를 비교하는데, 추상 키워드보다 시각적으로 관찰 가능한 문장을 더 안정적으로 생성한다.
따라서 추상적인 키워드가 들어오면 해당 키워드를 가장 관찰 가능한 문장으로 바꾸는 역할이다.
"""
CATEGORY_PROMPTS = {
    "fitness": [
        "a person exercising",
        "a person working out in a gym",
        "a person lifting weights",
        "a person running outdoors",
        "fitness training scene",
        "sportswear in a gym",
    ],
    "study": [
        "a person studying at a desk",
        "a person reading a book",
        "a laptop on a desk",
        "a notebook and pen on a desk",
        "a study environment indoors",
    ],
    "cleaning": [
        "a person cleaning a room",
        "a person tidying up a desk",
        "a clean and organized room",
        "cleaning supplies in a home",
    ],
    "food": [
        "a healthy meal on a table",
        "a home-cooked meal",
        "a salad in a bowl",
        "food on a dining table",
    ],
    "outdoor": [
        "a person walking outdoors",
        "a street scene outdoors",
        "a person hiking",
        "a park outdoors",
    ],
    # 매핑 실패 시 fallback으로 키워드 매칭이 실패했을 때, 서버가 죽지 않도록 해준다.
    "generic": [
        "a photo of a person",  # 그냥 사람이 찍힌 사진
        "a photo taken indoors",  # 실내 사진
        "a photo taken outdoors",  # 야외 사진
        "a photo of an object",  # 사람없이 사물만 있는 사진
    ],
}
"""
한국어 기준 규칙 기반 키워드 매핑이다. 서비스 특성에 맞게 계속 보강하는 데이터(룰)이다.
해당 딕셔너리는 텍스트 분류기 역할을 수행한다.
사용자 챌린지 제목이 한국어로 들어오면, 출력으로 위 코드인 카테고리 레벨의 fitness, study 등을 내보낸다.
즉 자유 텍스트인 챌린지 제목을 소수의 고정된 카테고리로 매핑하기 위해 사용한다.
"""
CATEGORY_KEYWORDS = {
    "fitness": ["운동", "헬스", "러닝", "달리기", "조깅", "요가", "필라테스", "스트레칭", "다이어트", "체중", "웨이트", "몸무계"],
    "study": ["공부", "독서", "책", "코딩", "과제", "자격증", "학습", "스터디", "리딩", "복습"],
    "cleaning": ["청소", "정리", "정돈", "설거지", "방청소", "정리정돈"],
    "food": ["식단", "요리", "건강식", "샐러드", "금주", "음식", "간식", "물마시기", "물 마시기"],
    "outdoor": ["산책", "등산", "여행", "출근", "외출", "걷기", "하이킹"],
}