from setuptools import setup, find_packages
import disk_monitor

setup(
    name="disk_monitor_aureldevops",
    version=disk_monitor.__version__,
    author=disk_monitor.__author__,
    author_email=disk_monitor.__author_email__,
    description="Module de surveillance d'espace disque pour Linux",
    long_description="Un module Python pour surveiller l'espace disque et déclencher des alertes.",
    long_description_content_type="text/markdown",
    url="https://github.com/votrecompte/disk_monitor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)