param(
    [string]$Profile,
    [string]$ProjectDir = ".",
    [ValidateSet("both","codex","claude")][string]$Target = "both",
    [switch]$IncludeCore,
    [switch]$InitProject,
    [switch]$DryRun,
    [switch]$Force,
    [string[]]$AddSkill = @(),
    [string[]]$RemoveSkill = @()
)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path))

if (-not $Profile) {
    Write-Host "Select project stack profile:"
    Write-Host "1) nextjs"
    Write-Host "2) symfony"
    Write-Host "3) nextjs-mysql"
    Write-Host "4) symfony-postgresql"
    Write-Host "5) full"
    $choice = Read-Host "Choice [1]"
    if (-not $choice) { $choice = "1" }
    $Profile = switch ($choice) {
        "1" { "nextjs" }
        "2" { "symfony" }
        "3" { "nextjs-mysql" }
        "4" { "symfony-postgresql" }
        "5" { "full" }
        default { throw "Invalid choice" }
    }
}

$Python = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } elseif (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { throw "Python is required." }
$argsList = @((Join-Path $Root "scripts\profile_manager.py"), "install-project", "--profile", $Profile, "--project-dir", $ProjectDir, "--target", $Target)
if ($IncludeCore) { $argsList += "--include-core" }
if ($InitProject) { $argsList += "--init-project" }
if ($DryRun) { $argsList += "--dry-run" }
if ($Force) { $argsList += "--force" }
foreach ($s in $AddSkill) { $argsList += @("--add-skill", $s) }
foreach ($s in $RemoveSkill) { $argsList += @("--remove-skill", $s) }
& $Python @argsList
