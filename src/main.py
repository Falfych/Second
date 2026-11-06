import os
import sys
import json
import urllib.request

REQUIRED_FIELDS = [
    "package_name",
    "repo_path",
    "mode",
    "output_image_path",
    "ascii_tree_path"
]


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        print(f"Критическая ошибка: Файл '{config_path}' не найден.")
        sys.exit(1)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Критическая ошибка: Невалидный формат JSON. Ошибка: {e}")
        sys.exit(1)

    return data


def validate_config(config: dict):
    for field in REQUIRED_FIELDS:
        if field not in config:
            print(f"Критическая ошибка: Отсутствует параметр '{field}'")
            sys.exit(1)
        if not str(config[field]).strip():
            print(f"Ошибка: Параметр '{field}' не должен быть пустым.")
            sys.exit(1)


def parse_dependency_name(dep_str: str) -> str:
    cleaned = ""
    for char in dep_str:
        if char in [" ", "(", "[", "<", ">", "=", "!"]:
            break
        cleaned += char
    return cleaned


def fetch_dependencies(package_name: str, base_url: str) -> list:
    clean_url = base_url.rstrip("/")
    if "pypi.org" not in clean_url:
        clean_url = "https://pypi.org"

    url = f"{clean_url}/pypi/{package_name}/json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla"})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode("utf-8")
            data = json.loads(html)
    except Exception as e:
        print(f"Ошибка связи: Не удалось получить данные. Лог: {e}")
        sys.exit(1)

    info = data.get("info", {})
    reqs = info.get("requires_dist")
    if reqs is None:
        return []

    dependencies = []
    for req in reqs:
        if "extra ==" not in req:
            dep_name = parse_dependency_name(req)
            if dep_name:
                dependencies.append(dep_name)

    return dependencies


def print_dependencies(package_name: str, dependencies: list):
    print(f"=== Реальные прямые зависимости пакета '{package_name}' ===")
    if not dependencies:
        print("(нет прямых зависимостей)")
    else:
        for dep in dependencies:
            print(f"  - {dep}")
    print("==================================================\n")


def main():
    config_file = "config.json"
    config_data = load_config(config_file)
    validate_config(config_data)

    pkg = config_data["package_name"]
    repo = config_data["repo_path"]

    deps = fetch_dependencies(pkg, repo)
    print_dependencies(pkg, deps)


if __name__ == "__main__":
    main()
