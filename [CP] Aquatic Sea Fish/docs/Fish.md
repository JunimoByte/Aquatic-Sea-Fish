# Fish Technical Documentation

Reference guide for defining fish data, behavior, pond output, location spawns, and aquarium animations in Aquatic Sea Fish (ASF).

---

## 1. Object Definition (`code/Fish/fish.json`)

Fish are registered in `Data/Objects` using Stardew Valley 1.6 object data schema:

```json
"{{ModId}}_SeaTurtle": {
  "Name": "{{ModId}}_SeaTurtle",
  "DisplayName": "{{i18n:{{ModId}}_SeaTurtle.displayname}}",
  "Description": "{{i18n:{{ModId}}_SeaTurtle.description}}",
  "Type": "Fish",
  "Category": -4,
  "Price": 90,
  "Texture": "Mods/{{ModId}}/FishSprite",
  "SpriteIndex": 0,
  "Edibility": -20,
  "ContextTags": [
    "season_spring",
    "season_summer",
    "fish_ocean"
  ]
}
```

---

## 2. Minigame & Fishing Behavior (`code/Fish/behavior.json`)

Fishing minigame difficulty and basic spawn rules are added to `Data/Fish` using the slash-separated vanilla string format:

`FishID/Difficulty/Type/MinSize/MaxSize/TimeRange/Seasons/Weather/Unused/MaxDepth/SpawnChance/DepthMultiplier/FishingLevel/FirstCatchAllowed`

### Field Breakdown

| Field | Example | Notes |
| :--- | :--- | :--- |
| **FishID** | `{{ModId}}_SeaTurtle` | Matches the object key. |
| **Difficulty** | `49` | Minigame bar difficulty (higher = faster/harder). |
| **Type** | `sinker` | Movement pattern: `mixed`, `smooth`, `floater`, `sinker`, `dart`. |
| **MinSize / MaxSize** | `5/9` | Size range in inches. |
| **TimeRange** | `600 1800` | Start and end time in military format (can have multiple pairs, e.g. `600 1000 1700 2000`). |
| **Seasons** | `spring summer` | Space-separated seasons: `spring`, `summer`, `fall`, `winter`. |
| **Weather** | `sunny` | `sunny`, `rainy`, or `both`. |
| **Unused** | `685 .35` | Legacy bait/trap field placeholder. |
| **MaxDepth** | `2` | Minimum water depth to start spawning. |
| **SpawnChance** | `.25` | Base chance to hook when water depth criteria are met. |
| **DepthMultiplier** | `.1` | Chance increase per unit of depth. |
| **FishingLevel** | `0` | Minimum required fishing level. |
| **FirstCatchAllowed** | `false` | Whether this fish can be caught during the tutorial/first catch. |

---

## 3. Location Spawning (`code/Fish/locations.json`)

ASF hooks into `Data/Locations` using 1.6 location data queries:

```json
{
  "Id": "{{ModId}}_SeaTurtle_Beach",
  "ItemId": "(O){{ModId}}_SeaTurtle",
  "Chance": 0.08,
  "Season": "Spring, Summer",
  "Condition": "!IS_EVENT_FESTIVAL",
  "Precedence": -10
}
```

---

## 4. Fish Pond Production (`code/Fish/pond.json`)

Pond data is added to `Data/FishPondData` keyed by item ID:

- `SpawnTime`: Days between fish population growth.
- `ProducedItems`: Array of drops with `RequiredPopulation`, `Chance`, `ItemID`, `MinStack`, `MaxStack`.
- `PopulationGates`: Dictionary mapping population thresholds (`"3"`, `"5"`, `"8"`) to required unlock items.
- `WaterColor`: Hex color for tinted pond water (e.g., `"#003080"` for Marlin).

---

## 5. Aquarium Support (`code/Fish/aquarium.json`)

Tank animations are registered in `Data/AquariumFish` using the vanilla aquarium format:

`SpriteFrame/AnimationType/Velocity/TankType/IdleBehavior/TexturePath`

### Example
```json
"{{ModId}}_BlueSpottedOctopus": "1/cephalopod/////Mods\\{{ModId}}\\AquariumSprite"
```

### Supported Animation Types
- `fish` — Normal directional swimming.
- `cephalopod` — Pulsing up/down motion (octopuses, jellies).
- `crawl` — Walks along the aquarium floor (crabs, snails).
- `ground` — Sits stationary on the substrate (starfish).
- `eel` — Serpentine undulating swim path.
- `static` — Stationary non-animated object (shells, pearls).