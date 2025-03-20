from setuptools import setup, find_packages

# قراءة محتوى README لاستخدامه كـ long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="veilgen",  # اسم الأداة على PyPI
    version="1.0.0",  # رقم الإصدار
    packages=find_packages(),  # البحث تلقائيًا عن جميع الحزم الفرعية
    install_requires=[
        "rich",
        "cryptography",
        "faker",
    ],  # المكتبات المطلوبة للأداة
    include_package_data=True,  # تضمين الملفات غير البرمجية (إن وجدت)
    author="hexa-01",
    author_email="veilgen@proton.me",
    description="A powerful tool for generating fake data for cybersecurity testing and development.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hexa-01/Veilgen-Master",  # رابط المستودع على GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # الحد الأدنى من إصدار Python المدعوم
    entry_points={
        "console_scripts": [
            "veilgen=veilgen.veilgen:main",  # تشغيل الأداة من سطر الأوامر
        ]
    },
)
