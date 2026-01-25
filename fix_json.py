import json

# Fix instrument_specs.json trailing comma
path = 'data/instrument_specs.json'
try:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the likely trailing comma at line 611 (before line 612 ] )
    # Error was: Illegal trailing comma before end of object: line 612 column 10
    # Actually, char 20584 is exactly near the end.
    
    # Trying to load it with a more tolerant parser or just fixing common trailing commas
    import re
    # Remove trailing commas before ] or }
    fixed_content = re.sub(r',\s*([\]}])', r'\1', content)
    
    data = json.loads(fixed_content)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("✅ Fixed instrument_specs.json")
except Exception as e:
    print(f"❌ Failed to fix instrument_specs.json: {e}")
