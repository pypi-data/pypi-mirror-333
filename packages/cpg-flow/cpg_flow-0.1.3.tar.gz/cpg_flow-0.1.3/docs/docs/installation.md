# 🔨 Installation

The packages are hosted on:

![PyPI](https://img.shields.io/badge/-PyPI-black?style=for-the-badge&logoColor=white&logo=pypi&color=3776AB)

To install this project, you will need to have Python and `uv` installed on your machine:

![uv](https://img.shields.io/badge/-uv-black?style=for-the-badge&logoColor=white&logo=uv&color=3776AB&link=https://docs.astral.sh/uv/)
![Python](https://img.shields.io/badge/-Python-black?style=for-the-badge&logoColor=white&logo=python&color=3776AB)

Run the following commands, to create a virtual environment with `uv` and install the dependencies:

```bash
# Install the package using uv
uv sync

# Or equivalently use make (also installs pre-commit)
make init
```

## 🛠️ Development

To setup for development we recommend using the makefile setup

```bash
make init-dev # installs pre-commit as a hook
```

To install `cpg-flow` locally, run:

```bash
make install-local
```

!!! tip
    To try out the pre-installed `cpg-flow` in a Docker image, find more information in the **[Docker](docker.md#docker)** section.

## 🚀 Build</a>

To build the project, run the following command:

```bash
make build
```

To make sure that you're actually using the installed build we suggest calling the following to install the build wheel.

```bash
make install-build
```
