# 정성우

from typing import Dict, Any

from app.verify.VerifyService import map_title_to_categories

"""
챌린지 제목을 받아서 사진 자동 검증 가능 여부를 판단하는 서비스이다.
"""
class ChallengePreviewService:
    def preview(self, title: str) -> Dict[str, Any]:
        # 제목과 유사한 카테고리를 검색한다.
        categories = map_title_to_categories(title) 

        # 검색된 카테고리가 generic이 아니라면 true를 저장한다. 즉 generic이면 사진 검증이 불가능하다.
        auto_verifiable = categories != ["generic"]

        return {
            "title": title,
            "categories": categories,
            "autoVerifiable": auto_verifiable,
            "reason": (
                "사진으로 자동 판별 가능한 챌린지입니다."
                if auto_verifiable
                else "사진으로 자동 판별하기 어려운 챌린지입니다."
            ),
        }