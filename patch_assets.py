import UnityPy
import os
import shutil

GAME_PATH = r"D:\SteamLibrary\steamapps\common\Dust Front RTS Demo\Dust Front RTS_Data"
OUTPUT_DIR = r"D:\SteamLibrary\steamapps\common\Dust Front RTS Demo\localization-tool\output"
ASSETS_FILE = os.path.join(GAME_PATH, "resources.assets")
BACKUP_FILE = os.path.join(GAME_PATH, "resources.assets.bak")

from translate import TRANSLATIONS

def patch_assets():
    if not os.path.exists(BACKUP_FILE):
        print(f"Backing up original...")
        shutil.copy2(ASSETS_FILE, BACKUP_FILE)

    print(f"Loading {ASSETS_FILE}...")
    env = UnityPy.load(ASSETS_FILE)

    for obj in env.objects:
        if obj.type.name != "TextAsset":
            continue
        
        data = obj.read()
        text = str(getattr(data, 'm_Script', ''))
        if not text or len(text) < 100:
            continue
        
        # Only patch path_id=163 (the ORIGINAL with Keys,Russian,English)
        if obj.path_id != 163:
            continue
        
        print(f"\nProcessing TextAsset path_id={obj.path_id}...")
        
        # The original uses \r\n line endings
        lines = text.split('\r\n')
        print(f"  Lines: {len(lines)}")
        print(f"  First line: {repr(lines[0])}")
        
        # Add Chinese column to header
        new_lines = []
        translated = 0
        
        for line in lines:
            stripped = line.strip()
            
            # Empty line - keep as-is
            if not stripped:
                new_lines.append(line)
                continue
            
            # Header line
            if stripped.startswith('Keys,'):
                new_lines.append(line + ',Chinese')
                continue
            
            # Data line
            comma_pos = line.find(',')
            if comma_pos == -1:
                new_lines.append(line)
                continue
            
            key = line[:comma_pos].strip()
            if not key:
                new_lines.append(line)
                continue
            
            cn_text = TRANSLATIONS.get(key, '')
            if cn_text:
                translated += 1
            
            # Escape for CSV
            if ',' in cn_text or '"' in cn_text or '\n' in cn_text:
                cn_text = '"' + cn_text.replace('"', '""') + '"'
            
            new_lines.append(line + ',' + cn_text)
        
        new_text = '\r\n'.join(new_lines)
        print(f"  Translated: {translated}")
        print(f"  Size: {len(text)} -> {len(new_text)}")
        print(f"  Header: {new_lines[0]}")
        
        # Write back
        data.m_Script = new_text
        data.save()
        print(f"  Patched!")

    # Save
    patched_file = os.path.join(GAME_PATH, "resources.assets.patched")
    print(f"\nSaving to {patched_file}...")
    with open(patched_file, 'wb') as f:
        f.write(env.file.save())

    print(f"\n{'='*60}")
    print(f"DONE!")
    print(f"{'='*60}")

if __name__ == '__main__':
    patch_assets()
