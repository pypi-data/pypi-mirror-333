from setuptools import setup, find_packages

setup(
    name='maxplotlib',
    version='0.1.9',
    author='Max Cembalest',
    author_email='macembalest@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='http://github.com/mcembalest/maxplotlib',
    license='LICENSE',
    description='Autoviz API by Max Cembalest',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    extras_require={
        'server': [
            "matplotlib",
            "mlx_lm",
            "numpy",
            "pillow",
            "plotly",
            "torch"
        ]
    },
    python_requires='>=3.8',  # Minimum version requirement of Python
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    entry_points={
        'console_scripts': [
            'maxplotlib=maxplotlib.cli:main',
        ],
    },
)
