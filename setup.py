import os, sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def main():
    setup(
        name='py_sne_rest_client',
        version= '0.1',
        author='PoornimaWari',
        author_email='poornima.wari@spirent.com',
        url='https://github.com/waripoornima/sne_rest_client',
        description='sne_rest_client: Front end for SPirent Network Emulator ReST API',
        long_description = 'See https://github.com/waripoornima/sne_rest_client',
        license='http://www.opensource.org/licenses/mit-license.php',
        keywords='Spirent Network Emulator API',
        classifiers=['Development Status :: 1 - Production/Stable',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Utilities',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3'],
        packages=['sne_rest_client'],
        install_requires=['requests>=2.7'],
        zip_safe=True,
        )


if __name__ == '__main__':
    main()
