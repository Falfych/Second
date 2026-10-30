import os
import sys
import json

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


def print_config(config: dict):
    print("=== Отладочный вывод параметров ===")
    for key, value in config.items():
        print(f"{key}: {value}")
    print("===================================\n")


def main():
    config_file = "config.json"
    config_data = load_config(config_file)
    validate_config(config_data)
    print_config(config_data)


if __name__ == "__main__":
    main()
