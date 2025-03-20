import os
from setuptools import setup, find_packages

# ✅ README.md 절대 경로 지정
this_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_directory, "README.md")

# ✅ README.md 파일이 없으면 기본값 제공
long_description = "Screen Watcher IG: 화면 변경 감지 프로그램"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="screen-watcher-ig",
    version="1.1.5",  # ✅ 버전 업데이트 필수
    packages=find_packages(include=["monitor"]),
    package_data={"monitor": ["configp.py"]},  # ✅ configp.py 파일 포함
    include_package_data=True,  # ✅ 필요 없는 파일이 자동 포함되지 않도록 설정
    install_requires=[
        "numpy",
        "opencv-python",
        "pynput",
        "pyobjc-framework-Quartz",
        "pync"
    ],
    entry_points={
        "console_scripts": [
            "monitor=monitor.main:main"
        ]
    },
    author="rudclthe",
    author_email="your_email@example.com",
    description="화면 변경 감지 모니터링 프로그램",
    long_description=long_description,  # ✅ README.md가 없으면 기본값 사용
    long_description_content_type="text/markdown",
    url="https://github.com/rudclthe/screen-watcher-ig",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS"
    ],
    python_requires=">=3.6",
)
