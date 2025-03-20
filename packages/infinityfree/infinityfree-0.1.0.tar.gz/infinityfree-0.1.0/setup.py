from setuptools import setup, find_packages

setup(
    name='infinityfree',
    version='0.1.0',
    author='Your Name',
    author_email='your_email@example.com',
    description='A bypasser tool for infinityfree module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/infinityfree',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pycryptodome'  # Add other dependencies if needed
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
