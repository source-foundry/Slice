; -- Slice-Installer.iss --
; Creates a minimal Windows installer for the Slice application

;   Copyright (C) 2021 Christopher Simpkins
;
;   This program is free software: you can redistribute it and/or modify
;   it under the terms of the GNU General Public License as published by
;   the Free Software Foundation, either version 3 of the License, or
;   (at your option) any later version.
;
;   This program is distributed in the hope that it will be useful,
;   but WITHOUT ANY WARRANTY; without even the implied warranty of
;   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;   GNU General Public License for more details.
;
;   You should have received a copy of the GNU General Public License
;   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#define BUILDPATH "..\..\dist\Slice.exe"
#define SliceVersion "0.7.1"

[Setup]
AppName=Slice
AppVersion={#SliceVersion}
AppPublisher="Christopher Simpkins"
AppPublisherURL=https://github.com/source-foundry/Slice
AppReadmeFile=https://github.com/source-foundry/Slice/blob/main/README.md
AppSupportURL=https://github.com/source-foundry/Slice/issues
AppUpdatesURL=https://github.com/source-foundry/Slice/releases
AppCopyright="Copyright 2021 Christopher Simpkins. GPLv3 License"
WizardStyle=modern
DefaultDirName={autopf}\Slice
DisableProgramGroupPage=yes
SetupIconFile=..\..\icons\Icon.ico
UninstallDisplayIcon={app}\Slice.exe
Compression=lzma2
SolidCompression=yes
OutputBaseFilename=Slice-{#SliceVersion}-Installer
OutputDir=..\..\dist\Windows-Installer
LicenseFile=..\..\LICENSE

[Files]
Source: {#BUILDPATH}; DestDir: "{app}"

[Tasks]
Name: desktopicon; Description: "Create a &desktop icon"; GroupDescription: "Additional icons:"
Name: desktopicon\common; Description: "For all users"; GroupDescription: "Additional icons:"; Flags: exclusive
Name: desktopicon\user; Description: "For the current user only"; GroupDescription: "Additional icons:"; Flags: exclusive unchecked

[Icons]
Name: "{autoprograms}\Slice"; Filename: "{app}\Slice.exe"
Name: "{commondesktop}\Slice"; Filename: "{app}\Slice.exe"; Tasks: desktopicon