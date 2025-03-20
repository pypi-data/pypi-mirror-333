from setuptools import find_packages
from setuptools import setup


version = '1.1'

TESTS_REQUIRE = ["zc.buildout", "zope.testing"]

setup(
    name='z3c.autoinclude',
    version=version,
    description="Automatically include ZCML",
    long_description=(
        open('README.rst').read() + "\n" + open('CHANGES.rst').read()),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Zope :: 3",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords='zcml automatic',
    author='Zope Foundation and Contributors',
    author_email='zope-dev@zope.dev',
    url='https://github.com/zopefoundation/z3c.autoinclude',
    license='ZPL',
    packages=find_packages('src'),
    package_dir={
        '': 'src'},
    namespace_packages=['z3c'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.9',
    install_requires=[
        'setuptools',
        'zope.dottedname',
        'zope.interface',
        'zope.configuration',
        'zope.schema>=4.2.0',
    ],
    extras_require={
        'test': TESTS_REQUIRE},
    entry_points="""
    [console_scripts]
    autoinclude-test = z3c.autoinclude.tests.tests:interactive_testing_env
    """,
)
