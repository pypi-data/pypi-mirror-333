import argparse
import threading
import time
import numpy as np
import sys
import cv2
import itertools
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
sound_volume = config["sound_volume"]

# ✅ 글로벌 변수 선언
start_pos = None
end_pos = None
mute_sound = False  
stop_program = False  
reset_alert = False  
detection_state = "normal"  # 'normal' → 감지중, 'alert' → 감지됨!

region = None  # ✅ region 초기화 (None으로 설정해 오류 방지)

# ✅ 감지 애니메이션
def display_status():
    symbols = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_program:
        if detection_state == "normal":
            sys.stdout.write(f"\r🟢 감지중 {next(symbols)} : ")
        else:
            sys.stdout.write(f"\r🛑 감지됨! {next(symbols)} : ")
        sys.stdout.flush()
        time.sleep(0.5)

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

# ✅ 키보드 입력 처리 (알림 끄기, 프로그램 종료)
def on_key_press(key):
    global mute_sound, stop_program, reset_alert
    try:
        if key.char == '0':  
            stop_program = True
            print("\n🛑 프로그램 종료 중...")
            sys.exit(0)  # ✅ 즉시 프로그램 종료
        elif key.char == '1':  
            reset_alert = True
            print("\n🔄 감지 초기화 중...")
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
        print("\n❌ 오류: 감지할 영역이 설정되지 않았습니다. 프로그램을 다시 실행하세요.")
        sys.exit(1)

    print(f"\n📸 감지를 시작합니다... {sleep_interval}초마다 화면을 체크합니다.")
    
    # ✅ 감지 애니메이션 시작
    threading.Thread(target=display_status, daemon=True).start()

    prev_image = image_to_array(capture_region(region))

    # ✅ 키보드 리스너 실행 (0: 종료, 1: 초기화)
    keyboard_listener = threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press).start(), daemon=True)
    keyboard_listener.start()

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
                Notifier.notify("⚠️ 화면 변경 감지됨!", title="Screen Watcher", sound="default" if not mute_sound else None)
                time.sleep(3)
            detection_state = "normal"
            prev_image = curr_image  

if __name__ == "__main__":
    main()

