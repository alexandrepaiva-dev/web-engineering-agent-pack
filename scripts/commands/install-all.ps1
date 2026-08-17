param([string]$Profile="core",[switch]$DryRun,[switch]$WithThirdParty,[string[]]$AddSkill=@(),[string[]]$RemoveSkill=@())
$ErrorActionPreference="Stop"
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
. (Join-Path $Root "scripts\BackupLib.ps1")
. (Join-Path $Root "scripts\StateLib.ps1")

if($DryRun){
  & (Join-Path $Root "scripts\commands\install-codex.ps1") -Profile $Profile -DryRun -AddSkill $AddSkill -RemoveSkill $RemoveSkill
  & (Join-Path $Root "scripts\commands\install-claude.ps1") -Profile $Profile -DryRun -AddSkill $AddSkill -RemoveSkill $RemoveSkill
  if($WithThirdParty){& (Join-Path $Root "scripts\commands\install-third-party-skills.ps1") -DryRun}
  exit 0
}

$b=New-AgentPackSnapshot "install-all:$Profile"
$BackupName=Split-Path -Leaf $b
Write-Host "Snapshot: $b"
try{
  & (Join-Path $Root "scripts\commands\install-codex.ps1") -Profile $Profile -SkipSnapshot -AddSkill $AddSkill -RemoveSkill $RemoveSkill
  & (Join-Path $Root "scripts\commands\install-claude.ps1") -Profile $Profile -SkipSnapshot -AddSkill $AddSkill -RemoveSkill $RemoveSkill
  if($WithThirdParty){& (Join-Path $Root "scripts\commands\install-third-party-skills.ps1")}
}catch{
  Write-Warning "Installation failed. Restoring $BackupName"
  & (Join-Path $Root "scripts\commands\restore-backup.ps1") $BackupName
  throw
}

$Python=if(Get-Command python -ErrorAction SilentlyContinue){"python"}elseif(Get-Command py -ErrorAction SilentlyContinue){"py"}else{throw "Python required"}
$args=@((Join-Path $Root "scripts\profile_manager.py"),"resolve","--profile",$Profile)
foreach($s in $AddSkill){$args+=@("--add-skill",$s)}
foreach($s in $RemoveSkill){$args+=@("--remove-skill",$s)}
$Skills=@(& $Python @args)
Write-AgentPackInstallState -Profile $Profile -Target "both" -ThirdPartyInstalledByPack ([bool]$WithThirdParty) -FirstPartySkills $Skills
Write-Host "Transactional installation complete. Profile: $Profile"
