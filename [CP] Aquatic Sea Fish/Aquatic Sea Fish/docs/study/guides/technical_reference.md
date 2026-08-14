# Technical Reference: Quest & Event Implementation

This document serves as the absolute reference for implementing new content in the Willy Expansion mod, based on the established patterns of the original project.

## 1. Dialogue Strategy

### NPC Dialogue Edits
- **Target**: `Characters/Dialogue/[NPC]`
- **Action**: `EditData`
- **Location**: `code/NPCs/[NPC]/dialogue.json`
- **Key Constraints**: Use the provided `[npc]_blacklist.txt` files to avoid overwriting standard dialogue keys unless explicitly intended.

**Key Pattern Example:**
```json
{
    "Action": "EditData",
    "Target": "Characters/Dialogue/Willy",
    "Entries": {
        "spring_Mon": "{{i18n: {{ModId}}_WillyDialogue_Spring_Mon}}"
    }
}
```

---

## 2. Quest System (Item Delivery)

Quests follow a three-part lifecycle: **Trigger -> Delivery -> Registry**.

### Part A: Trigger (`code/Events/triggers.json`)
Use `Data/TriggerActions` with a `DayStarted` trigger.
- **Condition**: Check for season, heart levels, and ensure the player hasn't already received the quest mail.
- **Action**: `AddMail Current [MailID] now`

### Part B: Delivery (`code/Events/mail.json`)
Use `Data/Mail`. The entry must contain the `%item quest [QuestID] %%` command.
- **I18n Format**: `"Letter text... %item quest [QuestID] %% [#][Mail Title]"`

### Part C: Registry (`code/Events/quests.json`)
Use `Data/Quests`. Define the quest mechanics and rewards.
- **Format**: `ItemDelivery/Title/Prompt/Objectives/TargetNPC ItemID Amount/-1/RewardMoney/-1/true/CompletionDialogue`
- **Item ID Syntax**: Use `(O)[ID]` for objects.

---

## 3. Cutscene Implementation (`code/Events/events.json`)

Events are added to location-specific data files (e.g., `Data/Events/Beach`).

### Definition Key
`[EventID]/[Conditions]`
- `f [NPC] [Points]`: 250 points = 1 heart (e.g., `f Willy 750`).
- `t [Start] [End]`: 24h format (e.g., `t 600 2200`).
- `Season [Season]`: `Season spring`, `Season summer`, etc. (Preferred over exclusionary `z` checks or CP `When` blocks).
- `w [weather]`: `w sunny`, `w rainy`.
- `Skill [Name] [Level]`: `Skill Fishing 3`.
- `k [EventID]`: Has NOT seen event ID yet.
- `Tile [x1 y1 x2 y2]`: Trigger when player enters specific tiles.

*Note: The game developer explicitly advises using native event preconditions in the key over Content Patcher `When` blocks wherever possible to reduce unnecessary conditional patching overhead.*

### Script Syntax
`Music/Setup/Visuals/Movements/Dialogue/Cleanup`

**Common Commands Reference:**
- `skippable`: Allows skipping the event.
- `pause [ms]`: Pause execution.
- `speak [NPC] "{{i18n:Token}}"`: NPC dialogue.
- `emote [NPC] [ID]`: 20=heart, 16=music, 32=blush.
- `viewport [x y] true`: Focus camera.
- `move [NPC] [dx dy] [direction] true`: Move character and wait for completion.
- `faceDirection [NPC] [0-3]`: 0=up, 1=right, 2=down, 3=left.
- `itemAboveHead (O)[ID] false`: Player holds item.
- `end [position/direction]`: Terminate event.

---

## 4. Internationalization (i18n)

All user-facing strings must be defined in `i18n/default.json`.
- **Naming Convention**: `{{ModId}}_[Type][NPC]_[Description]`
- **Tokens**: Use `{{ModId}}` as a placeholder for the Unique ID defined in `manifest.json`.
