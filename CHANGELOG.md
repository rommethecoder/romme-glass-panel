# Changelog

## 0.1.0 — 2026-11-06

Initial public implementation. See README.md for scope, test commands, provenance and outstanding live/device checks.

## Verification — 2026-11-06

6 unittest cases passed: SVG/metadata contract, isolated install/remove, existing-package refusal, symlink rejection, and preservation of modified/unmanaged packages. rsvg-convert rendered the SVG and an offscreen Plasma KSvg FrameSvgItem loaded it with positive frame margins on Plasma 6.8.2. The package was not applied to the live desktop; panel orientations, display scaling, blur and compositor behavior remain manual checks.
