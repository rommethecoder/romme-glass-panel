# Romme Glass Panel

A small Plasma desktop style: dark translucent panels with rounded corners, using Breeze fallback for elements it does not override. Inspired by a personal CachyOS desktop customization; the published SVG is an original, minimal nine-slice asset rather than a copy of the full Breeze theme.

## Install and select

Requires KDE Plasma 6 with Breeze available. Python 3.11+ is needed for the package helper.

```sh
python manage.py check
python manage.py install
```

Then open **System Settings → Colors & Themes → Plasma Style** and select **Romme Glass Panel**. The installer only copies the package into your user data directory; it does not activate a theme, edit system files, patch shell QML or restart Plasma.

If a theme with the same ID already exists, installation refuses to overwrite it. Back up your current package first and choose deliberately whether to replace it. The package does not include an SDDM theme, lock-screen authentication changes, wallpaper, icons or a full desktop preset.

For an isolated installation test:

```sh
python manage.py install --data-home /tmp/my-isolated-theme-data
python manage.py uninstall --data-home /tmp/my-isolated-theme-data --confirm
python -m unittest discover -s tests -v
```

## Appearance and compatibility

The background uses 12-pixel rounded corner slices and a translucent charcoal fill. Blur and final panel appearance depend on the compositor, panel opacity mode, wallpaper and installed Plasma version. Floating-panel behavior is controlled by Plasma; this package does not force a persistent gap through a shell override.

Validation covers the package metadata, SVG structure, required frame elements and isolated install/uninstall behavior. SVG rendering and an offscreen KSvg frame smoke test are recorded in the release notes. Applying this newly packaged asset to a live session and testing multiple panel orientations/scaling factors are manual checks; do not interpret an SVG preview as a full desktop screenshot.

## Remove or roll back

Select Breeze (or your previous style) in System Settings first, then:

```sh
python manage.py uninstall --confirm
```

Removal is limited to a package installed by this helper. Unexpected extra files or symlinks stop automatic removal so modified files are not silently deleted. Restore a previous package from your own backup if needed; the helper does not change your existing theme selection or maintain a backup of someone else's style.

## Design and provenance

The [KDE Plasma style format](https://develop.kde.org/docs/plasma/theme/theme-details/) provides the element/fallback contracts. Breeze remains an installed dependency and is not bundled. Original package assets and helper code are MIT licensed. The package intentionally avoids the version-sensitive Plasma panel and lock-screen QML overrides used in the author's personal setup.
