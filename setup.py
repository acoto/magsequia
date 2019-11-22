import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()


requires = ["formshare",
            "matplotlib",
            "numpy",
            "geopandas",
            "descartes"]




tests_require = ["WebTest >= 1.3.1", "pytest", "pytest-cov"]  # py3 compat

setup(
    name="ext_climate",
    version="0.1",
    description="Extension for climate MAG",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="bioversity-acoto",
    author_email="a.coto@cgiar.org",
    url="www.myserver.com",
    keywords="formshare plugin",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={"testing": tests_require},
    install_requires=requires,
    entry_points={
        "formshare.plugins": ["ext_climate = ext_climate.plugin:ext_climate"],
        "formshare.tasks": ["ext_climate = ext_climate.processes.updateProducts"],
    },
)
