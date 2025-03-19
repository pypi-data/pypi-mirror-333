from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name="jupyterhub-enverge-placeholder",
    version="0.0.2",
    description="JupyterHub Enverge Placeholder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Enverge-Labs/enverge_placeholder",
    author="Leticia Portella",
    author_email="leportella@protonmail.com",
    license="3 Clause BSD",
    packages=find_packages(),
    package_data={
        'enverge_placeholder': ['schema/*', 'src/*', 'style/*', 'enverge_placeholder/config/*'],
    },
    python_requires=">=3.10",
    install_requires=[
        "jupyterhub>=4.1.6",
    ],
    extras_require={},
    include_package_data=True,
)
