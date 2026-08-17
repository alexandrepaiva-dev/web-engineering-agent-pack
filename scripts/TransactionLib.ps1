function Replace-DirectoryTransactionally {
    param([string]$Stage,[string]$Target)
    $Old="$Target.weap-old-$PID"
    Remove-Item -Recurse -Force $Old -ErrorAction SilentlyContinue
    if(Test-Path $Target){Move-Item -Force $Target $Old}
    try{
        Move-Item -Force $Stage $Target
    }catch{
        Remove-Item -Recurse -Force $Target -ErrorAction SilentlyContinue
        if(Test-Path $Old){Move-Item -Force $Old $Target}
        throw
    }
    Remove-Item -Recurse -Force $Old -ErrorAction SilentlyContinue
}

function Replace-FileTransactionally {
    param([string]$Stage,[string]$Target)
    $Old="$Target.weap-old-$PID"
    Remove-Item -Force $Old -ErrorAction SilentlyContinue
    if(Test-Path $Target){Move-Item -Force $Target $Old}
    try{
        Move-Item -Force $Stage $Target
    }catch{
        Remove-Item -Force $Target -ErrorAction SilentlyContinue
        if(Test-Path $Old){Move-Item -Force $Old $Target}
        throw
    }
    Remove-Item -Force $Old -ErrorAction SilentlyContinue
}

function Test-SkillStage {
    param([string]$Stage,[int]$Expected)
    $dirs=@(Get-ChildItem -Directory $Stage)
    if($dirs.Count -ne $Expected){throw "Skill stage count mismatch: expected $Expected, got $($dirs.Count)"}
    foreach($d in $dirs){
        if(-not(Test-Path (Join-Path $d.FullName "SKILL.md"))){throw "Missing SKILL.md in $($d.FullName)"}
    }
}
