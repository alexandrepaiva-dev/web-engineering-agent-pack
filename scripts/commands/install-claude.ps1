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

$ClaudeHome=if($env:CLAUDE_CONFIG_DIR){$env:CLAUDE_CONFIG_DIR}else{Join-Path $HOME ".claude"}
$SkillsHome=Join-Path $ClaudeHome "skills"
if($DryRun){Write-Host "Claude transactional install: $Profile ($($Skills.Count) skills)";Write-Host "Preserve: settings.json/settings.local.json";exit 0}
if(-not $SkipSnapshot){$b=New-AgentPackSnapshot "claude-install:$Profile";Write-Host "Snapshot: $b"}

New-Item -ItemType Directory -Force -Path $ClaudeHome|Out-Null
$StageSkills=Join-Path $ClaudeHome ".weap-skills-stage-$PID"
$StageAgents=Join-Path $ClaudeHome ".weap-agents-stage-$PID"
$StageMd=Join-Path $ClaudeHome ".weap-CLAUDE-stage-$PID.md"
Remove-Item -Recurse -Force $StageSkills,$StageAgents -ErrorAction SilentlyContinue
Remove-Item -Force $StageMd -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $StageSkills,$StageAgents|Out-Null
Copy-Item -Force (Join-Path $Root "claude\global\.claude\CLAUDE.md") $StageMd
Copy-Item -Recurse -Force (Join-Path $Root "claude\global\.claude\agents\*") $StageAgents
foreach($s in $Skills){Copy-Item -Recurse -Force (Join-Path $Root "shared\skills\$s") (Join-Path $StageSkills $s)}
& $Python (Join-Path $Root "scripts\install-claude-skill-overlays.py") $StageSkills
Test-SkillStage $StageSkills $Skills.Count
Replace-DirectoryTransactionally $StageAgents (Join-Path $ClaudeHome "agents")
Replace-DirectoryTransactionally $StageSkills $SkillsHome
Replace-FileTransactionally $StageMd (Join-Path $ClaudeHome "CLAUDE.md")
Write-AgentPackInstallState -Profile $Profile -Target "claude" -ThirdPartyInstalledByPack $false -FirstPartySkills $Skills
Write-Host "Claude transactional install complete. Profile: $Profile"
