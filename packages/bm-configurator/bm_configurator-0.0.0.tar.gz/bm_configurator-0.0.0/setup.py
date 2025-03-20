from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bm_configurator",
    version="0.0.0",
    author="Dmatryus Datry",
    author_email="dmatryus.sqrt49@yandex.ru",
    description="The configurator allows you to collect knowledge about models in configs and select among them suitable for local deployment on certain devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dmatryus/bm_configurator",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        'PyYAML>=5.4',
        'psutil>=5.8',
        'nvidia-ml-py>=12.535.77'  # Для совместимости с nvidia-smi
    ]
)