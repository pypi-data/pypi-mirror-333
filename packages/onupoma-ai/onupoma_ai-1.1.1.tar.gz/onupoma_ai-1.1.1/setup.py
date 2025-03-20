from setuptools import setup, find_packages

setup(
    name='onupoma_ai',
    version='1.1.1',  # Updated version to 1.1.1 (you can increment the version as needed)
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='Onupoma AI Python Package',
    long_description='This package allows interaction with the Onupoma AI chat and think APIs.',
    long_description_content_type='text/markdown',
    author='MD Jakaria Fiad',
    author_email='onupoma749@gmail.com',
    url='https://github.com/onupoma/onupoma_ai',  # Update the URL if necessary
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
