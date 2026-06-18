import UnityPy
import os
import shutil
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GAME_PATH = os.path.join(SCRIPT_DIR, "..", "Dust Front RTS_Data")
ASSETS_FILE = os.path.join(GAME_PATH, "resources.assets")
BACKUP_FILE = os.path.join(GAME_PATH, "resources.assets.bak")
PATCHED_FILE = os.path.join(GAME_PATH, "resources.assets.patched")
ORIG_FILE = os.path.join(GAME_PATH, "resources.assets.orig")

from translate import TRANSLATIONS


def patch():
    """生成汉化补丁"""
    if not os.path.exists(ASSETS_FILE):
        print(f"[ERROR] {ASSETS_FILE} not found")
        return False

    if not os.path.exists(BACKUP_FILE):
        print("Creating backup...")
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

        if obj.path_id not in (163, 165):
            continue

        print(f"\nProcessing TextAsset path_id={obj.path_id}...")

        if '\r\n' in text:
            lines = text.split('\r\n')
            line_ending = '\r\n'
        else:
            lines = text.split('\n')
            line_ending = '\n'

        new_lines = []
        translated = 0

        for line in lines:
            stripped = line.strip()

            if not stripped:
                new_lines.append(line)
                continue

            if stripped.startswith('Keys,'):
                new_lines.append(line + ',Chinese')
                continue

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

            if ',' in cn_text or '"' in cn_text or '\n' in cn_text:
                cn_text = '"' + cn_text.replace('"', '""') + '"'

            new_lines.append(line + ',' + cn_text)

        new_text = line_ending.join(new_lines)
        print(f"  Translated: {translated}, Size: {len(text)} -> {len(new_text)}")

        data.m_Script = new_text
        data.save()

    print(f"\nSaving to {PATCHED_FILE}...")
    with open(PATCHED_FILE, 'wb') as f:
        f.write(env.file.save())

    print("[OK] Patch generated")
    return True


def apply():
    """应用补丁：替换 resources.assets"""
    if not os.path.exists(PATCHED_FILE):
        print(f"[ERROR] {PATCHED_FILE} not found. Run 'patch' first.")
        return False

    if os.path.exists(ORIG_FILE):
        os.remove(ORIG_FILE)

    if os.path.exists(ASSETS_FILE):
        os.rename(ASSETS_FILE, ORIG_FILE)

    os.rename(PATCHED_FILE, ASSETS_FILE)
    print("[OK] Patch applied")
    return True


def restore():
    """恢复原版"""
    if not os.path.exists(ORIG_FILE):
        print(f"[ERROR] {ORIG_FILE} not found. No backup to restore.")
        return False

    if os.path.exists(ASSETS_FILE):
        os.remove(ASSETS_FILE)

    os.rename(ORIG_FILE, ASSETS_FILE)
    print("[OK] Original restored")
    return True


def status():
    """查看当前状态"""
    files = {
        "resources.assets": ASSETS_FILE,
        "resources.assets.bak": BACKUP_FILE,
        "resources.assets.orig": ORIG_FILE,
        "resources.assets.patched": PATCHED_FILE,
    }
    print("File status:")
    for name, path in files.items():
        exists = os.path.exists(path)
        size = os.path.getsize(path) if exists else 0
        status = f"{size:,} bytes" if exists else "not found"
        print(f"  {name}: {status}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py <command>")
        print("  patch   - Generate Chinese localization patch")
        print("  apply   - Apply patch (replace resources.assets)")
        print("  restore - Restore original files")
        print("  status  - Show current file status")
        return

    cmd = sys.argv[1].lower()
    if cmd == "patch":
        patch()
    elif cmd == "apply":
        apply()
    elif cmd == "restore":
        restore()
    elif cmd == "status":
        status()
    else:
        print(f"Unknown command: {cmd}")


if __name__ == '__main__':
    main()
