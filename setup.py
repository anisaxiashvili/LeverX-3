
from setuptools import setup, find_packages

setup(
    name="mysql-student-room-manager",
    version="2.0.0",
    description="Enterprise MySQL solution for student-room analytics with query optimization",
    packages=find_packages(),
    install_requires=[
        "mysql-connector-python>=8.0.33",
        "tabulate>=0.9.0"
    ],
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'student-room-manager=mysql_student_room_manager.main:main',
        ],
    },
    author="MySQL Student Room Analytics Team",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8+",
    ]
)
