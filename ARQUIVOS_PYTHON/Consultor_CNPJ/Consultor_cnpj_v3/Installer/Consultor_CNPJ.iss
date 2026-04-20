
[Setup]
AppName=Consultor de CNPJ
AppVersion=3.0
AppPublisher=SeuNome
DefaultDirName={autopf}\ConsultorCNPJ
DefaultGroupName=Consultor de CNPJ
OutputDir=Instalador
OutputBaseFilename=ConsultorCNPJ_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Files]
Source: "dist\Consultor_CNPJ.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Consultor de CNPJ"; Filename: "{app}\Consultor_CNPJ.exe"
Name: "{commondesktop}\Consultor de CNPJ"; Filename: "{app}\Consultor_CNPJ.exe"

[Run]
Filename: "{app}\Consultor_CNPJ.exe"; Description: "Abrir o Consultor de CNPJ"; Flags: nowait postinstall skipifsilent