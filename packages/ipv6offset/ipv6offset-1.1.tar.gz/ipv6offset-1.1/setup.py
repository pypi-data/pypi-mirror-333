import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ipv6offset',
    version='1.1',
    py_modules=['ipv6offset'],
    install_requires=['netaddr'],
    entry_points={
        'console_scripts': [
            'ipv6offset=ipv6offset:main',
        ],
    },
    description='A Simple Tool To Find The IPv6 Address Offset For A Given IPv6.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ToanPhan24',
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
)
