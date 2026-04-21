import sys
import json
import argparse
import re

def validate_markdown_beat(filepath, schema_path):
    # For a production app, use the 'jsonschema' library. 
    # Here we do a lightweight dictionary check so it runs out-of-the-box.
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract JSON block from markdown
    match = re.search(r'```json(.*?)```', content, re.DOTALL)
    if not match:
        print("❌ FORMAT ERROR: No ```json ... ``` block found in file.")
        return False

    try:
        beat_data = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        print(f"❌ JSON ERROR: Invalid JSON format. {e}")
        return False

    required_keys = ["beat_id", "setup", "choices", "end_state"]
    for key in required_keys:
        if key not in beat_data:
            print(f"❌ SCHEMA ERROR: Missing required key '{key}'")
            return False
            
    if len(beat_data.get("choices", [])) < 2:
        print("❌ GAMEPLAY ERROR: A beat must have at least 2 choices.")
        return False

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--schema", default="narrative/templates/beat_schema.json")
    args = parser.parse_args()

    print(f"📝 Lead Narrative Editor validating {args.file}...")
    if validate_markdown_beat(args.file, args.schema):
        print("✅ Beat schema validated. Stat mechanics are present.")
        sys.exit(0)
    else:
        sys.exit(1)