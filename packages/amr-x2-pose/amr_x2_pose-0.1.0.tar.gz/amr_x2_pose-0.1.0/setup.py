from setuptools import setup, find_packages

setup(
    name="amr_x2_pose",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe",
        "numpy",
        "matplotlib",
        # "mpl_toolkits",  # Remove this line - it's part of matplotlib
        "filterpy",
      # "tensorflow",  # For GPU acceleration
    ],
   
)