import os
import re


def generate_markdown():
    docstrings = extract_docstrings()
    docstrings.sort(key=lambda x: x[1])
    output_file = "./../../../rules.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Rules\n\n")
        f.write("| Id  | Nom | Description | Tags |\n")
        f.write("|:---:|-----|-------------|------|\n")
        for function_name, rule_id, description, tags in docstrings:
            f.write(f"| {rule_id} | {function_name} | {description} | {tags} |\n")
    generate_tags(output_file)


def extract_docstrings():
    directory = "./../rules"
    pattern = re.compile(
        r'def\s+(\w+)\s*\(.*?\):\s+"""\s+Id\s*:\s*(\d+)\s+Description\s*:\s*(.*?)\s+Tags\s*:\s*(.*?)\s+Args\s*:(.*?)"""',
        re.DOTALL,
    )
    results = []

    for rules_folder in os.listdir(directory):
        rules_path = os.path.join(directory, rules_folder)
        for root, _, files in os.walk(rules_path):
            for file in files:
                if file.endswith(".py"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        content = f.read()
                        matches = pattern.findall(content)
                        for match in matches:
                            function_name, rule_id, description, tags, args = match
                            description = " ".join(description.splitlines()).strip()
                            tags_list = " ".join(
                                [t.strip() for t in tags.split("-") if t.strip()]
                            )

                            results.append(
                                (function_name, rule_id, description.strip(), tags_list)
                            )
    return results


def generate_tags(output_file):
    with open(output_file, "a", encoding="utf-8") as f:
        f.write("\n\n## Tags  \n")
        f.write("- **web_files** : HTML, JS, and CSS files.\n")
        f.write("- **python_files** : Python files with `.py` extension.\n")
        f.write("- **architecture** : Checks folder and file placement consistency.\n")
        f.write("- **format** : Directly modifies file formatting.\n")
        f.write("- **files_content** : Inspects file contents.\n")


generate_markdown()
