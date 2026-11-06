# Why I pulled my Plasma panel style into its own project

This began as a small part of my CachyOS desktop: a dark, translucent panel with rounded corners. My personal setup also had more invasive shell and login-screen changes, but those were tightly tied to the installed Plasma version. I wanted the public project to be something smaller that another person could inspect and try.

The published panel background is an original SVG with the frame elements Plasma expects. Breeze provides the elements this package does not override. That keeps the project focused on the panel instead of redistributing an entire desktop theme.

The installer copies the package into the current user's theme directory and leaves the decision to apply it to System Settings. It refuses to overwrite an existing package with the same ID. Removal checks the files against the installation manifest, because deleting someone's later edits would be a poor rollback experience.

Version 0.1.0 was published on November 6, 2026. Six tests passed locally and in CI. The SVG rendered successfully, and an offscreen KSvg frame loaded it on Plasma 6.8.2. Those checks establish that the asset and helper work in the tested environment; they are not a screenshot of the new package applied to a live desktop.

The next useful work is practical: try different panel orientations, display scales and compositor settings. The package does not include my wallpaper, lock-screen modifications or a full desktop preset.

## Keeping this history useful

This is a retrospective of the work that actually led to the first release, not a reconstructed commit sequence. Further changes should be committed as they happen, with plain-language messages explaining the problem, the decision and the checks that were run. Source and documentation were prepared with AI assistance; the verification limits above remain part of the project history.
