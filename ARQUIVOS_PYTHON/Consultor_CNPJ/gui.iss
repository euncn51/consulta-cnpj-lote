; Script para Inno Setup - Installer do Consultor CNPJ
[Setup]
AppName=Consultor de CNPJ
AppVersion=1.0
DefaultDirName={autopf}\ConsultorCNPJ
DefaultGroupName=Consultor de CNPJ
OutputDir=output_installer
OutputBaseFilename=ConsultorCNPJ_Setup
Compression=lzma
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "dist\gui.exe"; DestDir: "{app}"; Flags: ignoreversion
; Adicione outros arquivos (como ícones ou README) se necessário:
; Source: "icone.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\Consultor de CNPJ"; Filename: "{app}\gui.exe"
Name: "{commondesktop}\Consultor de CNPJ"; Filename: "{app}\gui.exe"

[Run]
Filename: "{app}\gui.exe"; Description: "Abrir Consultor de CNPJ"; Flags: nowait postinstall skipifsilent