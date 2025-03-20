import cv2
import numpy as np
import time
import ctypes
import threading
import os
import sys
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
from pync import Notifier
from pynput import mouse, keyboard

# ✅ 설정 파일을 올바르게 참조
from .configp import load_config  

config = load_config()

# ✅ 설정 불러오기
sleep_interval = config["detection_interval"]
detection_threshold = config["detection_threshold"]

print(f"📸 감지를 시작합니다... {sleep_interval}초마다 화면을 체크합니다.")

# 1️⃣ 마우스 클릭으로 감지할 화면 영역 선택
start_pos = None
end_pos = None
mute_sound = False  
stop_program = False  
reset_alert = False  
detection_state = "normal"  # ✅ 'normal' → 감지중, 'alert' → 감지됨!

region = (0, 0, 100, 100)  # 기본 감지 영역

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

def capture_region(region):
    x, y, w, h = region
    rect = CGRectMake(x, y, w, h)
    return CGWindowListCreateImage(rect, kCGWindowListOptionOnScreenOnly, kCGNullWindowID, kCGWindowImageBoundsIgnoreFraming)

def image_to_array(image):
    width = CGImageGetWidth(image)
    height = CGImageGetHeight(image)
    data = CGDataProviderCopyData(CGImageGetDataProvider(image))
    byte_data = memoryview(data).tobytes()

    expected_size = width * height * 4
    if len(byte_data) > expected_size:
        byte_data = byte_data[:expected_size]

    try:
        img_array = np.frombuffer(byte_data, dtype=np.uint8).reshape((height, width, 4))
    except ValueError:
        print(f"❌ 오류: 예상 크기({expected_size} bytes)와 실제 크기({len(byte_data)} bytes)가 일치하지 않음.")
        return None

    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGRA2RGB)
    return img_array

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
    global region, detection_state, reset_alert, stop_program

    print("🖱️ 마우스로 감지할 화면의 좌측 상단과 우측 하단을 차례로 클릭하세요.")

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()  

    if region == (0, 0, 100, 100):
        print("❌ 오류: 감지할 영역이 설정되지 않았습니다. 프로그램을 다시 실행하세요.")
        sys.exit(1)

    print(f"\n📸 감지를 시작합니다... {sleep_interval}초마다 화면을 체크합니다.")

    prev_image = image_to_array(capture_region(region))

    threading.Thread(target=lambda: keyboard.Listener(on_press=on_key_press).start(), daemon=True).start()

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

