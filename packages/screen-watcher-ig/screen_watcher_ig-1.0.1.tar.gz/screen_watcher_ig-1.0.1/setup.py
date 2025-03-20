import os
from setuptools import setup, find_packages

# ✅ README.md 파일이 없을 때 기본값 제공
long_description = "Screen Watcher IG: 화면 변경 감지 프로그램"
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="screen-watcher-ig",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "pynput",
        "pyobjc-framework-Quartz",
        "pync"
    ],
    entry_points={
        "console_scripts": [
            "monitor=monitor.monitor:main"
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
