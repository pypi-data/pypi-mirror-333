from setuptools import setup, find_packages

setup(
    name="asicloud",                    # Paket nomi (noyob bo‘lishi kerak)
    version="0.1.21",                    # Versiya (keyin yangilashingiz mumkin)
    packages=find_packages(),           # Avtomatik barcha modullarni topadi
    install_requires=["requests"],      # Qo‘shimcha kutubxonalar
    author="Asliddin",                  # Sizning ismingiz
    author_email="erdanayevasliddin@gmail.com",   # Emailingiz
    description="Sun’iy intellekt uchun shaxsiy kutubxona",  # Qisqa tavsif
    long_description=open("README.md").read(),              # To‘liq tavsif
    long_description_content_type="text/markdown",          # README formati
    url="https://t.me/itstimebeyond",            # GitHub havolasi (agar bo‘lsa)
    license="MIT",                                          # Litsenziya
    classifiers=[                                           # Qo‘shimcha ma’lumot
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                                # Minimal Python versiyasi
)