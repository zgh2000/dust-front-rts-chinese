import UnityPy
import os
import csv
import io
import shutil

GAME_PATH = r"D:\SteamLibrary\steamapps\common\Dust Front RTS Demo\Dust Front RTS_Data"
OUTPUT_DIR = r"D:\SteamLibrary\steamapps\common\Dust Front RTS Demo\localization-tool\output"
ASSETS_FILE = os.path.join(GAME_PATH, "resources.assets")
BACKUP_FILE = os.path.join(GAME_PATH, "resources.assets.bak")
PATCHED_FILE = os.path.join(GAME_PATH, "resources.assets.patched")

def patch_assets():
    # Step 1: Backup original
    if not os.path.exists(BACKUP_FILE):
        print(f"Backing up original to {BACKUP_FILE}")
        shutil.copy2(ASSETS_FILE, BACKUP_FILE)
    else:
        print(f"Backup already exists: {BACKUP_FILE}")

    # Step 2: Load environment
    print(f"Loading {ASSETS_FILE}...")
    env = UnityPy.load(ASSETS_FILE)

    # Step 3: Process each object
    patched_count = 0
    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        
        data = obj.read()
        text = getattr(data, 'm_Script', '')
        if not text or len(str(text)) < 100:
            continue
        
        text_str = str(text)
        
        # Check if this is a localization CSV
        if 'Keys,Russian,English' not in text_str[:50]:
            continue
        
        print(f"\nProcessing TextAsset path_id={obj.path_id}...")
        
        # Determine which file to use for replacement
        if obj.path_id == 164:
            cn_file = os.path.join(OUTPUT_DIR, 'textasset_164_cn.csv')
        elif obj.path_id == 165:
            cn_file = os.path.join(OUTPUT_DIR, 'textasset_165_cn.csv')
        else:
            print(f"  Unknown path_id {obj.path_id}, skipping")
            continue
        
        # Read the translated CSV
        with open(cn_file, 'r', encoding='utf-8-sig') as f:
            new_text = f.read()
        
        print(f"  Original length: {len(text_str)}")
        print(f"  New length: {len(new_text)}")
        
        # Write back the modified TextAsset
        data.m_Script = new_text
        data.save()
        patched_count += 1
        print(f"  Patched!")

    # Step 4: Save the modified asset file
    print(f"\nSaving patched assets to {PATCHED_FILE}...")
    with open(PATCHED_FILE, 'wb') as f:
        f.write(env.file.save())

    print(f"\n{'='*60}")
    print(f"DONE! Patched {patched_count} TextAssets")
    print(f"Original backup: {BACKUP_FILE}")
    print(f"Patched file: {PATCHED_FILE}")
    print(f"{'='*60}")
    print(f"\nTo apply the patch:")
    print(f"  1. Close the game")
    print(f'  2. Rename "{ASSETS_FILE}" to "{ASSETS_FILE}.orig"')
    print(f'  3. Rename "{PATCHED_FILE}" to "{os.path.basename(ASSETS_FILE)}"')
    print(f"  4. Launch the game and select English language")
    print(f"\nTo restore original:")
    print(f'  1. Delete "{os.path.basename(ASSETS_FILE)}"')
    print(f'  2. Rename "{BACKUP_FILE}" to "{os.path.basename(ASSETS_FILE)}"')

if __name__ == '__main__':
    patch_assets()
