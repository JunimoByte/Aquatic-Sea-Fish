# Technical Guide: Quests and Events Implementation

This guide documents how to add new quests and cutscenes to the mod, based on the implementation used for Evelyn and George.

## 1. Adding Quests

Quests in this mod are "Item Delivery" quests triggered by mail.

### Step A: Define the Quest (`code/Events/quests.json`)
Add an entry to `Data/Quests`.
**Format:**
`Type/Title/Prompt/Objectives/NPC ItemID Amount/-1/RewardMoney/-1/true/CompletionDialogue`

**Example:**
```json
"LucyTheDove.EvelynExpansion_EvelynTulipQuest": "ItemDelivery/Tulip Season/Evelyn would like a fresh Tulip to brighten up her living room./Bring Evelyn 1 Tulip./Evelyn (O)591 1/-1/100/-1/true/Oh, what a beautiful tulip!...$h"
```

### Step B: Create the Mail (`code/Events/mail.json`)
Add an entry to `Data/Mail`. The mail MUST include the quest command.
**Format:**
`[Text] %item quest [QuestID] %% [#][MailTitle]`

**Example (inside i18n):**
`"Hello dear... %item quest LucyTheDove.EvelynExpansion_EvelynTulipQuest %% [#]Letter from Evelyn"`

### Step C: Set the Trigger (`code/Events/triggers.json`)
Add a trigger to `Data/TriggerActions` to send the mail when conditions are met.
**Example:**
```json
"{{ModId}}_EvelynTulipQuestTrigger": {
    "Id": "{{ModId}}_EvelynTulipQuestTrigger",
    "Trigger": "DayStarted",
    "Condition": "SEASON Spring, PLAYER_HEARTS Current Evelyn 3, !PLAYER_HAS_MAIL Current {{ModId}}_EvelynTulipQuestLetter",
    "Actions": [
        "AddMail Current {{ModId}}_EvelynTulipQuestLetter now"
    ]
}
```

---

## 2. Adding Cutscenes (Events)

Cutscenes are added to specific locations in `code/Events/events.json`.

### Step A: Define the Key
The key is added to `Data/Events/[Location]`.
**Format:** `[EventID]/[Conditions]`

**Common Conditions (Native Preconditions Preferred):**
- **Friendship**: `f [NPC] [Points]` (e.g., `f Willy 750` for 3 hearts).
- **Time**: `t [Start] [End]` (e.g., `t 600 2200`).
- **Season**: `Season [Season]` (e.g., `Season Fall`). Do *not* use CP `When` blocks for seasons if native preconditions work.
- **Weather**: `w sunny` or `w rainy`.
- **Skill**: `Skill [SkillName] [Level]` (e.g., `Skill Fishing 3`).
- **Not Seen Event**: `k [EventID]` (safer than CP event checks).
- **Tile**: `Tile [x1 y1 x2 y2...]` (Trigger when walking on these tiles).

*Developer Advice: Avoid conditional patching (CP `When` blocks) as much as possible. If it's an event precondition, use the native precondition in the event key!*

### Step B: Write the Script
The value is the event script string.
**General Flow:**
1. `MusicName`
2. `StartingPositions` (e.g., `-1000 -1000` for off-screen, or specific tiles)
3. `Setup Commands`: `skippable`, `ignoreCollisions farmer`.
4. `Visuals`: `viewport [x y] true`, `pause [ms]`, `globalFade`.
5. `Movements`: `move [Name] [dx dy] [direction] [true/false]`.
6. `Dialogue`: `speak [Name] "{{i18n:Token}}"`.
7. `Interactions`: Use `quickQuestion` to keep all branching dialogue logic smashed into a single line. Example: `quickQuestion Prompt#Opt1#Opt2(break)speak [Name] \"Yes!\"(break)speak [Name] \"No!\"`.
8. `Cleanup`: `globalFade`, `viewport -1000 -1000`, `end`.

**Special Commands Used:**
- `advancedMove [NPC] false [commands]`: Complex movement paths.
- `emote [Name] [ID]`: Show mood bubbles (e.g., 20 for heart, 16 for music note).
- `playSound [Name]`: Play SFX (e.g., `smooch`, `waterSlosh`).
- `positionOffset [Name] [dx dy]`: Subtle position shifts (used for the kiss in Evelyn's 8-heart event).
- `addObject [x y] (O)[ID]`: Place object on ground.
- `itemAboveHead (O)[ID] false`: Player holds item.

---

## 3. Branching Dialogue (`quickQuestion`)

Standardize on the `quickQuestion` command to handle all branching dialogue. This allows you to smash all of the outcome paths into a single event line using the `(break)` syntax and `\\` delimiters for commands inside branches.

**The Prompt Text Rule:**
The actual prompt that appears above the options (e.g., `"Will you catch a Super Cucumber for Willy?"`) must **NOT** be heavily stylized or poetic (e.g., `"Will you brave the storm for Willy?"`). It must be brutally clear and to the point about what the player is actually agreeing to do. Keep the atmospheric dialogue strictly within the NPC's actual speech lines before the prompt is fired.

**Implementation:**
Use the `quickQuestion` architecture to embed branches directly into the main event script:

```json
"{{ModId}}_MyEvent": ".../speak NPC \"Will you help?\"/quickQuestion {{i18n:Prompt}}#{{i18n:Yes}}#{{i18n:No}}(break)pause 500\\speak NPC \"Thank you!\"\\action AddQuest {{ModId}}_MyQuest(break)pause 500\\speak NPC \"Okay, bye.\"/end"
```
*Why it works:* It keeps your event script centralized in one place instead of spawning dozens of confusing `fork` script keys, keeping the logic smashed into a single line!

---

## 4. The Screen Fade-In Freeze Bug (Dark Screen issue)

**WARNING:** If a cutscene triggers immediately upon entering a new location (e.g. walking through a door), the game engine uses a ~1000ms fade-in transition overlay to smoothly load the room. 

If your event script spawns a dialogue box (using a `speak` command) while this fade-in animation is still running, it will freeze game time. Because game time controls the screen fade animation, the screen will remain permanently dark or pitch-black until the player clicks to dismiss the dialogue, at which point the fade suddenly completes.

**The Solution (`pause 1500`):**
To ensure the room is fully visible before any dialogue pops up, always begin your "warp-in" events with a healthy pause command (minimum 1500ms).

```json
// BAD: Dialogue pops up while screen is still fading in, freezing the UI on black
"{{ModId}}_MyEvent": "none/14 19/.../pause 500/speak Gus \"Hello!\""

// GOOD: The system fully un-fades organically, then Gus speaks.
"{{ModId}}_MyEvent": "none/14 19/.../pause 1500/speak Gus \"Hello!\""
```

---

## 5. Mid-Scene Black Overlay Bug (`viewport` with `true`)

**WARNING:** Using `viewport [x y] true` mid-scene causes a **second** black overlay to appear while the camera animates to its destination. This overlay persists until the animation ends, which can be several seconds into dialogue.

The `true` flag triggers an animated camera pan, which fires the engine's internal transition overlay on top of the already-running event. This is especially visible on Farm events where the map loads with a fade-in.

**The Solution — bake the camera into the script header:**
Instead of using a `viewport` command at all, set the starting camera position directly in **slot 2** of the event script (between the music track and the actor positions):

```json
// BAD: Camera starts off-screen and pans with an overlay
"{{ModId}}_MyFarmEvent": "none/-1000 -1000/farmer 64 15 2 .../viewport 64 15 true/speak NPC ..."

// GOOD: Camera is already at the right position — no pan, no overlay
"{{ModId}}_MyFarmEvent": "none/64 15/farmer 64 15 2 .../speak NPC ..."
```

Slot 2 is the **starting camera anchor**. Set it to match your actor positions and you will never need a `viewport` command at all for static scenes.

**Farm Events: Do NOT use `globalFade/viewport -1000 -1000/end`:**
On large or modded Farm maps, `viewport -1000 -1000` snaps the camera to a far-off void position, and the `end` command then warps the player to a random tile on the massive map. For Farm events, simply end with `/end` alone — it returns the player to exactly where they stood when the event triggered, with no teleport.

```json
// BAD: teleports farmer to a random tile on large farm maps
"...": "none/64 15/.../globalFade/viewport -1000 -1000/end"

// GOOD: player stays exactly where they were
"...": "none/64 15/.../end"
```

---

## 6. Event Data Formatting Bugs (`quickQuestion` backslashes)

When using `quickQuestion`, be extremely careful with JSON backslashes and the `(break)` syntax:

- **Inside branches**: SDV splits `quickQuestion` inline commands using a single backslash `\`. In JSON, you must escape it exactly once as `\\`. If you accidentally use `\\\\` (four backslashes), SDV processes it as `\\` and crashes with an *empty command* parse error.
- **Closing the sequence**: The `(break)` command separates options. Never put a `(break)` at the very end of your options list. To resume normal unbranched event execution, simply use the standard forward-slash `/` after the final response option.

---

## 6. Best Practices for Willy & Elliott
- **Willy**: Focus on `Data/Events/Beach` and `Data/Events/FishShop`.
- **Elliott**: Focus on `Data/Events/ElliottHouse` and `Data/Events/Beach`.
- Keep IDs consistent: `{{ModId}}_Willy[Quest/Event]Name`.
- Use the 1.6 `TriggerActions` for all quest mail to ensure they fire correctly.
