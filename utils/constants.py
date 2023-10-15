from pathlib import Path


# Корневая директория проекта.
BASE_DIR = Path(__file__).absolute().parent.parent

# Директория с шаблонами.
TEMPLATES_DIR = BASE_DIR / "app" / "templates"

# Директория с медиа файлами.
MEDIA_DIR = BASE_DIR / "media"
