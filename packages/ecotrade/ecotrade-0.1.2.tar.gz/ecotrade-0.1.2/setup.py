from setuptools import setup, find_packages

setup(
    name='Ecotrade',
    version='0.1.2',
    author='Zyber Pireci & Vishva Teja Janne',
    author_email='supporto@ecotrade.bio',
    description='An Ecotrade package to manage the software infrastructure',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # url='https://github.com/yourusername/your-repo',  # If you have a GitHub repo for the package
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust the license to your choice
        'Operating System :: OS Independent',
    ],
    install_requires=[],  # List your dependencies here
    python_requires='>=3.6',  # Adjust this depending on your compatibility
)
