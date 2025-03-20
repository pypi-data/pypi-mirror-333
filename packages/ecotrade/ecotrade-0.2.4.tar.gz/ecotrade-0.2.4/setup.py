from setuptools import setup, find_packages

setup(
    name='ecotrade',
    version='0.2.4',
    author='Zyber Pireci & Vishva Teja Janne',
    author_email='supporto@ecotrade.bio',
    description='An Ecotrade package to manage the software infrastructure',
    packages=find_packages(include=["ecotrade"]),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    python_requires='>=3.6', 
)

