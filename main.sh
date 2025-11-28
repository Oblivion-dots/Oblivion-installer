#!/usr/bin/env bash

# Clone the repo
git clone https://github.com/Oblivion-dots/Oblivion-installer.git /tmp/Oblivion-dots
cd /tmp/Oblivion-dots || exit

# Optional: check/install prerequisites (Arch-based example)
if ! command -v python3 >/dev/null; then
    echo "[INFO] Installing Python3..."
    sudo pacman -S --noconfirm python
fi

if ! pacman -Q gtk3 python-gobject >/dev/null 2>&1; then
    echo "[INFO] Installing GTK and python-gobject..."
    sudo pacman -S --noconfirm gtk3 python-gobject
fi

# Launch the installer
python3 install.py
