from setuptools import setup, find_packages
import os

# Read README.md content
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="amr_x2_pose",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe",
        "numpy",
        "matplotlib",
        "filterpy",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="AMR",
    author_email="your.email@example.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: OS Independent",
    ],
    keywords="pose-estimation 3d-pose mediapipe computer-vision",
    python_requires=">=3.8",
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'amr_x2_pose=amr_x2_pose.main:main',
        ],
    },
)
