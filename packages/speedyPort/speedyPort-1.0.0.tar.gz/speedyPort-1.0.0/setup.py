# setup.py

from setuptools import setup, find_packages

setup(
    name="speedyPort",  # اسم الحزمة
    version="1.0.0",
    author="Error",
    author_email="",
    description="A simple web-based terminal interface using Flask.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",  # أضف الرابط إلى مستودع GitHub الخاص بك إذا كان لديك
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Flask>=2.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "speedy-port=speedyPort.app:run_app"  # الأمر لتشغيل التطبيق
        ]
    },
)
