from setuptools import setup, find_packages

setup(
    name="gpus",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "nvidia-ml-py",
        "click",
        "flask",
        "flask-socketio",
        "eventlet",  # For WebSocket support
        "python-engineio>=4.0.0",
        "python-socketio>=5.0.0",
        "psutil",    # For process management
    ],
    entry_points={
        'console_scripts': [
            'gpus=gpus.cli:cli',
        ],
    },
    include_package_data=True,
    package_data={
        'gpus': [
            'templates/*.html',
            'static/css/*.css',
            'static/js/*.js',
        ],
    },
    python_requires='>=3.6',
    description="A web interface for monitoring NVIDIA GPU status",
    author="GPU Monitor Team",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)