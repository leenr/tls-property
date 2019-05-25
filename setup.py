from setuptools import setup


setup(
    name='tls-property',
    version='1.0.1',

    py_modules=['tls_property'],
    provides=['tls_property'],

    description='A @decorator for caching properties in classes '
                'in the thread-local storage.',
    long_description=open('README.rst').read(),
    keywords=['thread-local storage', 'decorator'],

    url='https://github.com/leenr/tls-property',
    author='leenr',
    author_email='i@leenr.ru',
    maintainer='leenr',
    maintainer_email='i@leenr.ru',

    platforms=['posix'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],

    python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,<4",
    extras_require={
        'develop': [
            'pytest~=4.2',
            'pytest-cov~=2.6',
            'pylama~=7.6'
        ]
    }
)
