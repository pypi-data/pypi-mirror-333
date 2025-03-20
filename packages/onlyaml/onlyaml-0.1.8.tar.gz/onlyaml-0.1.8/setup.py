from setuptools import setup, find_packages

x = 0

y = 1

z = 8

version = "{}.{}.{}".format(x, y, z)


setup(
    name='onlyaml',
    version=version,
    description='A python library imposing program only accepting yaml file as CL argument',
    url='',
    author='WD',
    author_email='',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "dacite"
    ],
    python_requires=">=3.7",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
