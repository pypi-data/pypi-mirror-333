import setuptools
import os

# Read the contents of README.md for the long description.
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rvc_inferpy",
    version="0.7.1",
    author="TheNeoDev",
    author_email="theneodevemail@gmail.com",
    description="Easy tools for RVC Inference",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "av",
        "einops",
        "edge-tts",
        "faiss-cpu==1.7.3",
        "ffmpeg-python>=0.2.0",
        "fairseq",
        "gtts",
        "local_attention",
        "pydub==0.25.1",
        "praat-parselmouth==0.4.2",
        "pyworld==0.3.4",
        "resampy==0.4.2",
        "torchcrepe==0.0.23",
        "torchfcpe",
        "yt-dlp"
    ],
    extras_require={
        "gpu": ["audio-separator[gpu]==0.30.1"],
        "cpu": ["audio-separator[cpu]==0.30.1"],
        "dev": ["librosa>=0.9.1,<0.11"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    license="MIT",
)