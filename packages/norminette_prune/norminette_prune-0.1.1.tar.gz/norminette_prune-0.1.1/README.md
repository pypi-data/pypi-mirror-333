# Prune's Norminette

## What is it for?

The norminette automatically checks the organization of files in a Django project as well as code rules.
This allows for the same code standard between projects and makes it easier to navigate.

## Prerequisites

- To be installed on a Prune Django project that uses poetry or UV
- SSH access to the project: verify that you have SSH access to the Gitlab project of the norminette

## UV project

### Installation

In `pyproject.toml`, add in the `dependencies = []` or `dev[]` section :

```none
dependencies = [
"norminette @ git+ssh://git@gitlab.com/bastien_arnout/norminette.git",
]
```

To synchronize the results, run the following command in the console:

 ```bash
 uv sync
 ``` 
 Ou
 ```bash
 uv lock
 ```

### Running the norminette

To run the package, simply enter in the console :
```bash
norminette
```

### Updating the norminette
Don't hesitate to run `uv sync --upgrade` sometimes, the norminette evolves with time and our practices!

## Poetry project

### Installation

In `pyproject.toml`, add in the `[tool.poetry.group.dev.dependencies]` section :

```
[tool.poetry.group.dev.dependencies]
norminette = { git = "git@gitlab.com:bastien_arnout/norminette.git" }
```

Then, run the following command :

```bash
poetry update norminette
```

### Running the norminette
```bash
poetry run norminette
```

### Updating the norminette
Don't hesitate to run `poetry update norminette` sometimes, the norminette evolves with time and our practices!

## Project architecture at Prune

To access the documentation, please go to the link where you can find documentation in English and French.

[Documentation](https://gitlab.com/bastien_arnout/prune-doc.git)

If you want to download it directly, here is the link :

[Download](https://gitlab.com/bastien_arnout/prune-doc/-/archive/main/prune-doc-main.zip)
## Rules

| Id  | Name | Description | Tags |
|:---:|-----|-------------|------|
| 01 | name_view_function | Verify that the name of rendering functions for views ends with '_view'. | python_files files_content |
| 02 | verify_pages_folder | Verify if `page.html` files are inside the `pages/` folder and ensure files in `pages/`     are named `page` (except in `components`, `sections`, and `layouts` folders). | web_files architecture |
| 03 | verify_structure_templates_static | Verify that the `static/` and `templates/` folders contain only one subfolder named after the app. | architecture |
| 04 | double_line | Remove double empty lines in HTML, JS, and CSS files. | format files_content web_files |
| 05 | space_tag | Normalize spaces in Django tags (with exactly one space between the tag and its content). | format web_files files_content |
| 06 | component_layout_emplacement | Verify that layout, component, and section files are correctly placed based on their `include` references. | web_files architecture |
| 07 | include_svg | Ensure that SVG includes use absolute paths. | web_files files_content |
| 08 | svg | Verify that SVG files are inside the `svg/` folder and use the `.html` extension. | web_files architecture |


### Tags  
- **web_files** : HTML, JS, and CSS files.
- **python_files** : Python files with `.py` extension.
- **architecture** : Checks folder and file placement consistency.
- **format** : Directly modifies file formatting.
- **files_content** : Inspects file contents.
