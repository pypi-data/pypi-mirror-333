from setuptools import setup, find_packages

setup(
    name="onupoma_ai",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",  # this is the dependency for making HTTP requests
    ],
    description="AI API for Onupoma AI chatbot",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/onupoma_ai",  # Change to your actual URL if you publish to GitHub
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
