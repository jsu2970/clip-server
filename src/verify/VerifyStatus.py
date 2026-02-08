# 정성우

from enum import Enum

# 사진 검증 결과를 가진 enum 클래스이다.
class VerifyStatus(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    FAIL = "FAIL"