import sys
from cx_Freeze import setup, Executable

# Dependencies: Add any additional modules or packages your script requires
build_exe_options = {"packages": ["yaml", "googletrans", "jinja2", "PyQt5"], "excludes": []}

# Executable
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Use this option for GUI applications on Windows

setup(
    name="Trans",
    version="1.0",
    description="YML Tranlsation Tool",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
