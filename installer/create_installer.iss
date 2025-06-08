; Hand Gesture Control - Inno Setup Script
; This script creates a Windows installer for the Hand Gesture Control application

[Setup]
AppName=Hand Gesture Control
AppVersion=1.0
AppPublisher=Hand Gesture Development Team
AppPublisherURL=https://github.com/yourusername/hand-gesture-control
AppSupportURL=https://github.com/yourusername/hand-gesture-control
AppUpdatesURL=https://github.com/yourusername/hand-gesture-control
DefaultDirName={autopf}\Hand Gesture Control
DefaultGroupName=Hand Gesture Control
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=output
OutputBaseFilename=HandGestureControl_Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startmenu"; Description: "Create Start Menu shortcut"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkable checked
Name: "startup"; Description: "Start with Windows (runs in background)"; GroupDescription: "Startup Options"; Flags: unchecked

[Files]
Source: "HandGestureControl.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LATEST_UPDATES.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "start_normal.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "start_headless.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "start_silent.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "start_tray.bat"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Hand Gesture Control"; Filename: "{app}\HandGestureControl.exe"
Name: "{group}\Hand Gesture Control (Headless)"; Filename: "{app}\start_headless.bat"
Name: "{group}\Hand Gesture Control (Silent)"; Filename: "{app}\start_silent.bat"
Name: "{group}\Hand Gesture Control (System Tray)"; Filename: "{app}\start_tray.bat"
Name: "{group}\{cm:UninstallProgram,Hand Gesture Control}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Hand Gesture Control"; Filename: "{app}\HandGestureControl.exe"; Tasks: desktopicon

[Registry]
; Add to Windows startup if selected (using system tray mode)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "HandGestureControl"; ValueData: """{app}\start_tray.bat"""; Tasks: startup

[Run]
Filename: "{app}\HandGestureControl.exe"; Description: "{cm:LaunchProgram,Hand Gesture Control}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "taskkill"; Parameters: "/f /im HandGestureControl.exe"; Flags: runhidden

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
  begin
    // Create batch files
    SaveStringToFile(ExpandConstant('{app}\start_normal.bat'), 
      '@echo off' + #13#10 +
      'cd /d "%~dp0"' + #13#10 +
      'HandGestureControl.exe' + #13#10 +
      'pause', False);
      
    SaveStringToFile(ExpandConstant('{app}\start_headless.bat'), 
      '@echo off' + #13#10 +
      'cd /d "%~dp0"' + #13#10 +
      'HandGestureControl.exe --headless' + #13#10, False);
      
    SaveStringToFile(ExpandConstant('{app}\start_silent.bat'), 
      '@echo off' + #13#10 +
      'cd /d "%~dp0"' + #13#10 +
      'HandGestureControl.exe --headless --silent' + #13#10, False);
      
    SaveStringToFile(ExpandConstant('{app}\start_tray.bat'), 
      '@echo off' + #13#10 +
      'cd /d "%~dp0"' + #13#10 +
      'HandGestureControl.exe --tray --silent' + #13#10, False);
  end;
end;
