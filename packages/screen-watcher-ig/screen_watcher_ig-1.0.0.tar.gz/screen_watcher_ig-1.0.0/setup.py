from setuptools import setup, find_packages

setup(
    name="screen-watcher-ig",  # ✅ PyPI 패키지 이름
    version="1.0.0",
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
            "monitor=monitor.monitor:main"  # ✅ 터미널에서 `monitor` 명령 실행 가능
        ]
    },
    author="Your Name",
    author_email="your_email@example.com",
    description="화면 변경 감지 모니터링 프로그램",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/screen-watcher-ig",  # ✅ GitHub 저장소 URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS"
    ],
    python_requires=">=3.6",
)

