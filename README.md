# Oblivion-dots

**Oblivion-dots** is a modern dotfiles installer for Linux that automates setting up a complete development environment quickly and cleanly. It provides both CLI and GUI installers, with automatic dependency handling for supported systems.

---

## 📁 Repository Structure

```
Oblivion-Installer/
├─ install.py            # Main installer entry point
├─ main.sh               # One-line launcher script
├─ cli/
│   └─ main.py          # CLI installer
└─ gui/
    ├─ Oblivion         # GUI installer frontend
    └─ choices.sh       # GUI backend logic
```

---

## ⚙️ Requirements

* Python 3
* Git
* GTK 3 (`gtk3`)
* Python GObject (`python-gobject`)

On Arch-based systems, missing dependencies can be installed automatically during setup.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Oblivion-dots.git
cd Oblivion-Installer
```

---

### 2. Run manually

#### GUI Installer

```bash
python3 install.py
```

#### CLI Installer

```bash
python3 cli/main.py
```

---

## ⚡ Quick Install (CLI)

Install and launch the CLI installer directly without manual setup:

```bash
bash <(curl -sSL https://raw.githubusercontent.com/yourusername/Oblivion-dots/main/main.sh)
```

---

## ✨ Features

* Automatic environment detection (Wayland / X11)
* Modular component selection
* CLI and GUI support
* Automatic dependency installation (Arch-based systems)
* Lightweight and fast execution
* Logging support for debugging

---
