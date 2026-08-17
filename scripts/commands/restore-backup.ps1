param(
    [Parameter(Mandatory=$true)][string]$Backup,
    [switch]$CurrentPaths
)
$ErrorActionPreference="Stop"
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
. (Join-Path $Root "scripts\BackupLib.ps1")
Ensure-BackupRoot

if($Backup -eq "latest"){
    $d=Get-ChildItem -Directory $BackupRoot|Sort-Object Name|Select-Object -Last 1
    if(-not $d){throw "No backups found"}
    $Backup=$d.Name
}elseif($Backup -notmatch '^[0-9]{8}-[0-9]{6}(-[0-9]+)?$'){
    throw "Invalid backup name: $Backup"
}
$src=Join-Path $BackupRoot $Backup
$manifestPath=Join-Path $src "manifest.json"
if(-not(Test-Path $manifestPath)){throw "Invalid backup: $src"}

$current=New-AgentPackSnapshot "pre-restore-$Backup"
Write-Host "Current managed state snapshotted: $current"

if($CurrentPaths){
    $CodexHome=if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $HOME ".codex"}
    $ClaudeHome=if($env:CLAUDE_CONFIG_DIR){$env:CLAUDE_CONFIG_DIR}else{Join-Path $HOME ".claude"}
    $CodexSkills=if($env:AI_AGENT_PACK_CODEX_SKILLS_HOME){$env:AI_AGENT_PACK_CODEX_SKILLS_HOME}else{Join-Path $HOME ".agents\skills"}
}else{
    $m=Get-Content $manifestPath -Raw|ConvertFrom-Json
    $CodexHome=if($m.codexHome){$m.codexHome}else{Join-Path $HOME ".codex"}
    $ClaudeHome=if($m.claudeHome){$m.claudeHome}else{Join-Path $HOME ".claude"}
    $CodexSkills=if($m.codexSkillsHome){$m.codexSkillsHome}else{Join-Path $HOME ".agents\skills"}
}
$StateFile=if($env:AI_AGENT_PACK_STATE_FILE){$env:AI_AGENT_PACK_STATE_FILE}else{Join-Path $HOME ".ai-agent-pack-state.json"}

New-Item -ItemType Directory -Force -Path $CodexHome,$ClaudeHome,(Split-Path -Parent $CodexSkills)|Out-Null
Remove-Item -Force (Join-Path $CodexHome "AGENTS.md"),(Join-Path $ClaudeHome "CLAUDE.md"),$StateFile -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force (Join-Path $CodexHome "agents"),$CodexSkills,(Join-Path $ClaudeHome "agents"),(Join-Path $ClaudeHome "skills") -ErrorAction SilentlyContinue

if(Test-Path (Join-Path $src "codex\AGENTS.md")){Copy-Item -Force (Join-Path $src "codex\AGENTS.md") (Join-Path $CodexHome "AGENTS.md")}
if(Test-Path (Join-Path $src "codex\agents")){Copy-Item -Recurse -Force (Join-Path $src "codex\agents") (Join-Path $CodexHome "agents")}
if(Test-Path (Join-Path $src "codex\skills")){Copy-Item -Recurse -Force (Join-Path $src "codex\skills") $CodexSkills}
if(Test-Path (Join-Path $src "claude\CLAUDE.md")){Copy-Item -Force (Join-Path $src "claude\CLAUDE.md") (Join-Path $ClaudeHome "CLAUDE.md")}
if(Test-Path (Join-Path $src "claude\agents")){Copy-Item -Recurse -Force (Join-Path $src "claude\agents") (Join-Path $ClaudeHome "agents")}
if(Test-Path (Join-Path $src "claude\skills")){Copy-Item -Recurse -Force (Join-Path $src "claude\skills") (Join-Path $ClaudeHome "skills")}
if(Test-Path (Join-Path $src "state\install-state.json")){Copy-Item -Force (Join-Path $src "state\install-state.json") $StateFile}

Write-Host "Restore complete: $Backup"
Write-Host "Codex path: $CodexHome"
Write-Host "Claude path: $ClaudeHome"
