param([string]$Profile,[switch]$DryRun,[switch]$SkipSnapshot,[string[]]$AddSkill=@(),[string[]]$RemoveSkill=@())
$ErrorActionPreference="Stop"
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
. (Join-Path $Root "scripts\BackupLib.ps1")
. (Join-Path $Root "scripts\StateLib.ps1")
. (Join-Path $Root "scripts\TransactionLib.ps1")
$Python=if(Get-Command python -ErrorAction SilentlyContinue){"python"}elseif(Get-Command py -ErrorAction SilentlyContinue){"py"}else{throw "Python required"}

if(-not $Profile){$Profile="core"}
$args=@((Join-Path $Root "scripts\profile_manager.py"),"resolve","--profile",$Profile)
foreach($s in $AddSkill){$args+=@("--add-skill",$s)}
foreach($s in $RemoveSkill){$args+=@("--remove-skill",$s)}
$Skills=@(& $Python @args)
if($LASTEXITCODE -ne 0){throw "Profile resolution failed"}

$CodexHome=if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $HOME ".codex"}
$SkillsHome=if($env:AI_AGENT_PACK_CODEX_SKILLS_HOME){$env:AI_AGENT_PACK_CODEX_SKILLS_HOME}else{Join-Path $HOME ".agents\skills"}
if($DryRun){Write-Host "Codex transactional install: $Profile ($($Skills.Count) skills)";Write-Host "Preserve: $CodexHome\config.toml";exit 0}
if(-not $SkipSnapshot){$b=New-AgentPackSnapshot "codex-install:$Profile";Write-Host "Snapshot: $b"}

New-Item -ItemType Directory -Force -Path $CodexHome,(Split-Path -Parent $SkillsHome)|Out-Null
$StageSkills=Join-Path (Split-Path -Parent $SkillsHome) ".weap-skills-stage-$PID"
$StageAgents=Join-Path $CodexHome ".weap-agents-stage-$PID"
$StageMd=Join-Path $CodexHome ".weap-AGENTS-stage-$PID.md"
Remove-Item -Recurse -Force $StageSkills,$StageAgents -ErrorAction SilentlyContinue
Remove-Item -Force $StageMd -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $StageSkills,$StageAgents|Out-Null
Copy-Item -Force (Join-Path $Root "codex\global\.codex\AGENTS.md") $StageMd
Copy-Item -Recurse -Force (Join-Path $Root "codex\global\.codex\agents\*") $StageAgents
foreach($s in $Skills){Copy-Item -Recurse -Force (Join-Path $Root "shared\skills\$s") (Join-Path $StageSkills $s)}
Test-SkillStage $StageSkills $Skills.Count
Replace-DirectoryTransactionally $StageAgents (Join-Path $CodexHome "agents")
Replace-DirectoryTransactionally $StageSkills $SkillsHome
Replace-FileTransactionally $StageMd (Join-Path $CodexHome "AGENTS.md")
Write-AgentPackInstallState -Profile $Profile -Target "codex" -ThirdPartyInstalledByPack $false -FirstPartySkills $Skills
Write-Host "Codex transactional install complete. Profile: $Profile"
