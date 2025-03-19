from setuptools import setup, find_packages
import re

package = "mgefit"

def find_version():
    version_file = open(package + "/__init__.py").read()
    rex = r'__version__\s*=\s*"([^"]+)"'
    return re.search(rex, version_file).group(1)

def read_docstring(name, file=None):
    if file is None:
        file = name + ".py"
    main_file = open(package + "/" + file).read()
    rex = f'(?:def {name}[\\w\\W]+?|class {name}):\\n\\s*"""([\\W\\w]+?)"""'
    docstring = re.search(rex, main_file).group(1)
    return docstring.replace("\n    ", "\n")

setup(name=package,
      version=find_version(),
      description='MgeFit: Multi-Gaussian Expansion Fitting of Galaxy Images',
      long_description_content_type= 'text/x-rst',
      long_description=open(package + "/README.rst").read()
                       + read_docstring("mge_fit_sectors")
                       + read_docstring("mge_fit_1d")
                       + read_docstring("find_galaxy")
                       + open(package + "/LICENSE.txt").read()
                       + open(package + "/CHANGELOG.rst").read(),
      url="https://purl.org/cappellari/software",
      author="Michele Cappellari",
      author_email="michele.cappellari@physics.ox.ac.uk",
      license="Other/Proprietary License",
      packages=find_packages(),
      package_data={package: ["*.rst", "*.txt", "*.pdf", "*/*.txt", "*/*.fits"]},
      install_requires=['capfit', 'numpy', 'scipy', 'matplotlib', 'astropy'],
      classifiers=["Development Status :: 5 - Production/Stable",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 3"],
      zip_safe=True)
