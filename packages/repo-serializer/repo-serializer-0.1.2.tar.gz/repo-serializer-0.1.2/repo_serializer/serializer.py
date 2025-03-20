import os

SKIP_EXTENSIONS = {
    ".pyc",
    ".exe",
    ".dll",
    ".so",
    ".o",
    ".bin",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".ico",
    ".svg",
    ".log",
    ".zip",
    ".gz",
    ".tar",
    ".rar",
    ".7z",
    ".pdf",
    ".mp4",
    ".mp3",
    ".wav",
    ".class",
    ".jar",
    ".db",
    ".sqlite",
    ".map",  # Source Maps
    ".d.ts",  # TypeScript Declaration Files
    ".lock",  # Dependency Lock Files
    ".lockb",
    ".lock.json",
    ".lock.yaml",
    ".lock.yml",
    ".lock.toml",
    ".toml",
    ".yarnrc",
    ".npmrc",
}

SKIP_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "composer.lock",
    "Cargo.lock",
    "Pipfile.lock",
    "poetry.lock",
    "Gemfile.lock",
    "go.sum",
}

SKIP_DIRS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    ".DS_Store",
    "venv",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".coverage",
    ".cache",
    ".temp",
    ".build",
    ".dist",
    ".out",
    ".tmp",
    ".log",
    "temp",
    "tmp",
    "node_modules/.vite",
    "cypress",
    "dist",
    "build",
    "out",
    "cache",
    "temp",
}


def should_skip(name, is_dir=False):
    if name.startswith("."):
        return True
    if is_dir and name in SKIP_DIRS:
        return True
    if not is_dir:
        if os.path.splitext(name)[1] in SKIP_EXTENSIONS:
            return True
        if name in SKIP_FILES:
            return True
    return False


def generate_ascii_structure(path, prefix="", serialized_content=None):
    if serialized_content is None:
        serialized_content = []
    entries = sorted(
        e
        for e in os.listdir(path)
        if not should_skip(e, os.path.isdir(os.path.join(path, e)))
    )
    for idx, entry in enumerate(entries):
        entry_path = os.path.join(path, entry)
        connector = "└── " if idx == len(entries) - 1 else "├── "
        serialized_content.append(f"{prefix}{connector}{entry}")
        if os.path.isdir(entry_path):
            extension = "    " if idx == len(entries) - 1 else "│   "
            generate_ascii_structure(entry_path, prefix + extension, serialized_content)
    return serialized_content


def serialize_repo(repo_path, output_file):
    serialized_content = []

    serialized_content.append("Directory Structure:")
    generate_ascii_structure(repo_path, serialized_content=serialized_content)

    serialized_content.append("\nFiles Content:")
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not should_skip(d, True)]
        for file in files:
            if should_skip(file, False):
                continue
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, repo_path)
            serialized_content.append(f"\n--- Start of {rel_path} ---\n")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    serialized_content.append(f.read())
            except UnicodeDecodeError:
                serialized_content.append("[BINARY or NON-UTF8 CONTENT]")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(serialized_content))


def serialize(repo_path, output_file):
    serialize_repo(repo_path, output_file)
