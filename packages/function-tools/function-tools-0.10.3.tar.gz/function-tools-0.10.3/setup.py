from codecs import (
    open,
)
from os import (
    path,
)
from pathlib import (
    Path,
)

from pip._internal.network.session import (
    PipSession,
)
from pip._internal.req import (
    parse_requirements,
)
from setuptools import (
    find_packages,
    setup,
)


PROJECT = 'function-tools'


here = path.abspath(path.dirname(__file__))


current_dir_path = Path().resolve()

#  Получение полного описания
with open(str(current_dir_path / 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(str(current_dir_path / 'CHANGES.md'), encoding='utf-8') as f:
    long_description += f.read()

production_requirements_path = current_dir_path / 'requirements' / 'production.txt'

requirements = parse_requirements(str(production_requirements_path), session=PipSession())

install_requires = [str(item.requirement) for item in requirements]

setup(
    name=PROJECT,
    description='Tools for creating functions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Alexander Danilenko',
    author_email='a.danilenko@bars.group',
    url='https://github.com/sandanilenko/function-tools',
    download_url='http://nexus.budg.bars.group/#browse/browse:pypi-bars-private:function-tools',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
    ],
    platforms=['Any'],
    scripts=[],
    provides=[],
    namespace_packages=[],
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('tests', 'tests.*')),
    include_package_data=True,
    install_requires=install_requires,
    zip_safe=False,
)
