import random
import string
import pyperclip
from zxcvbn import zxcvbn  # zxcvbn 함수 사용

# ----------------------------------------------------------------------
# 비밀번호 강도 체크 함수
# zxcvbn 라이브러리의 zxcvbn 함수를 사용하여 비밀번호 강도 점수를 평가합니다.
# 강도 점수는 0 (매우 약함) 부터 4 (매우 강함)까지 있습니다.
# ----------------------------------------------------------------------
def check_password_strength(password):
    result = zxcvbn(password)  # 비밀번호 강도 분석
    return result['score']  # 비밀번호 강도 점수 반환 (0~4)

# ----------------------------------------------------------------------
# 비밀번호 생성 함수
# 사용자 입력에 따라 비밀번호를 생성하고, 강도를 평가합니다.
# 복잡도, 문자 포함/제외 옵션을 설정하여 비밀번호를 랜덤으로 생성합니다.
# ----------------------------------------------------------------------
def generate_random_password(length=12, complexity="medium", include_upper=True, include_lower=True, include_digits=True, include_special=True, contains=None, excludes=None):
    # 사용할 수 있는 문자 집합 초기화
    characters = ""

    # ------------------------------------------------------------------
    # 복잡도 설정에 따른 문자 집합 결정
    # 복잡도에 맞춰 선택한 문자 종류들을 characters에 추가합니다.
    # ------------------------------------------------------------------
    if complexity == "low":
        if include_lower:
            characters += string.ascii_lowercase  # 소문자 추가
        if include_digits:
            characters += string.digits  # 숫자 추가
    elif complexity == "medium":
        if include_upper:
            characters += string.ascii_uppercase  # 대문자 추가
        if include_lower:
            characters += string.ascii_lowercase  # 소문자 추가
        if include_digits:
            characters += string.digits  # 숫자 추가
    elif complexity == "high":
        if include_upper:
            characters += string.ascii_uppercase  # 대문자 추가
        if include_lower:
            characters += string.ascii_lowercase  # 소문자 추가
        if include_digits:
            characters += string.digits  # 숫자 추가
        if include_special:
            characters += string.punctuation  # 특수문자 추가

    # ------------------------------------------------------------------
    # 사용자 맞춤형 설정
    # 포함하고 싶은 문자가 있으면 contains에 추가합니다.
    # 제외할 문자가 있으면 excludes에서 제거합니다.
    # ------------------------------------------------------------------
    if contains:
        characters += contains  # 포함할 문자가 있으면 문자 집합에 추가
    if excludes:
        characters = ''.join(c for c in characters if c not in excludes)  # 제외할 문자가 있으면 문자 집합에서 제거

    # ------------------------------------------------------------------
    # 문자 집합이 비어있으면 오류 발생
    # 사용자가 문자 집합을 선택하지 않으면 ValueError를 발생시킵니다.
    # ------------------------------------------------------------------
    if not characters:
        raise ValueError("At least one character type must be selected.")  # 최소한 하나의 문자 집합을 선택해야 합니다.

    # ------------------------------------------------------------------
    # 랜덤하게 비밀번호 생성
    # 문자 집합에서 랜덤으로 문자를 선택하여 비밀번호를 생성합니다.
    # ------------------------------------------------------------------
    password = ''.join(random.choice(characters) for _ in range(length))

    # ------------------------------------------------------------------
    # 비밀번호 강도 체크
    # 생성된 비밀번호의 강도를 체크하여 강도 레벨을 반환합니다.
    # ------------------------------------------------------------------
    strength = check_password_strength(password)
    strength_label = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"][strength]  # 강도에 따른 레벨 이름 매핑
    
    return password, strength_label  # 생성된 비밀번호와 강도 레벨 반환

# ----------------------------------------------------------------------
# 비밀번호 자동 저장 (클립보드에 복사)
# 비밀번호를 클립보드에 복사하여 사용자가 쉽게 붙여넣을 수 있도록 합니다.
# ----------------------------------------------------------------------
def copy_to_clipboard(password):
    pyperclip.copy(password)  # 비밀번호를 클립보드에 복사
    print("비밀번호가 클립보드에 복사되었습니다.")  # 복사 완료 메시지 출력

# ----------------------------------------------------------------------
# 사용자 입력 받기
# 비밀번호 생성에 필요한 각종 옵션을 사용자로부터 입력받습니다.
# ----------------------------------------------------------------------
length = int(input("비밀번호 길이를 입력하세요: "))  # 비밀번호 길이 입력
complexity = input("복잡도 설정 (low, medium, high): ").strip().lower()  # 복잡도 선택
include_upper = input("대문자를 포함하시겠습니까? (y/n): ").strip().lower() == "y"  # 대문자 포함 여부
include_lower = input("소문자를 포함하시겠습니까? (y/n): ").strip().lower() == "y"  # 소문자 포함 여부
include_digits = input("숫자를 포함하시겠습니까? (y/n): ").strip().lower() == "y"  # 숫자 포함 여부
include_special = input("특수문자를 포함하시겠습니까? (y/n): ").strip().lower() == "y"  # 특수문자 포함 여부
contains = input("포함할 문자가 있으면 입력하세요 (예: !@#): ").strip()  # 포함할 문자
excludes = input("제외할 문자가 있으면 입력하세요: ").strip()  # 제외할 문자

# ----------------------------------------------------------------------
# 비밀번호 생성 및 강도 평가
# 사용자 입력을 바탕으로 비밀번호를 생성하고 강도를 평가합니다.
# ----------------------------------------------------------------------
password, strength_label = generate_random_password(
    length=length, complexity=complexity, include_upper=include_upper,
    include_lower=include_lower, include_digits=include_digits,
    include_special=include_special, contains=contains, excludes=excludes
)

# ----------------------------------------------------------------------
# 결과 출력
# 생성된 비밀번호와 비밀번호 강도를 출력합니다.
# ----------------------------------------------------------------------
print(f"생성된 비밀번호: {password}")
print(f"비밀번호 강도: {strength_label}")

# ----------------------------------------------------------------------
# 비밀번호 클립보드에 자동 복사
# 생성된 비밀번호를 클립보드에 복사하여 사용자가 쉽게 붙여넣을 수 있도록 합니다.
# ----------------------------------------------------------------------
copy_to_clipboard(password)