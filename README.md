# Oblivion-dots

**Oblivion-dots** is a modern, automated dotfiles installer for Linux that sets up your environment quickly and cleanly. It includes both CLI and GUI installers and handles dependencies automatically.

---

## Repository Structure

```
Oblivion-Installer/
├─ install.py           # Installer script
├─ main.sh              # One-liner launch script
├─ cli/
│   └─ main.py          # CLI installer
└─ gui/
    ├─ Oblivian         # GUI installer script
    └─ choices.sh       # Backend script for GUI
```

---

## Prerequisites

* Python 3
* GTK 3 (`gtk3` package)
* python-gobject (`python-gobject` package)

The installer can automatically detect and install missing dependencies on Arch-based systems.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Oblivion-dots.git
cd Oblivion-Installer
```

2. Run the installer:

* GUI: `python3 main.py`
* CLI: `python3 cli/main.py`

Or use the one-liner launch script:

```bash
bash main.sh
```

---

## Features

* Automatic environment detection (WAYLAND/X11)
* Modular component selection
* Clean GUI with typewriter-style welcome message
* Logging and clipboard support
* Lightweight and fast

---

## Notes

* GUI installer script: `gui/Oblivian`
* Backend script: `gui/choices.sh`
* `main.sh` can be used as a one-line installer for convenience

---

## License

Include your preferred license here (e.g., MIT, GPL).
