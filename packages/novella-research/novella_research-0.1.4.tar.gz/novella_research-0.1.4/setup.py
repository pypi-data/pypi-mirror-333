from setuptools import setup, find_packages

setup(
    name='novella_research',
    version='0.1.4',
    packages=find_packages(),
    install_requires=[
        'tensorflow>=2.0'
    ],
    author='Joshua Kim',
    author_email='happyjoshua08@gmail.com',
    description='This package contains all my custom Tensorflow work.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/novella_research',
    classifiers=[
        'Programming Language :: Python :: 3',  # Specify supported Python versions
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',  # Your chosen license
        'Operating System :: OS Independent',  # Cross-platform
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
