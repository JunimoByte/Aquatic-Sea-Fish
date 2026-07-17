# Fish Technical Documentation

This document outlines the data structures used for defining fish in ASF and how to add Aquarium compatibility.

## Fish Data Format

Fish are defined in `code/Fish/fish.json` using the standard Stardew Valley object format, but their behavior and spawning logic are controlled via custom properties and context tags.

### Difficulty String Format
When defining custom fish difficulty and behavior, uses the following pipe-separated format:
`"FishID/Difficulty/Type/MinSize/MaxSize/MinAndMaxTime/Season/Weather/Null/MaxDepth/Chance/DepthMulti/FishingLevel/FirstCatchAllowed"`

-   **FishID**: The unique ID of the fish (e.g., `{{ModId}}_SeaTurtle`).
-   **Difficulty**: Integer (e.g., `85`). Higher is harder.
-   **Type**: Movement pattern (`mixed`, `smooth`, `floater`, `sinker`, `dart`).
    -   `floater`: Tends to move up.
    -   `sinker`: Tends to move down.
    -   `dart`: Rapid movement changes.
-   **Conditions**: `sunny`, `rainy`, `both`.
-   **Fishing Level**: Required level to catch.
-   **FirstCatchAllowed**: Whether the fish can be the player's first ever catch.

## Aquarium Support

To add fish to the aquarium, you need to add them to `code/Fish/aquarium.json`. This file maps modded fish to their aquarium animations.

### Data Format
-   **FishID**: The unique ID of the fish (e.g., `{{ModId}}_SeaTurtle`).
-   **Type**: The animation behavior:
    -   `fish`: Standard swimming.
    -   `cephalopod`: Pulsing movement (octopus/jellyfish).
    -   `crawl`: Walking on the bottom (crabs/snails).
    -   `ground`: Stationary on ground (starfish).
    -   `static`: No animation (shells).
    -   `eel`: Serpentine movement.
-   **SpritePath**: Path to the texture (e.g., `Mods\\{{ModId}}\\AquariumSprite`).

### Example
```json
"{{ModId}}_BlueSpottedOctopus": "1/cephalopod/////Mods\\{{ModId}}\\AquariumSprite"
```
This defines the Blue Spotted Octopus using frame 1, behaving like a cephalopod, using the mod's aquarium sprite sheet.