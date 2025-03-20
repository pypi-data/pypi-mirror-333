import json
import os
import re
import subprocess
import urllib.parse
import urllib.request


def update_readme_files():
    docstrings = extract_docstrings()
    docstrings.sort(key=lambda x: x[1])

    tags_descriptions = {
        "web_files": "HTML, JS, and CSS files.",
        "python_files": "Python files with `.py` extension.",
        "architecture": "Checks folder and file placement consistency.",
        "format": "Directly modifies file formatting.",
        "files_content": "Inspects file contents.",
    }

    generate_english_readme(docstrings, tags_descriptions)
    generate_french_readme(docstrings, tags_descriptions)


def find_norminette_path():
    try:
        chemin = subprocess.check_output(
            "find . -type d -name 'norminette_prune'", shell=True, text=True
        ).strip()
        return chemin if chemin else None
    except subprocess.CalledProcessError:
        return None


def extract_docstrings():
    """Extrait les chaînes de documentation des règles à partir des fichiers Python."""
    directory = os.path.join(find_norminette_path(), "rules")
    pattern = re.compile(
        r'def\s+(\w+)\s*\(.*?\):\s+"""\s+Id\s*:\s*(\d+)\s+Description\s*:\s*(.*?)\s+Tags\s*:\s*(.*?)\s+Args\s*:(.*?)"""',
        re.DOTALL,
    )
    results = []
    try:
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return results

        for rules_folder in os.listdir(directory):
            rules_path = os.path.join(directory, rules_folder)

            for root, _, files in os.walk(rules_path):
                for file in files:
                    if file.endswith(".py"):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, "r", encoding="utf-8") as f:
                                content = f.read()
                                matches = pattern.findall(content)
                                for match in matches:
                                    function_name, rule_id, description, tags, args = (
                                        match
                                    )
                                    description = " ".join(
                                        description.splitlines()
                                    ).strip()
                                    tags_list = " ".join(
                                        [
                                            t.strip()
                                            for t in tags.split("-")
                                            if t.strip()
                                        ]
                                    )

                                    results.append(
                                        (
                                            function_name,
                                            rule_id,
                                            description.strip(),
                                            tags_list,
                                        )
                                    )
                        except Exception as e:
                            print(f"Error processing file {filepath}: {e}")
    except Exception as e:
        print(f"Error scanning directory: {e}")
    return results


def generate_english_readme(docstrings, tags_descriptions):
    """Generate and update english readme"""
    rules_markdown = "## Rules\n\n"
    rules_markdown += "| Id  | Name | Description | Tags |\n"
    rules_markdown += "|:---:|-----|-------------|------|\n"

    for function_name, rule_id, description, tags in docstrings:
        rules_markdown += f"| {rule_id} | {function_name} | {description} | {tags} |\n"

    rules_markdown += "\n\n### Tags  \n"

    for tag, description in tags_descriptions.items():
        rules_markdown += f"- **{tag}** : {description}\n"

    update_readme_file("README.md", rules_markdown)


def generate_french_readme(docstrings, tags_descriptions):
    """Generate and update french readme with translation"""
    rules_markdown = "## Règles\n\n"
    rules_markdown += "| Id  | Nom | Description | Tags |\n"
    rules_markdown += "|:---:|-----|-------------|------|\n"

    for function_name, rule_id, description, tags in docstrings:
        try:
            translated_description = translate_text(description)
        except Exception as e:
            print(f"Erreur lors de la traduction de la règle {rule_id}: {e}")
            translated_description = description

        rules_markdown += (
            f"| {rule_id} | {function_name} | {translated_description} | {tags} |\n"
        )

    rules_markdown += "\n\n### Tags  \n"

    for tag, description in tags_descriptions.items():
        try:
            translated_tag_desc = translate_text(description)
        except Exception as e:
            print(f"Erreur lors de la traduction du tag {tag}: {e}")
            translated_tag_desc = description

        rules_markdown += f"- **{tag}** : {translated_tag_desc}\n"

    update_readme_file("README-FR.md", rules_markdown, True)


def translate_text(text):
    """
    Translate with 'libre translate'
    """
    try:
        url = "https://translate.fedilab.app/translate"

        data = {"q": text, "source": "en", "target": "fr", "format": "text"}

        encoded_data = json.dumps(data).encode("utf-8")
        headers = {"Content-Type": "application/json"}

        req = urllib.request.Request(
            url, data=encoded_data, headers=headers, method="POST"
        )

        with urllib.request.urlopen(req, timeout=5) as response:
            response_data = response.read().decode("utf-8")
            result = json.loads(response_data)
            return result.get("translatedText", text)
    except Exception as e:
        print(f"Erreur de traduction: {e}")
        return text


def update_readme_file(filename, rules_markdown, is_french=False):
    """Update Readme with rules and tags"""
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found.")
        return

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"## Règles.*?(?=##|\Z)" if is_french else r"## Rules.*?(?=##|\Z)"
    content = re.sub(pattern, "", content, flags=re.DOTALL)

    tags_pattern = r"### Tags.*?(?=##|\Z)"
    content = re.sub(tags_pattern, "", content, flags=re.DOTALL)

    content = content.rstrip("\n") + "\n"

    content += rules_markdown

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


update_readme_files()
