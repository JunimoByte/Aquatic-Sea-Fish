This page documents the custom trigger actions added by Content Patcher.

🌐 In other languages: zh (中文).

Contents
MigrateIds
See also
MigrateIds
The Pathoschild.ContentPatcher_MigrateIds trigger action lets you update existing saves when you change IDs for your events, items, mail, recipes, or songs. For example, this can be used to migrate to unique string IDs.

The argument format is <type> [<old id> <new id>]+:

argument	usage
<type>	
One of Buildings, CookingRecipes, CraftingRecipes, Events, FarmAnimals, Items, Mail, or Songs.

<old id>	
The former ID to find in the game data.

If this is an item and it was previously defined...

In a data asset like Data/Objects:
Use the qualified item ID, like (O)OldId.
In a non-installed Json Assets content pack:
Use an ID in the form "JsonAssets:<type>:<name>". The valid types are big-craftables, clothing, hats, objects, and weapons. For example, a hat named Puffer Hat would be "JsonAssets:hats:Puffer Hat".
In an installed Json Assets content pack:
Use a Json Assets token to get the real item ID, and then use it as a qualified item ID. For example, (O){{spacechase0.JsonAssets/ObjectId: Puffer Hat}}.
<new id>	
The new ID to change it to.

For an item, using a qualified item ID is recommended to avoid ambiguity.

You can have any number old/new ID pairs.

For example, this changes the ID for two crafting recipes: Puffer Plush renamed to {{ModId}}_PufferPlush, and Puffer Sofa renamed to {{ModId}}_PufferSofa:

{
    "Action": "EditData",
    "Target": "Data/TriggerActions",
    "Entries": {
        "{{ModId}}_MigrateIds": {
            "Id": "{{ModId}}_MigrateIds",
            "Trigger": "DayStarted",
            "Actions": [
                // Note: use double-quotes around an argument if it contains spaces. This example has single-quotes for
                // the action itself, so we don't need to escape the double-quotes inside it.
                'Pathoschild.ContentPatcher_MigrateIds CraftingRecipes "Puffer Plush" {{ModId}}_PufferPlush "Puffer Sofa" {{ModId}}_PufferSofa'
            ],
            "HostOnly": true
        }
    }
}
Important

Content Patcher needs full access to the whole game state to do this. The action will log an error if:

it isn't set to "Trigger": "DayStarted" and "HostOnly": true.
or it's not being run from Data/TriggerActions.
See also
Author guide for other actions and options
Trigger actions on the wiki for more info