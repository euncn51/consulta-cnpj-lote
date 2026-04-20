; Script de instalação para Consultor de CNPJ
; Criado com Inno Setup Compiler
; Executável: C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\dist\Consultor_CNPJ.exe

[Setup]
; Informações básicas
AppId={{F1A3B5C7-D8E9-F0A1-B2C3-D4E5F6A7B8C9}
AppName=Consultor de CNPJ
AppVersion=3.0.0
AppVerName=Consultor de CNPJ v3.0
AppPublisher=Seu Nome ou Empresa
AppPublisherURL=https://seusite.com
AppSupportURL=https://seusite.com/suporte
AppUpdatesURL=https://seusite.com/atualizacoes
DefaultDirName={autopf}\Consultor de CNPJ
DefaultGroupName=Consultor de CNPJ
AllowNoIcons=yes
LicenseFile=C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\LICENSE.txt
InfoBeforeFile=C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\README.txt
; UninstallDisplayName=Consultor de CNPJ
; UninstallDisplayIcon={app}\Consultor_CNPJ.exe
Compression=lzma2/ultra
SolidCompression=yes
OutputDir=C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\Instaladores
OutputBaseFilename=Consultor_CNPJ_Instalador
SetupIconFile=C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\icon.ico
WizardStyle=modern
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1
Name: "associatexlsx"; Description: "Associar arquivos .xlsx com o Consultor de CNPJ"; GroupDescription: "Associações de arquivo:"; Flags: unchecked
Name: "associatecsv"; Description: "Associar arquivos .csv com o Consultor de CNPJ"; GroupDescription: "Associações de arquivo:"; Flags: unchecked

[Files]
; Executável principal
Source: "C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\dist\Consultor_CNPJ.exe"; DestDir: "{app}"; Flags: ignoreversion
; Arquivos de exemplo (opcionais)
Source: "C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\exemplo_cnpjs.xlsx"; DestDir: "{app}\Exemplos"; Flags: ignoreversion; Tasks: ; Languages: 
Source: "C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\exemplo_cnpjs.csv"; DestDir: "{app}\Exemplos"; Flags: ignoreversion; Tasks: ; Languages: 
; Documentação
Source: "C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\CHANGELOG.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
; DLLs adicionais se necessário (geralmente não necessário para PyInstaller onefile)

; Se o executável precisar de DLLs do Visual C++ Redistributable
; Source: "vcredist_x86.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Icons]
Name: "{group}\Consultor de CNPJ"; Filename: "{app}\Consultor_CNPJ.exe"
Name: "{group}\{cm:UninstallProgram,Consultor de CNPJ}"; Filename: "{uninstallexe}"
Name: "{group}\Documentação"; Filename: "{app}\README.txt"
Name: "{group}\Exemplos"; Filename: "{app}\Exemplos"
Name: "{commondesktop}\Consultor de CNPJ"; Filename: "{app}\Consultor_CNPJ.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Consultor de CNPJ"; Filename: "{app}\Consultor_CNPJ.exe"; Tasks: quicklaunchicon

[Registry]
; Registrar associações de arquivo
Root: HKA; Subkey: "Software\Classes\.xlsx\OpenWithProgids"; ValueType: string; ValueName: "ConsultorCNPJ.xlsx"; ValueData: ""; Flags: uninsdeletevalue; Tasks: associatexlsx
Root: HKA; Subkey: "Software\Classes\ConsultorCNPJ.xlsx"; ValueType: string; ValueName: ""; ValueData: "Planilha Excel"; Flags: uninsdeletekey; Tasks: associatexlsx
Root: HKA; Subkey: "Software\Classes\ConsultorCNPJ.xlsx\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Consultor_CNPJ.exe,0"; Tasks: associatexlsx
Root: HKA; Subkey: "Software\Classes\ConsultorCNPJ.xlsx\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Consultor_CNPJ.exe"" ""%1"""; Tasks: associatexlsx

Root: HKA; Subkey: "Software\Classes\.csv\OpenWithProgids"; ValueType: string; ValueName: "ConsultorCNPJ.csv"; ValueData: ""; Flags: uninsdeletevalue; Tasks: associatecsv
Root: HKA; Subkey: "Software\Classes\ConsultorCNPJ.csv"; ValueType: string; ValueName: ""; ValueData: "Arquivo CSV"; Flags: uninsdeletekey; Tasks: associatecsv
Root: HKA; Subkey: "Software\Classes\ConsultorCNPJ.csv\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\Consultor_CNPJ.exe,0"; Tasks: associatecsv
Root: HKA; Subkey: "Software\Classes\ConsultorCNPJ.csv\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\Consultor_CNPJ.exe"" ""%1"""; Tasks: associatecsv

[Run]
; Executar o programa após instalação
Filename: "{app}\Consultor_CNPJ.exe"; Description: "{cm:LaunchProgram,Consultor de CNPJ}"; Flags: nowait postinstall skipifsilent
; Instalar Visual C++ Redistributable se necessário
; Filename: "{tmp}\vcredist_x86.exe"; Parameters: "/quiet /norestart"; StatusMsg: "Instalando Visual C++ Redistributable..."; Check: VCRedistNeedsInstall

[UninstallDelete]
; Limpar arquivos gerados pelo programa (opcional)
Type: files; Name: "{app}\cnpj_cache.json"
Type: files; Name: "{app}\log_cnpj.txt"
Type: files; Name: "{app}\*.log"
Type: dirifempty; Name: "{app}\Exemplos"
Type: dirifempty; Name: "{app}"

[Code]
// Função para verificar se Visual C++ Redistributable está instalado (opcional)
function VCRedistNeedsInstall: Boolean;
var 
  Version: String;
begin
  if RegQueryStringValue(HKEY_LOCAL_MACHINE,
    'SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x86', 
    'Version', Version) then
  begin
    // Verifica se a versão instalada é suficiente
    Result := (CompareStr(Version, '14.30.30704') < 0);
  end
  else 
  begin
    Result := True;
  end;
end;

// Procedimento para inicialização
procedure InitializeWizard;
begin
  // Código de inicialização personalizado (opcional)
end;

// Procedimento para finalização
procedure DeinitializeSetup;
begin
  // Código de limpeza (opcional)
end;