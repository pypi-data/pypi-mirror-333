
from setuptools import setup, find_packages

setup(
    name="OMER_AKER",
    version="1.0.0",
    author="Omer Aker",
    description="مكتبة رؤية حاسوبية متكاملة تشمل تتبع اليد، رسم الهيكل، وتحليل الصور.",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
