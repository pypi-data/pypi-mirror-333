from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="jupyterhub-enverge-open-from-badge",
    version="0.0.1",
    description="JupyterHub Enverge Open From Badge",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Enverge-Labs/enverge_open_from_badge",
    author="Tudor M",
    author_email="tudor@enverge.ai",
    license="3 Clause BSD",
    packages=find_packages(),
    package_data={},
    python_requires=">=3.10",
    install_requires=[
        "jupyterhub>=4.1.6",
    ],
    extras_require={},
    include_package_data=True,
)
