# Quest Creation Guide

This guide details how to add new quests to ASF, covering the Quest string format, Triggers, and Mail integration.

## Quest Data Format

Quests are defined in `Data/Quests` (see `code/Events/quests.json`). To support multiple languages, the values in `quests.json` point to translation keys (e.g., `"{{i18n:{{ModId}}_QuestWillyGoldenMahiMahi}}"`).

The actual quest logic is defined in `i18n/default.json` as a slash-separated string:

`Type/Title/Description/Objective/Reward/Cancellation/NextQuest/DailyQuest/SpaceUsually`

### Fields Breakdown

1.  **Type**: Usage `ItemDelivery`, `Monster`, etc.
    *   *ASF Usage*: Mostly `ItemDelivery`.
2.  **Title**: The name of the quest shown in the journal.
3.  **Description**: The flavor text describing what needs to be done.
4.  **Objective**: Example: `Bring Willy 5 Mahi Mahis.`
5.  **Reward**: Logic string for completion logic.
    *   Format: `NPC TargetItem Quantity`
    *   Example: `Willy (O)ASF_MahiMahi 5`
6.  **Cancellation**: usually `-1`.
7.  **Reward Money**: Amount of gold (e.g., `1500`).
8.  **NextQuest**: ID of the next quest, or `-1` if none.
9.  **DailyQuest**: `true` or `false` (usually `true` for modded quests to behave correctly in some contexts, though often irrelevant for special orders).
10. **Completion Message**: The dialogue the NPC says when you turn it in.
    *   *Note*: Custom actions can be appended here using `#$action`.
    *   Example: `#$action AddMail Current ASF_QuestWillyGoldenMahiMahiThankYouLetter tomorrow`

### Example (in `i18n/default.json`)
```json
"{{ModId}}_QuestWillyGoldenMahiMahi": "ItemDelivery/Catch More Mahi Mahi/Description.../Bring Willy 5 Mahi Mahis./Willy (O)ASF_MahiMahi 5/-1/15000/-1/true/Thanks!#$action AddMail..."
```

## Starting Quests via Triggers

Quests usually start via letters or interactions. In ASF, we use `Data/TriggerActions` (see `code/Events/triggers.json`) to inject mail or quests based on dynamic conditions.

### Trigger Structure
```json
"{{ModId}}_TriggerName": {
    "Id": "{{ModId}}_TriggerName",
    "Trigger": "LocationChanged",
    "Condition": "PLAYER_LOCATION_NAME Current IslandSouth..., PLAYER_BASE_FISHING_LEVEL Current 7",
    "Actions": [
        "AddMail Current {{ModId}}_QuestWillyGoldenMahiMahiLetter tomorrow"
    ]
}
```

### Common Triggers
-   `DayStarted`: Good for checking weather/season changes.
-   `LocationChanged`: Good for area-specific quests (e.g., entering the Island).

## Mail Integration

Mail is defined in `Data/Mail` (see `code/Events/mail.json`).

To attach a quest to a letter, use the syntax `%item quest QuestID%%` inside the letter text.

### Example
```json
"ASF_QuestWillyGoldenMahiMahiLetter": "Hello @!^^Could you catch me...^^%item quest ASF_QuestWillyGoldenMahiMahi%%[#]Request Letter"
```
