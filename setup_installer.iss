#define MyAppName "Sistema de Gestión de Reportes"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "HITSS"
#define MyAppURL "https://example.com"
#define MyAppExeName "SistemaReportes.exe"
#define SourcePath "dist\SistemaReportes"

[Setup]
AppId={{3F7F42B8-4D9F-4B5C-8A3E-2F8C1D0E9B4A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputBaseFilename=SistemaReportes_Instalador
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
Uninstallable=yes
UninstallDisplayIcon={{app}}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: {{en:Create a &desktop shortcut,es:Crear un acceso directo en el &escritorio}}; GroupDescription: "{{en:Additional tasks,es:Tareas adicionales}}:"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{en:Create a &Quick Launch shortcut,es:Crear un acceso rápido}}"; GroupDescription: "{{en:Additional tasks,es:Tareas adicionales}}:"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "{#SourcePath}\{#MyAppExeName}"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "{#SourcePath}\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\{#MyAppName}"; Filename: "{{app}}\{#MyAppExeName}"; WorkingDir: "{{app}}"
Name: "{{group}}\{{cm:UninstallProgram,{#MyAppName}}}"; Filename: "{{uninstallexe}}"
Name: "{{commondesktop}}\{#MyAppName}"; Filename: "{{app}}\{#MyAppExeName}}"; WorkingDir: "{{app}}"; Tasks: desktopicon
Name: "{{userappdata}}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{{app}}\{#MyAppExeName}}"; WorkingDir: "{{app}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\{#MyAppExeName}"; Flags: nowait postinstall skipifsilent; Description: "{{en:Launch the application,es:Iniciar la aplicación}}"

[UninstallDelete]
Type: dirifempty; Name: "{{app}}"
Type: dirifempty; Name: "{{app}}\app"
