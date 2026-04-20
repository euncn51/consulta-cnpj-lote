; Script para Inno Setup - Consultor de CNPJ
[Setup]
AppName=Consultor de CNPJ
AppVersion=1.0
AppPublisher=SeuNome
DefaultDirName={autopf}\ConsultorCNPJ
DefaultGroupName=Consultor de CNPJ
OutputDir=output_installer
OutputBaseFilename=ConsultorCNPJ_Setup
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\dist\Consultor_CNPJ.exe"; DestDir: "{app}"; Flags: ignoreversion
; Adicione outros arquivos se necessário (ex.: README, templates)
; Source: "README.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Consultor de CNPJ"; Filename: "{app}\Consultor_CNPJ.exe"
Name: "{commondesktop}\Consultor de CNPJ"; Filename: "{app}\Consultor_CNPJ.exe"

[Run]
Filename: "{app}\Consultor_CNPJ.exe"; Description: "Abrir o Consultor de CNPJ"; Flags: nowait postinstall skipifsilent