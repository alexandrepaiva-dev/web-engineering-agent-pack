param([string]$Backup="latest",[string]$ProjectDir=".")
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
$Python=if(Get-Command python -ErrorAction SilentlyContinue){"python"}elseif(Get-Command py -ErrorAction SilentlyContinue){"py"}else{throw "Python required"}
& $Python (Join-Path $Root "scripts\project_backup.py") restore $Backup --project-dir $ProjectDir
