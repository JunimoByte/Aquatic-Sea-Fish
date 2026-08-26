# Quests & Events Documentation

Reference guide for creating and triggering custom quests, letters, and actions in Aquatic Sea Fish (ASF).

---

## 1. Quest Definition (`code/Events/quests.json`)

Quests are registered in `Data/Quests` and point to translation keys in `i18n/default.json`:

```json
"{{ModId}}_QuestWillyGoldenMahiMahi": "{{i18n:{{ModId}}_QuestWillyGoldenMahiMahi}}"
```

The underlying quest logic string uses the slash-separated vanilla format:

`Type/Title/Description/Objective/Target/NextQuest/MoneyReward/RewardDescription/Cancellable/CompletionMessage`

### Field Breakdown

| Field | Example | Notes |
| :--- | :--- | :--- |
| **Type** | `ItemDelivery` | Quest archetype (mostly `ItemDelivery` in ASF). |
| **Title** | `Catch More Mahi Mahi` | Name displayed in the player's quest journal. |
| **Description** | `Willy asked for a Mahi Mahi...` | Full journal text describing the request. |
| **Objective** | `Bring Willy 1 Mahi Mahi.` | Short objective line shown on the HUD / checklist. |
| **Target** | `Willy (O){{ModId}}_MahiMahi 1` | `NPC (O)ItemID Quantity`. |
| **NextQuest** | `-1` | Next chained quest ID, or `-1` if none. |
| **MoneyReward** | `1000` | Gold awarded upon completion (`-1` for none). |
| **RewardDescription** | `-1` | Custom reward text or `-1`. |
| **Cancellable** | `true` | Whether the player can abandon the quest. |
| **CompletionMessage** | `Thanks! #$action AddMail ...` | NPC dialogue on hand-in. Supports inline `#$action` calls. |

---

## 2. Trigger Actions (`code/Events/triggers.json`)

ASF uses `Data/TriggerActions` to start quests or send letters automatically based on player progress:

```json
{
  "Id": "{{ModId}}_Trigger_WillyGoldenMahiMahi",
  "Trigger": "LocationChanged",
  "Condition": "PLAYER_LOCATION_NAME Current IslandSouth, PLAYER_BASE_FISHING_LEVEL Current 7",
  "Action": "AddMail Current {{ModId}}_QuestWillyGoldenMahiMahiLetter tomorrow"
}
```

### Common Triggers & Conditions
- `DayStarted` — Fires each morning (ideal for seasonal checks and weather triggers).
- `LocationChanged` — Fires when entering a new map (e.g. Ginger Island or Submarine).
- `PLAYER_HAS_MAIL Current <MailId>` / `!PLAYER_HAS_MAIL Current <MailId>` — Checks if a letter has already been delivered.
- `PLAYER_HAS_CAUGHT_FISH Current <FishId>` — Checks if a specific fish is recorded in the player's catches.

---

## 3. Mail Integration (`code/Events/mail.json`)

Letters are registered in `Data/Mail`. To attach an interactive quest to a letter, use the `%item quest <QuestId>%%` tag:

```json
"{{ModId}}_QuestWillyGoldenMahiMahiLetter": "{{i18n:{{ModId}}_QuestWillyGoldenMahiMahiLetter}}"
```

### Example Letter Format (`i18n/default.json`)
```
Hello @!^^If you make it to Ginger Island, bring me a fresh Mahi Mahi.^^- Willy^^%item quest {{ModId}}_QuestWillyGoldenMahiMahi%%[#]Letter from Willy
```
- `@` — Replaced by the player's name.
- `^^` — Line break.
- `%item quest <Id>%%` — Attaches the quest accept button to the letter.
- `[#]<Title>` — Mail header title in the letter box.

---

## 4. Special Orders (`code/Events/orders.json`)

Special orders are registered in `Data/SpecialOrders` for both the Pelican Town Special Orders Board and Mr. Qi's Walnut Room Board:

```json
"{{ModId}}_SpecialOrder_ForbiddenPredators": {
  "Name": "{{i18n:{{ModId}}_SpecialOrder_ForbiddenPredators_Name}}",
  "Requester": "Qi",
  "Duration": "Week",
  "Repeatable": "True",
  "OrderType": "Qi",
  "Objectives": [ ... ],
  "Rewards": [ { "Type": "Gems", "Data": { "Amount": "35" } } ]
}
```

### Active Special Orders in ASF

| Board | Order Name | Requester | Type | Reward |
| :--- | :--- | :--- | :--- | :--- |
| **Town** | **Spring Tide Bounty** | Willy | Repeatable (`season_spring`) | 1,500g + 250 Friendship |
| **Town** | **Summer Coastal Catch** | Gus | Repeatable (`season_summer`) | 1,500g + 250 Friendship |
| **Town** | **Autumn Nocturnal Survey** | Demetrius | Repeatable (`season_fall`) | 1,500g + 250 Friendship |
| **Town** | **Winter Star Shoal** | Willy | Repeatable (`season_winter`) | 1,500g + 250 Friendship |
| **Town** | **Ginger Island Research** | Demetrius | Repeatable (`island`) | 2,000g + 250 Friendship |
| **Town** | **The Coastal Smokehouse** | Willy | Repeatable (`Ship` Smoked Fish) | 2,000g + 15 Deluxe Bait + 250 Friendship |
| **Town** | **Coastal Companions** | Linus | Non-repeatable (`season_spring`, Lvl 8+) | 1 Ancient Fruit + 500 Friendship |
| **Town** | **Prismatic Tears** | Willy | Non-repeatable Master Challenge | 1 Prismatic Mermaid's Tear + 500 Friendship |
| **Qi** | **Forbidden Predators** | Qi | Repeatable (Qi Walnut Room Board) | 25 Qi Gems |
| **Qi** | **Island Population Control** | Qi | Repeatable (Catch 30 Island Critters) | 20 Qi Gems |
