# TCCP Docs Styles MkDocs Plugin

[![Build](https://github.com/trimble-oss/mkdocs-tccp-docs-styles/actions/workflows/ci.yml/badge.svg)](https://github.com/trimble-oss/mkdocs-tccp-docs-styles/actions/workflows/ci.yml) [![Publish](https://github.com/trimble-oss/mkdocs-tccp-docs-styles/actions/workflows/publish-pypi.yml/badge.svg)](https://github.com/trimble-oss/mkdocs-tccp-docs-styles/actions/workflows/publish-pypi.yml)


This plugin adds custom styles to a MkDocs project that uses MkDocs Material. 
- Modus light and dark theme
- Adds favicon and logo
- Modus themed admonitions
- Call to action buttons
- Modus color variables

[Demo Site](https://ideal-adventure-6v53m7m.pages.github.io/) [PyPi](https://pypi.org/project/mkdocs-tccp-docs-styles/)

## Installation

```bash
pip install tccp-docs-styles
```

## Usage

Add to your mkdocs.yml file

```yml

plugins:
  - tccp-docs-styles
      
```

## Dependencies

This plugin expects the following markdown extensions to be installed

```yml

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences  
  - attr_list

```

## Developing

Setup your environment, different steps for local testing and demo site deploy

### All
```sh
# setup a virtual python env
python3 -m venv .venv

# source your python env
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

### Local testing
```sh
# install the plugin in development mode
pip install -e .

# serve the develop/demo project
mkdocs serve
```

### Demo - GH Pages (Action)
```sh
# install the plugin in development mode
pip install -e .

# serve the develop/demo project
mkdocs gh-deploy --force
```
