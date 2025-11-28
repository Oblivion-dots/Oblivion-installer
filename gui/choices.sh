#!/usr/bin/env bash
set -e

# -----------------------------
# Installer backend
# -----------------------------

# Functions for installing AUR helpers
install_yay() {
    echo "Installing yay..."
    sudo pacman -Sy --needed --noconfirm git base-devel
    git clone https://aur.archlinux.org/yay.git /tmp/yay
    pushd /tmp/yay
    makepkg -si --noconfirm
    popd
    rm -rf /tmp/yay
}

install_paru() {
    echo "Installing paru..."
    sudo pacman -Sy --needed --noconfirm git base-devel
    git clone https://aur.archlinux.org/paru.git /tmp/paru
    pushd /tmp/paru
    makepkg -si --noconfirm
    popd
    rm -rf /tmp/paru
}

# Functions for components
install_hyprland() {
    echo "Installing Hyprland..."
    $AUR_HELPER -Sy hyprland-git --noconfirm
}

install_quickshell() {
    echo "Installing QuickShell..."
    $AUR_HELPER -Sy quickshell-git --noconfirm
}

install_matugen() {
    echo "Installing Matugen..."
    $AUR_HELPER -Sy matugen --noconfirm
}

# Detect installed AUR helper
if command -v yay &> /dev/null; then
    AUR_HELPER="yay"
elif command -v paru &> /dev/null; then
    AUR_HELPER="paru"
else
    # No AUR helper found, require user/GUI to choose one
    echo "No AUR helper found! Please select one to install: yay or paru"
    read -r selection
    case $selection in
        yay) install_yay; AUR_HELPER="yay" ;;
        paru) install_paru; AUR_HELPER="paru" ;;
        *) echo "Invalid selection! Exiting."; exit 1 ;;
    esac
fi

echo "Using AUR helper: $AUR_HELPER"

# -----------------------------
# Install requested components
# -----------------------------
for component in "$@"; do
    case $component in
        hyprland) install_hyprland ;;
        quickshell) install_quickshell ;;
        matugen) install_matugen ;;
        *) echo "Unknown component: $component" ;;
    esac
done

echo "All selected components installed successfully!"
