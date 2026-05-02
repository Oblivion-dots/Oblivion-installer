#!/usr/bin/env python3
import os
import sys
import subprocess

# ========= ASCII BANNER ========= #
BANNER = r"""

░█████╗░██████╗░██╗░░░░░██╗██╗░░░██╗██╗░█████╗░███╗░░██╗░░░░░░██████╗░░█████╗░████████╗░██████╗
██╔══██╗██╔══██╗██║░░░░░██║██║░░░██║██║██╔══██╗████╗░██║░░░░░░██╔══██╗██╔══██╗╚══██╔══╝██╔════╝
██║░░██║██████╦╝██║░░░░░██║╚██╗░██╔╝██║██║░░██║██╔██╗██║█████╗██║░░██║██║░░██║░░░██║░░░╚█████╗░
██║░░██║██╔══██╗██║░░░░░██║░╚████╔╝░██║██║░░██║██║╚████║╚════╝██║░░██║██║░░██║░░░██║░░░░╚═══██╗
╚█████╔╝██████╦╝███████╗██║░░╚██╔╝░░██║╚█████╔╝██║░╚███║░░░░░░██████╔╝╚█████╔╝░░░██║░░░██████╔╝
░╚════╝░╚═════╝░╚══════╝╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝░░░░░░╚═════╝░░╚════╝░░░░╚═╝░░░╚═════╝░
"""

# ========= COLOR SHORTCUTS ========= #
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    GREEN = "\033[32m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    MAG = "\033[35m"

USE_COLOR = sys.stdout.isatty()

def color(text, col):
    if not USE_COLOR:
        return text
    return f"{col}{text}{C.RESET}"

# ========= LOGGING ========= #
def log_info(msg):
    print(color("[INFO] ", C.BLUE) + msg)

def log_ok(msg):
    print(color("[ OK ] ", C.GREEN) + msg)

def log_warn(msg):
    print(color("[WARN] ", C.YELLOW) + msg)

def log_error(msg):
    print(color("[ERR ] ", C.RED) + msg)

def log_step(msg):
    print(color("⟹ ", C.CYAN) + msg)

# ========= SYSTEM PACKAGE CHECK ========= #
REQUIRED_PACKAGES = [
    "python-gobject",  # gi, Gtk
    "gtk3",
    "bash",            # needed for choices.sh
]

def check_and_install_packages():
    missing = []
    for pkg in REQUIRED_PACKAGES:
        result = subprocess.run(["pacman", "-Qi", pkg],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            missing.append(pkg)
    if missing:
        log_warn(f"Missing system packages: {', '.join(missing)}")
        # Ask user for permission
        while True:
            choice = input(color("Do you want to install the missing packages now? [y/N]: ", C.CYAN)).strip().lower()
            if choice in ("y", "yes"):
                log_step("Installing missing packages with pacman...")
                subprocess.run(["sudo", "pacman", "-S", "--needed"] + missing)
                break
            elif choice in ("n", "no", ""):
                log_error("Cannot continue without required packages. Exiting.")
                sys.exit(1)
            else:
                print("Please answer 'y' or 'n'.")
    else:
        log_ok("All required system packages are installed.")

# ========= ENV DETECTION ========= #
def detect_env():
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    return None

# ========= RUN INSTALLER ========= #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_installer(env):
    if env in ("wayland", "x11"):
        log_ok(f"Detected {env.upper()} session.")
        log_step("Launching GUI installer...")
        gui_path = os.path.join(BASE_DIR, "gui", "main.py")
        subprocess.run([sys.executable, gui_path])
    else:
        log_warn("No graphical session found.")
        log_step("Launching CLI installer instead...")
        cli_path = os.path.join(BASE_DIR, "cli", "main.py")
        subprocess.run([sys.executable, cli_path])

# ========= MAIN ========= #
def main():
    print(color(BANNER, C.MAG))

    log_info("Checking required system packages...")
    check_and_install_packages()

    log_info("Detecting environment...")
    env = detect_env()

    if env:
        log_ok(f"Graphical environment: {env.upper()}")
    else:
        log_warn("Graphical environment not detected.")

    run_installer(env)

if __name__ == "__main__":
    main()
