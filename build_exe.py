import PyInstaller.__main__
import os
import shutil

# Make sure we are in the right directory
base_dir = os.path.abspath(os.path.dirname(__file__))

print("Cleaning build folders...")
shutil.rmtree(os.path.join(base_dir, 'build'), ignore_errors=True)
shutil.rmtree(os.path.join(base_dir, 'dist'), ignore_errors=True)

# Check for icon
icon_path = 'app.ico'
if os.path.exists(icon_path):
    print(f"Using icon: {icon_path}")
    icon_option = f'--icon={icon_path}'
else:
    print("No app.ico found. Using default icon.")
    icon_option = '--icon=NONE'

print("Starting Build...")
PyInstaller.__main__.run([
    'main.py',
    '--name=AccountBook',
    '--onefile',
    '--noconsole',  # Hide terminal
    '--add-data=templates;templates',
    '--add-data=static;static',
    icon_option,
    '--clean'
])

print("Build Complete. Executable is in 'dist' folder.")
