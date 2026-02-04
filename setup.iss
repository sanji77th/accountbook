; Inno Setup Script for AccountBook
; Requires Inno Setup to compile: https://jrsoftware.org/isdl.php

[Setup]
AppId={{8B43F241-1234-4567-89AB-CDEF12345678}
AppName=AccountBook
AppVersion=1.0
AppPublisher=Vibe Coding
DefaultDirName={autopf}\AccountBook
DisableDirPage=no
DisableProgramGroupPage=no
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=lowest
OutputDir=Output
OutputBaseFilename=AccountBook_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
; Icon for the installer file itself
SetupIconFile=app.ico

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; IMPORTANT: Run 'python build_exe.py' first to generate this file
Source: "dist\AccountBook.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\AccountBook"; Filename: "{app}\AccountBook.exe"; IconFilename: "{app}\AccountBook.exe"
Name: "{autodesktop}\AccountBook"; Filename: "{app}\AccountBook.exe"; Tasks: desktopicon; IconFilename: "{app}\AccountBook.exe"

[Run]
Filename: "{app}\AccountBook.exe"; Description: "{cm:LaunchProgram,AccountBook}"; Flags: nowait postinstall skipifsilent
