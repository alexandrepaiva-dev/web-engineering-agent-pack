param([switch]$DryRun,[switch]$KeepThirdParty,[switch]$RestorePrevious,[switch]$ForceLegacy)
$ErrorActionPreference="Stop"
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
. (Join-Path $Root "scripts\BackupLib.ps1")
. (Join-Path $Root "scripts\StateLib.ps1")

if((-not(Test-Path $StateFile)) -and (-not $ForceLegacy)){
    throw "No v8 install-state file found at $StateFile. Refusing automatic uninstall. For v7-or-earlier use -ForceLegacy after reviewing -DryRun."
}

$CodexHome=if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $HOME ".codex"}
$ClaudeHome=if($env:CLAUDE_CONFIG_DIR){$env:CLAUDE_CONFIG_DIR}else{Join-Path $HOME ".claude"}
$CodexSkills=if($env:AI_AGENT_PACK_CODEX_SKILLS_HOME){$env:AI_AGENT_PACK_CODEX_SKILLS_HOME}else{Join-Path $HOME ".agents\skills"}
$ClaudeSkills=Join-Path $ClaudeHome "skills"
$FirstParty=(Get-ChildItem -Directory (Join-Path $Root "shared\skills")).Name
$CodexAgents=(Get-ChildItem -File (Join-Path $Root "codex\global\.codex\agents") -Filter "*.toml").Name
$ClaudeAgents=(Get-ChildItem -File (Join-Path $Root "claude\global\.claude\agents") -Filter "*.md").Name
$ThirdParty=@("ui-ux-pro-max","web-quality-audit")

$Target="both"
if(Test-Path $StateFile){
    try{$Target=(Get-Content $StateFile -Raw|ConvertFrom-Json).target}catch{$Target="both"}
}
$RemoveCodex=($Target -eq "both" -or $Target -eq "codex")
$RemoveClaude=($Target -eq "both" -or $Target -eq "claude")

if($DryRun){
    Write-Host "Global uninstall preview"
    Write-Host "Detected install target: $Target"
    Write-Host "Will snapshot current managed state first."
    if($RemoveCodex){Write-Host "Codex: remove pack AGENTS.md, known pack agents, and known first-party skills."}
    if($RemoveClaude){Write-Host "Claude: remove pack CLAUDE.md, known pack agents, and known first-party skills."}
    if($KeepThirdParty){Write-Host "Recommended third-party skills are preserved."}else{Write-Host "Recommended third-party skills are also removed."}
    Write-Host "Unknown/custom skills and agents are preserved."
    if($RestorePrevious){Write-Host "Newest prior install snapshot will be restored afterward."}
    exit 0
}

$current=New-AgentPackSnapshot "pre-uninstall"
Write-Host "Current managed state snapshotted: $current"

if($RemoveCodex){
    Remove-Item -Force (Join-Path $CodexHome "AGENTS.md") -ErrorAction SilentlyContinue
    foreach($a in $CodexAgents){Remove-Item -Force (Join-Path $CodexHome "agents\$a") -ErrorAction SilentlyContinue}
    foreach($s in $FirstParty){Remove-Item -Recurse -Force (Join-Path $CodexSkills $s) -ErrorAction SilentlyContinue}
    if(-not $KeepThirdParty){foreach($s in $ThirdParty){Remove-Item -Recurse -Force (Join-Path $CodexSkills $s) -ErrorAction SilentlyContinue}}
}
if($RemoveClaude){
    Remove-Item -Force (Join-Path $ClaudeHome "CLAUDE.md") -ErrorAction SilentlyContinue
    foreach($a in $ClaudeAgents){Remove-Item -Force (Join-Path $ClaudeHome "agents\$a") -ErrorAction SilentlyContinue}
    foreach($s in $FirstParty){Remove-Item -Recurse -Force (Join-Path $ClaudeSkills $s) -ErrorAction SilentlyContinue}
    if(-not $KeepThirdParty){foreach($s in $ThirdParty){Remove-Item -Recurse -Force (Join-Path $ClaudeSkills $s) -ErrorAction SilentlyContinue}}
}
Remove-Item -Force $StateFile -ErrorAction SilentlyContinue
Write-Host "Global pack-managed installation removed."

if($RestorePrevious){
    Ensure-BackupRoot
    $candidate=$null
    foreach($d in (Get-ChildItem -Directory $BackupRoot|Sort-Object Name -Descending)){
        if($d.FullName -eq $current){continue}
        $m=Join-Path $d.FullName "manifest.json";if(-not(Test-Path $m)){continue}
        try{$j=Get-Content $m -Raw|ConvertFrom-Json}catch{continue}
        if($j.reason -like "install-all*" -or $j.reason -like "codex-install*" -or $j.reason -like "claude-install*"){$candidate=$d.Name;break}
    }
    if(-not $candidate){throw "No prior install snapshot found."}
    & (Join-Path $Root "scripts\commands\restore-backup.ps1") $candidate
}
