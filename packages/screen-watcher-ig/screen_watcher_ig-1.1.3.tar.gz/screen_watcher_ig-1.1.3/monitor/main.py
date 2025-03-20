import argparse
import threading
import time
import numpy as np
import sys
import cv2
from pync import Notifier
from pynput import mouse, keyboard
from Quartz import (
    CGWindowListCreateImage,
    kCGWindowListOptionOnScreenOnly,
    kCGNullWindowID,
    kCGWindowImageBoundsIgnoreFraming,
    CGRectMake,
    CGImageGetWidth,
    CGImageGetHeight,
    CGDataProviderCopyData,
    CGImageGetDataProvider,
    CFDataGetBytePtr,
    CFDataGetLength
)
from .configp import load_config, save_config  

# ✅ 설정 불러오기
config = load_config()
sleep_interval = config["detection_interval"]
detection_threshold = config["detection_threshold"]

# ✅ 글로벌 변수 선언
start_pos = None
end_pos = None
mute_sound = False  
stop_program = False  
reset_alert = False  
detection_state = "normal"  # 'normal' → 감지중, 'alert' → 감지됨!

region = None  # ✅ region 초기화 (None으로 설정해 오류 방지)

# ✅ 마우스로 감지할 영역 설정
def on_click(x, y, button, pressed):
    global start_pos, end_pos, region
    if pressed:
        if start_pos is None:
            start_pos = (int(x), int(y))
            print(f"📍 시작 좌표: {start_pos}")
        else:
            end_pos = (int(x), int(y))
            width = abs(end_pos[0] - start_pos[0])
            height = abs(end_pos[1] - start_pos[1])
            region = (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), width, height)
            print(f"✅ 선택한 영역: {region}")
            return False  # 마우스 리스너 종료

# ✅ 설정 변경 기능 추가
def configure_settings():
    """사용자가 설정을 변경할 수 있도록 인터페이스 제공"""
    config = load_config()

    print("\n🔧 설정 변경 (값을 입력하지 않으면 기존 값 유지)")

    try:
        new_interval = input(f"⏳ 감지 간격(기본값: {config['detection_interval']}) (초): ").strip()
        if new_interval.isdigit():
            config["detection_interval"] = int(new_interval)

        new_threshold = input(f"🎚️ 감지 민감도(기본값: {config['detection_threshold']}) : ").strip()
        if new_threshold.isdigit():
            config["detection_threshold"] = int(new_threshold)

        save_config(config)  
        print("\n✅ 설정이 저장되었습니다!")

    except ValueError:
        print("❌ 잘못된 입력입니다. 숫자만 입력해주세요.")

# ✅ 키보드 입력 처리 (알림 끄기, 프로그램 종료)
def on_key_press(key):
    global mute_sound, stop_program, reset_alert
    try:
        if key.char == '0':  
            stop_program = True
            print("🛑 프로그램 종료 중...")
            return False  
        elif key.char == '1':  
            reset_alert = True
            print("🔄 감지 초기화 중...")
    except AttributeError:
        pass

# ✅ 메인 실행 함수
def main():
    global region, detection_state, reset_alert, stop_program, sleep_interval, detection_threshold

    parser = argparse.ArgumentParser(description="Screen Watcher 설정 및 실행")
    parser.add_argument("--config", action="store_true", help="설정을 변경합니다.")
    args = parser.parse_args()

    if args.config:
        configure_settings()
        return

    print("🖱️ 마우스로 감지할 화면의 좌측 상단과 우측 하단을 차례로 클릭하세요.")

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()  

    if region is None:
        print("❌ 오류: 감지할 영역이 설정되지 않았습니다. 프로그램을 다시 실행하세요.")
        sys.exit(1)

    print(f"\n📸 감지를 시작합니다... {sleep_interval}초마다 화면을 체크합니다.")

    threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press).start(), daemon=True).start()

    prev_image = image_to_array(capture_region(region))

    while not stop_program:
        if reset_alert:
            prev_image = image_to_array(capture_region(region))
            reset_alert = False
            print("\n✅ 감지 초기화 완료. 감지를 다시 시작합니다.")

        time.sleep(sleep_interval)
        curr_image = image_to_array(capture_region(region))

        if prev_image is None or curr_image is None:
            continue  

        if np.sum(np.abs(curr_image - prev_image)) > detection_threshold:
            detection_state = "alert"
            while not stop_program and not reset_alert:
                Notifier.notify("⚠️ 화면 변경 감지됨!", title="Screen Watcher", sound="default")
                time.sleep(3)
            detection_state = "normal"
            prev_image = curr_image  

if __name__ == "__main__":
    main()

