#!/usr/bin/env python3
"""
Satty Screenshot Launcher

Takes a screenshot via the GNOME/XdgDesktopPortal (same idea as Gradia),
then opens the resulting file with Satty (must be in PATH):

    satty --filename <path to screenshot>

Usage:
    python satty_screenshot_launcher.py [--screenshot=INTERACTIVE|FULL] [--delay=N]

Examples:
    python satty_screenshot_launcher.py --screenshot=INTERACTIVE
    python satty_screenshot_launcher.py --screenshot=FULL --delay=3000
"""

import sys
import subprocess

import gi
gi.require_version("Xdp", "1.0")
from gi.repository import Xdp, GLib, Gio


class ScreenshotTaker:
    """Take screenshot via XdgDesktopPortal, return local file path or None."""

    def __init__(self):
        self.portal = Xdp.Portal()
        self._loop = None
        self._result_path = None

    def take_screenshot(
        self,
        flags: Xdp.ScreenshotFlags = Xdp.ScreenshotFlags.INTERACTIVE,
        delay_ms: int = 0,
    ) -> str | None:
        def on_finish(portal, result, user_data):
            try:
                uri = portal.take_screenshot_finish(result)
                file = Gio.File.new_for_uri(uri)
                path = file.get_path()
                if not path:
                    raise RuntimeError("Failed to get local file path from URI")
                self._result_path = path
            except Exception as e:
                print("Screenshot failed:", e, file=sys.stderr)
                self._result_path = None
            finally:
                if self._loop:
                    self._loop.quit()

        def start_screenshot():
            self.portal.take_screenshot(None, flags, None, on_finish, None)
            return False

        self._loop = GLib.MainLoop()
        if delay_ms > 0:
            GLib.timeout_add(delay_ms, start_screenshot)
        else:
            start_screenshot()

        self._loop.run()
        return self._result_path


def run_satty(screenshot_path: str) -> None:
    """Launch Satty with the screenshot file (satty must be in PATH)."""
    subprocess.Popen(
        ["satty", "--filename", screenshot_path],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def main() -> int:
    mode = "INTERACTIVE"
    delay = 0

    for arg in sys.argv[1:]:
        if arg.startswith("--screenshot"):
            parts = arg.split("=", 1)
            mode = (parts[1].strip().upper() if len(parts) == 2 else "INTERACTIVE")
        elif arg.startswith("--delay"):
            parts = arg.split("=", 1)
            if len(parts) == 2:
                try:
                    delay = int(parts[1])
                except ValueError:
                    print("Invalid delay value. Using 0.", file=sys.stderr)
                    delay = 0

    if mode not in ("INTERACTIVE", "FULL"):
        print("Usage: satty_screenshot_launcher.py [--screenshot=INTERACTIVE|FULL] [--delay=N]")
        return 1

    flags = (
        Xdp.ScreenshotFlags.INTERACTIVE
        if mode == "INTERACTIVE"
        else Xdp.ScreenshotFlags.NONE
    )
    taker = ScreenshotTaker()
    screenshot_path = taker.take_screenshot(flags=flags, delay_ms=delay)

    if screenshot_path is None:
        print("Screenshot was cancelled or failed. Exiting.", file=sys.stderr)
        return 1

    run_satty(screenshot_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
