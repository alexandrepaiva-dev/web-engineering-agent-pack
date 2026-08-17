$ErrorActionPreference="Stop"
$Root=Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))
. (Join-Path $Root "scripts\BackupLib.ps1")
Ensure-BackupRoot
$rows=foreach($d in Get-ChildItem -Directory $BackupRoot | Sort-Object Name -Descending){$m=Join-Path $d.FullName "manifest.json";if(Test-Path $m){try{$j=Get-Content $m -Raw|ConvertFrom-Json;[PSCustomObject]@{Backup=$d.Name;Pack=$j.packVersion;Reason=$j.reason;Created=$j.createdAt}}catch{[PSCustomObject]@{Backup=$d.Name;Pack="?";Reason="?";Created="?"}}}}
if($rows){$rows|Format-Table -AutoSize}else{Write-Host "No backups found in $BackupRoot"}
