from codecs import (
    open,
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


PROJECT = 'm3-db-utils'


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
    description='Utils for working with database.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    author='Alexander Danilenko',
    author_email='a.danilenko@bars.group',
    url='https://stash.bars-open.ru/projects/M3/repos/m3-db-utils/browse',
    download_url='http://nexus.budg.bars.group/#browse/browse:pypi-bars-private:m3-db-utils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
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
