from skbuild import setup

setup(
    name="finmath",
    version="0.1.0",
    description="Python Financial Mathematics library written in C/C++",
    author="Prajwal Shah, .. , Boiler Quant",
    license="MIT",
    packages=["finmath"],
    cmake_source_dir=".",
    cmake_install_dir="finmath"
)
