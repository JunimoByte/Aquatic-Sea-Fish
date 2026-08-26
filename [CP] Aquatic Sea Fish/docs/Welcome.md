# Developer Guide

A quick reference for navigating the codebase, adding compatibility patches, and contributing to Aquatic Sea Fish (ASF).

## Project Structure

- `assets/` — Texture files and spritesheets (`FishSprite.png`, `AquariumSprite.png`, `ObjectSprite.png`).
- `code/`
  - `Fish/` — Core fish definitions (`fish.json`, `behavior.json`, `pond.json`, `aquarium.json`, `locations.json`).
  - `Events/` — Mail, quests, and trigger actions (`mail.json`, `quests.json`, `triggers.json`).
  - `NPCs/` — Gift tastes and catch dialogue (`dialogue.json`, `gifts.json`).
  - `LocalTokens/` — Reusable local token presets for modular location spawning.
  - `Other/` — Config schemas and tailoring recipes (`config.json`, `tailoring.json`).
  - `Compat/` — Compatibility patches and save migration data.
- `i18n/` — Translation files (`default.json`).
- `docs/` — Developer documentation and reference material.

## Adding Compatibility

When adding support for new locations or custom NPCs from other mods:
1. Create a dedicated subfolder under `code/Compat/Mods/<ModName>/`.
2. Register the include in `code/Compat/index.json` guarded by a `"HasMod": "<ModUniqueID>"` condition.
3. Reuse the presets in `code/LocalTokens/` to keep location spawns modular and consistent.
4. Place any new dialogue or quest text into `i18n/default.json`.

## Contributing

- Keep JSON formatting clean and valid.
- Route all user-facing text (item names, descriptions, letters, dialogue, quests) through `i18n/default.json`.
- Follow the established `{{ModId}}_<Name>` ID naming conventions.
- Test changes with SMAPI to ensure no missing assets, broken tokens, or patch errors.