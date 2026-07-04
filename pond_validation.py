import json
import os
import re
import sys
import unicodedata
from collections import Counter

def normalize_text(text):
    if not text:
        return ""
    nfkd_form = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def parse_item_ids(filepath):
    item_map = {}
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.", file=sys.stderr)
        return item_map

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f]

    for i, line in enumerate(lines):
        match = re.match(r'^\[([^\]]+)\]$', line)
        if match:
            item_id = match.group(1)
            if i > 0:
                name = lines[i-1]
                item_map[item_id] = name
    return item_map


def validate_pond_comments(pond_path, item_map):
    errors_count = 0
    item_id_re = re.compile(r'"ItemID"\s*:\s*"([^"]*)"(.*)')
    gate_line_re = re.compile(r'"\(([A-Z]+)\)([^\s\"]+)\s+(\d+)"(.*)')
    gate_comment_re = re.compile(r'(.*?)\s*[x×]\s*(\d+)\s*$')

    with open(pond_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if "ItemID" in line:
                match = item_id_re.search(line)
                if not match:
                    print(f"Line {line_num}: [ERROR] Unable to parse ItemID line structure: {line.strip()}")
                    errors_count += 1
                    continue

                item_id_val = match.group(1)
                remainder = match.group(2)

                is_o_prefix = item_id_val.startswith("(O)")
                is_skipped_prefix = item_id_val.startswith("(F)") or item_id_val.startswith("(BC)")

                item_id = None
                if is_o_prefix:
                    item_id = item_id_val.split("(O)", 1)[1]
                elif is_skipped_prefix:
                    pass
                else:
                    print(f"Line {line_num}: [ERROR] ItemID value '{item_id_val}' does not have a recognized prefix (expected '(O)', '(F)', or '(BC)').")
                    errors_count += 1

                comment_match = re.search(r'//\s*(.*)', remainder)
                if comment_match:
                    comment = comment_match.group(1).strip()
                else:
                    print(f"Line {line_num}: [ERROR] Comment is missing at the end of the ItemID field (value: '{item_id_val}').")
                    errors_count += 1
                    comment = None

                if is_o_prefix and item_id is not None:
                    if item_id not in item_map:
                        print(f"Line {line_num}: [ERROR] Item ID '{item_id}' does not exist in ItemId.txt.")
                        errors_count += 1
                    elif comment is not None:
                        expected_name = item_map[item_id]
                        if normalize_text(comment) != normalize_text(expected_name):
                            print(f"Line {line_num}: [ERROR] Comment '{comment}' does not match the name '{expected_name}' for ID '{item_id}' in ItemId.txt.")
                            errors_count += 1
            else:
                gate_match = gate_line_re.search(line)
                if gate_match:
                    prefix = gate_match.group(1)
                    item_id = gate_match.group(2)
                    coded_qty = gate_match.group(3)
                    remainder = gate_match.group(4)

                    if prefix not in ["O", "F", "BC"]:
                        print(f"Line {line_num}: [ERROR] PopulationGates entry has an unrecognized prefix '{prefix}' (expected 'O', 'F', or 'BC').")
                        errors_count += 1
                        continue

                    comment_match = re.search(r'//\s*(.*)', remainder)
                    if comment_match:
                        comment = comment_match.group(1).strip()
                        comment_info_match = gate_comment_re.match(comment)
                        if comment_info_match:
                            commented_name = comment_info_match.group(1).strip()
                            commented_qty = comment_info_match.group(2)

                            if commented_qty != coded_qty:
                                print(f"Line {line_num}: [ERROR] PopulationGates quantity mismatch on '{item_id}': comment specifies '{commented_qty}' but code specifies '{coded_qty}'.")
                                errors_count += 1

                            if prefix == "O":
                                if item_id not in item_map:
                                    print(f"Line {line_num}: [ERROR] Item ID '{item_id}' in PopulationGates does not exist in ItemId.txt.")
                                    errors_count += 1
                                else:
                                    expected_name = item_map[item_id]
                                    if normalize_text(commented_name) != normalize_text(expected_name):
                                        print(f"Line {line_num}: [ERROR] PopulationGates comment name '{commented_name}' does not match the name '{expected_name}' for ID '{item_id}' in ItemId.txt.")
                                        errors_count += 1
                        else:
                            print(f"Line {line_num}: [ERROR] PopulationGates comment '{comment}' is not formatted correctly (expected 'Item Name xQuantity').")
                            errors_count += 1
                    else:
                        print(f"Line {line_num}: [ERROR] Comment is missing in PopulationGates entry (value: '{gate_match.group(0).strip()}').")
                        errors_count += 1

    return errors_count


def validate_pond_structure(pond_path, item_map):
    errors_count = 0

    with open(pond_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content_clean = re.sub(r'//[^\r\n]*', '', content)
    try:
        data = json.loads(content_clean)
    except json.JSONDecodeError as e:
        print(f"[ERROR] pond.json is not valid JSON (after stripping comments): {e}")
        return 1

    entries = data.get('Changes', [{}])[0].get('Entries', {})

    for fish_name, fish_data in entries.items():
        produced = fish_data.get('ProducedItems', [])
        ids_seen = []
        last_pop = -1

        for item in produced:
            rp = item.get('RequiredPopulation', 0)
            chance = item.get('Chance', 0)
            mn = item.get('MinQuantity', 1)
            mx = item.get('MaxQuantity', 1)
            iid = item.get('ItemID', '')

            # Chance out of 0, 1
            if not (0 < chance <= 1.0):
                print(f"[{fish_name}]: [ERROR] ItemID '{iid}' has Chance={chance} which is not in range (0, 1].")
                errors_count += 1

            # MinQuantity > MaxQuantity
            if mn > mx:
                print(f"[{fish_name}]: [ERROR] ItemID '{iid}' has MinQuantity={mn} > MaxQuantity={mx}.")
                errors_count += 1

            # RequiredPopulation
            if rp < last_pop:
                print(f"[{fish_name}]: [ERROR] RequiredPopulation={rp} comes after RequiredPopulation={last_pop} — must be non-descending.")
                errors_count += 1
            last_pop = rp

            ids_seen.append(iid)

        # Duplicate ItemIDs
        for iid, count in Counter(ids_seen).items():
            if count > 1:
                print(f"[{fish_name}]: [ERROR] ItemID '{iid}' appears {count} times in ProducedItems (possible duplicate).")
                errors_count += 1

        # PopulationGates
        gates = fish_data.get('PopulationGates', {})
        if gates:
            gate_keys = [int(k) for k in gates.keys()]
            sorted_keys = sorted(gate_keys)
            if gate_keys != sorted_keys:
                print(f"[{fish_name}]: [ERROR] PopulationGates keys are not in ascending order: {gate_keys}.")
                errors_count += 1

    return errors_count


def validate_pond(pond_path, item_map):
    print("\n--- Pass 1: Comment & ID Validation ---")
    comment_errors = validate_pond_comments(pond_path, item_map)
    if comment_errors == 0:
        print("  No comment/ID errors found.")

    print("\n--- Pass 2: Structural Validation ---")
    struct_errors = validate_pond_structure(pond_path, item_map)
    if struct_errors == 0:
        print("  No structural errors found.")

    return (comment_errors + struct_errors) == 0


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    item_id_path = os.path.join(base_dir, "ItemId.txt")
    pond_json_path = os.path.join(base_dir, "code", "Fish", "pond.json")

    print("Parsing ItemId.txt...")
    item_map = parse_item_ids(item_id_path)
    print(f"Loaded {len(item_map)} items from ItemId.txt.")

    print("\nValidating pond.json...")
    success = validate_pond(pond_json_path, item_map)

    if success:
        print("\n[SUCCESS] pond.json validation passed with 0 errors!")
        sys.exit(0)
    else:
        print("\n[FAILURE] pond.json validation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
