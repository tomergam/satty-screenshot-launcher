# Satty Screenshot Launcher

Takes a screenshot using the same approach as [Gradia](https://github.com/alexandervanhee/gradia): the GNOME/XdgDesktopPortal screenshot flow. Then opens the saved screenshot file in **Satty** with:

```text
satty --filename <path to screenshot>
```

## Requirements

- Python 3 with PyGObject (GObject Introspection)
- `xdg-desktop-portal` and portal implementation (e.g. GNOME’s) for screenshots
- [Satty](https://github.com/noornee/satty) installed and available in your PATH (e.g. in `~/bin` or `/usr/bin`)

### Fedora / RHEL

```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

### Ubuntu / Debian

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
```

## Usage

```bash
# Interactive (select region)
python satty_screenshot_launcher.py --screenshot=INTERACTIVE

# Full screen
python satty_screenshot_launcher.py --screenshot=FULL

# Full screen with 3 second delay
python satty_screenshot_launcher.py --screenshot=FULL --delay=3000
```

Or make the script executable and run it directly:

```bash
chmod +x satty_screenshot_launcher.py
./satty_screenshot_launcher.py --screenshot=INTERACTIVE
```

## GNOME keyboard shortcut

To open Satty with a new screenshot via a shortcut:

1. **Settings → Keyboard → Keyboard Shortcuts → View and customize shortcuts → Custom Shortcuts**
2. Add a shortcut, e.g.:
   - **Name:** Open Satty with screenshot  
   - **Command:** `python3 /path/to/satty-screenshot-launcher/satty_screenshot_launcher.py --screenshot=INTERACTIVE`
3. Assign a key (e.g. `Print Screen` or a custom combo).

## How it works

1. The script uses **Xdp.Portal** (XdgDesktopPortal) to trigger the system screenshot UI (same as Gradia’s `gradia.in`).
2. The portal saves the screenshot and returns a file URI; the script resolves it to a local path.
3. It runs: `satty --filename <path>` so Satty opens that file.

If the screenshot is cancelled or fails, the script exits with code 1 and does not start Satty.
