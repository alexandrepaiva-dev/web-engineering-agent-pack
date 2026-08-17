param(
    [ValidateSet("both","codex","claude")][string]$Target="both",
    [switch]$DryRun
)
$ErrorActionPreference="Stop"
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$Python=if(Get-Command python -ErrorAction SilentlyContinue){"python"}elseif(Get-Command py -ErrorAction SilentlyContinue){"py"}else{throw "Python required"}
if(-not(Get-Command git -ErrorAction SilentlyContinue)){throw "git is required"}
$argsList=@((Join-Path $Root "scripts\install_locked_third_party.py"),"--target",$Target)
if($DryRun){$argsList+="--dry-run"}
& $Python @argsList
