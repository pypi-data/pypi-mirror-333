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


PROJECT = 'nightly-scripts'

current_dir_path = Path().resolve()


#  Получение полного описания
with open(str(current_dir_path / 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(str(current_dir_path / 'CHANGELOG.md'), encoding='utf-8') as f:
    long_description += f.read()

production_requirements_path = current_dir_path / 'requirements' / 'production.txt'

requirements = parse_requirements(str(production_requirements_path), session=PipSession())

install_requires = [str(item.requirement) for item in requirements]

setup(
    name=PROJECT,

    description='Ночные скрипты',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='BARS Group',
    author_email='bars@bars.group',

    url='',
    download_url='',

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
        'Environment :: Console',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
    ],

    platforms=['Any'],

    scripts=[],

    provides=[],

    namespace_packages=[],
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('tests', 'tests.*')),
    include_package_data=True,

    package_data={
        '': [
            '*.conf',
            '*.tmpl',
            '*.sh',
            'Dockerfile',
            '*.yaml',
        ],
    },

    install_requires=install_requires,

    zip_safe=False,
)
