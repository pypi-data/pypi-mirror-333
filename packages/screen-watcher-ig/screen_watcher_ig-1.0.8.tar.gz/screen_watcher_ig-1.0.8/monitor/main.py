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

# ✅ 최상위 디렉터리를 import 가능하도록 경로 추가
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from .configp import load_config  # ✅ 이제 `configp.py`를 찾을 수 있음

# ✅ 기존 코드 유지: 전역 변수 및 초기 설정
start_pos = None
end_pos = None
mute_sound = False  
stop_program = False  
reset_alert = False  
detection_state = "normal"  # ✅ 'normal' → 감지중, 'alert' → 감지됨!

region = (0, 0, 100, 100)

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
            global region
            region = (min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), width, height)
            print(f"✅ 선택한 영역: {region}")
            print(f"\n📸 감지를 시작합니다... {sleep_interval}초마다 화면을 체크합니다.")
            return False

# ✅ 기존 코드 유지: 화면 캡처 및 감지 기능
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

# ✅ 메인 실행 함수 추가 (패키지 실행 가능하게 변경)
def main():
    global sleep_interval, detection_threshold

    # ✅ 설정 불러오기
    config = load_config()
    sleep_interval = config["detection_interval"]
    detection_threshold = config["detection_threshold"]

    print(f"\n📸 감지를 시작합니다... {sleep_interval}초마다 화면을 체크합니다.")

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

# ✅ 패키지 실행 가능하도록 변경
if __name__ == "__main__":
    main()

