from setuptools import find_packages,setup
from typing import List
HYPEN_EDOT = "-e ."
def get_packages(file_path:str)-> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("/n","") for req in requirements]
        if HYPEN_EDOT in requirements:
            requirements.remove(HYPEN_EDOT)
    return requirements


setup(
    name="ML Project",
    version = "0.0.1",
    author= "Kaushik Adiraju",
    author_email="kaushikadiraju3@gmail.com",
    packages = find_packages(),
    install_requires = get_packages("requirements.txt")
)