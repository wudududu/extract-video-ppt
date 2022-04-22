import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name='extract-video-ppt',
    version='1.1.2',
    author="wudu",
    author_email="296525335@qq.com",
    description="support export ppt from a video",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['video2ppt', ],
    package_dir={'video2ppt': 'video2ppt'},
    py_modules=['evp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        'click',
        'fpdf2',
        'matplotlib',
        'opencv-python',
        'numpy'
    ],
    entry_points='''
        [console_scripts]
        evp=video2ppt:main
    ''',
)