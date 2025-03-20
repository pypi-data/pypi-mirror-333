from setuptools import setup, find_packages

setup(
    name="library_utils",
    version="0.1.6",
    author="x24142816-JiyoungKim",
    author_email="x24142816@student.ncirl.ie",
    description="A collection of utility functions for AWS services",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jiyoung0716/Final_CPP_Project",
    packages=find_packages(include=["time_tracker.utils", "time_tracker.utils.*"]),  # ✅ utils 폴더 포함
    package_dir={"time_tracker.utils": "time_tracker/utils"},  # ✅ 패키지 디렉토리 명확하게 설정
    include_package_data=True,  # ✅ 모든 패키지 파일 포함
    install_requires=[
        'boto3==1.37.8',
        'botocore==1.37.8',
        'Django==4.2.19',
        'setuptools==59.6.0',
        'gunicorn==23.0.0',
        'Pillow==11.1.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
