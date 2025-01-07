import os

from setuptools import find_packages, setup

import spdx_license_matcher

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

_ROOT = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_ROOT, 'README.md')) as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="spdx-license-matcher",
    version=spdx_license_matcher.__version__,
    description="SPDX License matcher matches the license text given by the user against the SPDX license list using an algorithm which finds close matches.",
    long_description=LONG_DESCRIPTION,
    author="SPDX",
    url="https://github.com/spdx/spdx-license-matcher",
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements,
    setup_requires=['setuptools>=39.0.1'],
    entry_points={'console_scripts': [
        'spdx-license-matcher = spdx_license_matcher.matcher:matcher']},
    keywords='spdx license license-matcher',
)
