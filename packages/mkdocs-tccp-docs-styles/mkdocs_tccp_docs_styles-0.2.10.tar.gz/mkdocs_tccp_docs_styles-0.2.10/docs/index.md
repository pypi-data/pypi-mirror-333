# TCCP Docs Styles MkDocs Plugin

This plugin adds custom styles to a MkDocs project that uses MkDocs Material. 

- Modus light and dark theme
- Adds favicon and logo
- Modus themed admonitions
- Call to action buttons
- Modus color variables

Check out the official [Modus Style Guide](https://modus.trimble.com/)

## Installation

```bash
pip install mkdocs-tccp-docs-styles
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

