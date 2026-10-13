"""
MasterAutomation Desktop Launcher
Wrapper entrypoint for frozen PyInstaller Windows executable.
"""
import os
import sys
import multiprocessing

# Critical: Prevents child process fork bombs on Windows with PyInstaller
multiprocessing.freeze_support()

import socket
import threading
import time
import webbrowser
from pathlib import Path


def find_free_port(preferred: int = 8501) -> int:
    """Find a free TCP port, starting with the preferred port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(("127.0.0.1", preferred))
            return preferred
    except OSError:
        pass

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def get_base_dir() -> Path:
    """Determine base directory whether running from source or frozen binary."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent


def main():
    base_dir = get_base_dir()
    os.chdir(base_dir)

    if str(base_dir) not in sys.path:
        sys.path.insert(0, str(base_dir))

    # Point to the app entrypoint
    app_path = base_dir / "app.py"
    if not app_path.exists():
        app_path = base_dir / "master_update_automation" / "app.py"

    port = find_free_port(8501)
    url = f"http://localhost:{port}"

    print("=" * 64)
    print("  Master Data Automation — Consumer Master Update System")
    print("=" * 64)
    print(f"  Starting local server on: {url}")
    print("  Your default web browser will open automatically...")
    print("  To exit, close this window or press Ctrl+C.")
    print("=" * 64)

    # Background browser opener
    def _open_browser():
        time.sleep(1.8)
        try:
            webbrowser.open(url)
        except Exception:
            pass

    threading.Thread(target=_open_browser, daemon=True).start()

    # Import and run Streamlit via bootstrap in-process
    import streamlit.web.bootstrap as bootstrap

    flag_options = {
        "server.port": port,
        "server.headless": False,
        "server.maxUploadSize": 3072,
        "browser.gatherUsageStats": False,
        "global.developmentMode": False,
    }

    bootstrap.run(
        str(app_path),
        is_hello=False,
        args=[],
        flag_options=flag_options,
    )


if __name__ == "__main__":
    main()
