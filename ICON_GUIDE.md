# How to Add a Custom Icon

To change the icon of your application and installer:

1.  **Get an `.ico` file**:
    - Convert your logo to `.ico` format (needs to be square, typically 256x256).
    - You can use online converters like [ConvertICO](https://convertico.com/).

2.  **Name it `app.ico`**:
    - Rename your file to `app.ico`.

3.  **Place it in the Project Folder**:
    - Move `app.ico` to: `c:\Ongoing Projects\2026\Projects\Vibe Coding\Accounting App\` (the same folder as `main.py`).

4.  **Rebuild**:
    - Run the build script again:
      ```bash
      python build_exe.py
      ```
    - The script will automatically detect `app.ico` and use it for the EXE.

5.  **Installer Icon (Optional)**:
    - Open `setup.iss` in Inno Setup.
    - Uncomment the line `; SetupIconFile=app.ico` (remove the semicolon `;`).
    - Compiling will now use your icon for the setup file too.
