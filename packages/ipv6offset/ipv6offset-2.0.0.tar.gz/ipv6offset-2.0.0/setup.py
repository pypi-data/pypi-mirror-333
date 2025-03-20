import setuptools

with open('/tmp/ipv6offset/requirements.txt') as f:
    requirements = f.readlines()

with open("/tmp/ipv6offset/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ipv6offset',
    version='2.0.0',
    author='VietDuc19',
    description='A Simple Tool To Find The IPv6 Address Offset For A Given IPv6.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GPLv3',
    #py_modules=['ipv6offset'],
    install_requires=['netaddr'],
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'ipv6offset=ipv6offset.ipv6offset:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    keywords ='IPv6 offset',
    #install_requires = requirements,
    zip_safe = False
)
