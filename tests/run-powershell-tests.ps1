$ErrorActionPreference="Stop"
$Root=Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)

$files=@(
  "scripts\commands\install-all.ps1","scripts\commands\install-codex.ps1","scripts\commands\install-claude.ps1","scripts\commands\install-project.ps1",
  "scripts\commands\uninstall.ps1","scripts\commands\uninstall-project.ps1","scripts\commands\restore-backup.ps1"
)
foreach($f in $files){
  $tokens=$null
  $errors=$null
  $null=[System.Management.Automation.Language.Parser]::ParseFile(
    (Join-Path $Root $f),[ref]$tokens,[ref]$errors
  )
  if($errors){throw "PowerShell parse errors in $f"}
}

$TestHome=Join-Path ([System.IO.Path]::GetTempPath()) ("weap-"+[guid]::NewGuid())
New-Item -ItemType Directory -Force -Path $TestHome|Out-Null
try{
  $env:HOME=$TestHome
  $env:USERPROFILE=$TestHome
  $env:CODEX_HOME=Join-Path $TestHome ".codex"
  $env:CLAUDE_CONFIG_DIR=Join-Path $TestHome ".claude"
  $env:AI_AGENT_PACK_CODEX_SKILLS_HOME=Join-Path $TestHome ".agents\skills"
  $env:AI_AGENT_PACK_BACKUP_ROOT=Join-Path $TestHome ".ai-agent-pack-backups"
  $env:AI_AGENT_PACK_STATE_FILE=Join-Path $TestHome ".ai-agent-pack-state.json"
  New-Item -ItemType Directory -Force -Path (Join-Path $TestHome ".codex"),(Join-Path $TestHome ".claude")|Out-Null
  "keep=true"|Set-Content (Join-Path $TestHome ".codex\config.toml")
  '{"keep":true}'|Set-Content (Join-Path $TestHome ".claude\settings.json")

  & (Join-Path $Root "scripts\commands\install-all.ps1") -Profile core
  if(-not(Test-Path (Join-Path $TestHome ".codex\AGENTS.md"))){throw "Codex install missing"}
  if(-not(Test-Path (Join-Path $TestHome ".claude\CLAUDE.md"))){throw "Claude install missing"}
  & (Join-Path $Root "scripts\commands\uninstall.ps1") -KeepThirdParty
  if(Test-Path (Join-Path $TestHome ".codex\AGENTS.md")){throw "Codex uninstall failed"}
} finally {
  Remove-Item -Recurse -Force $TestHome -ErrorAction SilentlyContinue
}
Write-Host "PowerShell lifecycle tests OK."
