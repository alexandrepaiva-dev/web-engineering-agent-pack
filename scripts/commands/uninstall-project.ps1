param(
 [string]$ProjectDir=".",
 [ValidateSet("both","codex","claude")][string]$Target="both",
 [switch]$RemoveAiConfig,
 [switch]$DryRun
)
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$Python=if(Get-Command python -ErrorAction SilentlyContinue){"python"}elseif(Get-Command py -ErrorAction SilentlyContinue){"py"}else{throw "Python required"}
$argsList=@((Join-Path $Root "scripts\uninstall_project.py"),"--project-dir",$ProjectDir,"--target",$Target)
if($RemoveAiConfig){$argsList+="--remove-ai-config"}
if($DryRun){$argsList+="--dry-run"}
& $Python @argsList
