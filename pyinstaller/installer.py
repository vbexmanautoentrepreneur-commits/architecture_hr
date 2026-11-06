import os
import platform
import shutil
import subprocess
from pathlib import Path

APP_NAME = "HRManager"

ICON_PATH = Path("assets/icons/hr.ico")
MAIN_FILE = "../main.py"
DEBUG = False
def clean():
    for folder in ("build", "dist"):
        path = Path(folder)
        if path.exists():
            shutil.rmtree(path)
    for spec in Path("..").glob("*.spec"):
        spec.unlink()

def get_add_data():
    separator = ";" if platform.system() == "Windows" else ":"
    data = []
    if Path("assets").exists():
        data.extend(["--add-data", f"assets{separator}assets"])
    # if Path("employees.db").exists():
    #     data.extend(["--add-data", f"employees.db{separator}."])
    return data

def build():
    cmd = ["pyinstaller", "--clean", "--onefile", "--name", APP_NAME,"--distpath", "release","--add-data", "../icons;icons"]
    if DEBUG:
        cmd.extend(["--console", "--debug=all"])
    else:
        cmd.append("--windowed")
    if ICON_PATH.exists():
        cmd.extend(["--icon", str(ICON_PATH)])
    cmd.extend(get_add_data())
    cmd.append(MAIN_FILE)
    print("\nCommand:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    # Suppression du dossier build
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)

def main():
    print(f"OS       : {platform.system()}")
    print(f"Python   : {platform.python_version()}")
    clean()
    build()
    exe_name = f"{APP_NAME}.exe" if platform.system() == "Windows" else APP_NAME
    print("\n" + "=" * 50)
    print("BUILD SUCCESS")
    print(f"Output : dist/{exe_name}")
    print("=" * 50)

if __name__ == "__main__":
    main()