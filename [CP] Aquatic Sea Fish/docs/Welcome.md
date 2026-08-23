# Aquatic Sea Fish - Developer Guide

Welcome to the development documentation for Aquatic Sea Fish (ASF). This guide is intended for modders who want to understand the project structure, contribute, add compatibility, or maintain my mod if I left one day.

## Project Structure

The mod is organized into the following directories:

-   **assets**: Contains all graphical assets (spritesheets, portraits, etc.).
-   **code**: The core logic, split into submodules:
    -   `Fish`: Definitions for new fish and their behaviors.
    -   `NPCs`: Dialogue and gift taste changes.
    -   `Events`: Quests, mail, and event triggers.
    -   `LocalTokens`: Grouped LocalTokens for fish/object placement.
    -   `Other`: Miscellaneous items like configuration or tailoring recipes.
    -   `Compat`: Compatibility patches for other mods.
-   **docs**: Documentation files (you are here).
-   **i18n**: Translation files for localization.

## Adding Compatibility

To add compatibility with another mod:
1.  Check `code/Compat` for existing examples.
2.  Use Content Patcher's `EditData` or `Include` actions based on the `HasMod` condition.
3.  Ensure any new assets are placed in `assets` and referenced correctly.

## Contribution

If you wish to contribute:
-   Ensure JSON is valid.
-   Add localization strings to `i18n/default.json`.
-   Read the other documentation files to understand the project structure.
-   Send me a message for me to verify your changes and accept the request, otherwise, I will not accept the request.