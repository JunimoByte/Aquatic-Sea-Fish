using System;
using StardewModdingAPI;
using StardewModdingAPI.Events;
using StardewValley;
using StardewValley.Buildings;
using Object = StardewValley.Object;

namespace AquaticSeaFishCode
{
    internal sealed class ModEntry : Mod
    {
        private const string OldPrefix = "ASF_";
        private const string NewPrefix = "LucyTheDove.ASF_";
        private const string SaveDataKey = "MigrationStatus";
        private const string LegacySaveDataKey = "BaitMigrationDone";

        public override void Entry(IModHelper helper)
        {
            helper.Events.GameLoop.SaveLoaded += this.OnSaveLoaded;
        }

        private void OnSaveLoaded(object? sender, SaveLoadedEventArgs e)
        {
            if (!Context.IsMainPlayer)
                return;

            var record = this.Helper.Data.ReadSaveData<MigrationRecord>(SaveDataKey) ?? new MigrationRecord();

            if (!record.BaitDone && this.Helper.Data.ReadSaveData<MigrationRecord>(LegacySaveDataKey)?.Done == true)
                record.BaitDone = true;

            bool changed = false;

            if (!record.BaitDone)
            {
                int count = MigrateBait();
                record.BaitDone = true;
                changed = true;
                if (count > 0)
                    this.Monitor.Log($"[ASF] Migrated {count} legacy bait/preserved item(s).", LogLevel.Info);
            }

            if (!record.PondsDone)
            {
                int count = MigratePonds();
                record.PondsDone = true;
                changed = true;
                if (count > 0)
                    this.Monitor.Log($"[ASF] Migrated {count} legacy fish pond(s).", LogLevel.Info);
            }

            if (changed)
                this.Helper.Data.WriteSaveData(SaveDataKey, record);
        }

        // Scans every item in the world (inventories, chests, rods, and update ASF to LucyTheDove.ASF)
        private static int MigrateBait()
        {
            int count = 0;

            Utility.ForEachItem(item =>
            {
                if (item is Object obj)
                    count += TryMigratePreserved(obj);
                return true;
            });

            return count;
        }

        // Scans every building for fish ponds with legacy fishType IDs
        private static int MigratePonds()
        {
            int count = 0;

            Utility.ForEachBuilding(building =>
            {
                if (building is not FishPond pond)
                    return true;

                string? fishId = pond.fishType.Value;
                if (!string.IsNullOrEmpty(fishId))
                {
                    string? newId = null;

                    if (fishId.StartsWith(OldPrefix, StringComparison.Ordinal))
                        newId = NewPrefix + fishId[OldPrefix.Length..];
                    else if (fishId.StartsWith("(O)" + OldPrefix, StringComparison.Ordinal))
                        newId = NewPrefix + fishId[("(O)" + OldPrefix).Length..];

                    if (newId != null)
                    {
                        pond.fishType.Value = newId;
                        pond.UpdateMaximumOccupancy();
                        pond.GetFishPondData();
                        count++;
                    }
                }

                // Migrate roe/produce sitting in the output basket
                if (pond.output.Value is Object outputObj)
                    TryMigratePreserved(outputObj);

                // Migrate any fish shown on an attached sign
                if (pond.sign.Value is Object signObj && signObj.heldObject.Value is Object heldObj)
                {
                    if (heldObj.ItemId?.StartsWith(OldPrefix, StringComparison.Ordinal) == true)
                        heldObj.ItemId = NewPrefix + heldObj.ItemId[OldPrefix.Length..];
                }

                return true;
            });

            return count;
        }

        // Updates preservedParentSheetIndex on a single Object if it contains a legacy ID
        private static int TryMigratePreserved(Object obj)
        {
            string? preserved = obj.preservedParentSheetIndex.Value;
            if (string.IsNullOrEmpty(preserved))
                return 0;

            if (preserved.StartsWith(OldPrefix, StringComparison.Ordinal))
            {
                obj.preservedParentSheetIndex.Value = NewPrefix + preserved[OldPrefix.Length..];
                return 1;
            }

            const string qualifiedOld = "(O)" + OldPrefix;
            if (preserved.StartsWith(qualifiedOld, StringComparison.Ordinal))
            {
                obj.preservedParentSheetIndex.Value = NewPrefix + preserved[qualifiedOld.Length..];
                return 1;
            }

            return 0;
        }
    }

    internal sealed class MigrationRecord
    {
        public bool Done { get; set; }
        public bool BaitDone { get; set; }
        public bool PondsDone { get; set; }
    }
}
