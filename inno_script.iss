; Inno Setup Script to install Python application, Ghostscript, and set PATH

[Setup]
AppName=TIF PDF Generator
AppVersion=0.05 Alpha
DefaultDirName={commonpf}\TIFPDFGenerator
DefaultGroupName=TIF PDF Generator
OutputDir=executable
OutputBaseFilename=tif_pdf_Generator_0.05
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin

[Files]
; Add your PyInstaller executable
Source: "dist\Pdf_generator.exe"; DestDir: "{app}"; Flags: ignoreversion

; Include Ghostscript installer (download from https://www.ghostscript.com/download/gsdnld.html)
Source: "gs\gs10040w64.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{group}\TIFF PDF Generator"; Filename: "{app}\Pdf_generator.exe"
Name: "{group}\Uninstall TIF PDF Generator"; Filename: "{uninstallexe}"

[Run]
; Run Ghostscript installer silently
Filename: "{tmp}\gs10040w64.exe"; Parameters: "/S"; StatusMsg: "Installing Ghostscript..."

; Add Ghostscript to PATH
Filename: "{cmd}"; Parameters: "/C setx /M PATH ""%PATH%;{commonpf}\gs\gs10.04.0\bin"""

; Run the main application after installation
Filename: "{app}\Pdf_generator.exe"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Remove Ghostscript from PATH during uninstall
Filename: "{cmd}"; Parameters: "/C setx /M PATH ""%PATH:C:\Program Files\gs\gs10.04.0\bin;=%"""

