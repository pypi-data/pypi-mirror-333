import json
import os

# ✅ 설정 저장 파일
CONFIG_FILE = "config.json"

# ✅ 기본 권장 값 (monitor.py 기준)
default_recommended = {
    "sound_volume": 100,  # 🔊 권장 벨소리 크기
    "detection_interval": 20,  # ⏳ 권장 감지 간격 (초)
    "detection_threshold": 5000  # 📸 권장 감지 민감도
}

# ✅ 설정 저장 함수
def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print("\n✅ 설정이 저장되었습니다.")

# ✅ 설정 불러오기 함수
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return default_recommended  # 파일이 없으면 권장 값 사용

# ✅ 설정 변경 함수 (권장 값 + 범위 + 현재 값 표시)
def update_config():
    config = load_config()

    print("\n🔧 설정 변경 (값을 입력하지 않으면 현재 값 유지)")

    try:
        # 🔊 벨소리 크기 설정
        new_sound_volume = input(f"🔊 벨소리 크기 (기본값: {default_recommended['sound_volume']}, 범위: 0~100) [현재 값: {config['sound_volume']}]: ").strip()
        if new_sound_volume:
            config["sound_volume"] = int(new_sound_volume)

        # ⏳ 감지 간격 설정
        new_detection_interval = input(f"⏳ 감지 간격 (기본값: {default_recommended['detection_interval']}, 초 단위) [현재 값: {config['detection_interval']}]: ").strip()
        if new_detection_interval:
            config["detection_interval"] = int(new_detection_interval)

        # 📸 감지 민감도 설정
        new_detection_threshold = input(f"📸 감지 민감도 (기본값: {default_recommended['detection_threshold']}, 값이 낮을수록 민감) [현재 값: {config['detection_threshold']}]: ").strip()
        if new_detection_threshold:
            config["detection_threshold"] = int(new_detection_threshold)

        save_config(config)

    except ValueError:
        print("❌ 잘못된 입력입니다. 숫자만 입력해주세요.")

# ✅ monitor --config 명령어로 실행 가능하도록 처리
if __name__ == "__main__":
    update_config()
