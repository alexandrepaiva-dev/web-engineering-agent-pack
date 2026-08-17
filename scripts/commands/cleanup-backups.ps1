param([int]$Keep=5)
$ErrorActionPreference="Stop"
if($Keep -lt 0){throw "Keep must be >= 0"}
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
. (Join-Path $Root "scripts\BackupLib.ps1")
Ensure-BackupRoot
$dirs=Get-ChildItem -Directory $BackupRoot|Sort-Object Name -Descending
if($dirs.Count -le $Keep){Write-Host "Nothing to remove.";exit 0}
$dirs|Select-Object -Skip $Keep|ForEach-Object{Write-Host "Removing $($_.FullName)";Remove-Item -Recurse -Force $_.FullName}
