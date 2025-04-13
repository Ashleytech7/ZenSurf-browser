import os
import sys
import subprocess
import shutil

def build_application():
    print("Building ZenSurf...")
    
    # Clean previous build
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Build the executable
    pyinstaller_cmd = [
        "pyinstaller",
        "--name=ZenSurf",
        "--windowed",
        "--onefile",
        "--icon=browser_icon.png",
        "--add-data=version.json;.",
        "--add-data=browser_icon.png;.",
        "main.py"
    ]
    
    try:
        subprocess.run(pyinstaller_cmd, check=True)
        print("\nBuild successful!")
        print("Executable created at: dist/ZenSurf.exe")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_application() 