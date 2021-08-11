
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sne_rest_client',
    version='0.1',
    author='Poornima Wari',
    author_email='poornima.wari@spirent.com',
    description='Installation of Spirent Network Emulator ReST client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/waripoornima/sne_rest_client',
    project_urls = {
        "Bug Tracker": "https://github.com/waripoornima/sne_rest_client/issues"
    },
    license='MIT',
    packages=['sne_rest_client'],
    install_requires=['requests'],
)