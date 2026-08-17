$StateFile = if ($env:AI_AGENT_PACK_STATE_FILE) { $env:AI_AGENT_PACK_STATE_FILE } else { Join-Path $HOME ".ai-agent-pack-state.json" }

function Write-AgentPackInstallState {
    param(
        [string]$Profile,
        [string]$Target,
        [bool]$ThirdPartyInstalledByPack,
        [string[]]$FirstPartySkills
    )

    $old=$null
    if(Test-Path $StateFile){
        try{$old=Get-Content $StateFile -Raw|ConvertFrom-Json}catch{$old=$null}
    }

    $mergedTarget=$Target
    if($old){
        if($old.target -eq "both" -or $Target -eq "both"){$mergedTarget="both"}
        elseif(($old.target -eq "codex" -and $Target -eq "claude") -or ($old.target -eq "claude" -and $Target -eq "codex")){$mergedTarget="both"}
    }

    $skills=@()
    if($old -and $old.firstPartySkills){$skills+=@($old.firstPartySkills)}
    $skills+=@($FirstPartySkills)
    $skills=@($skills|Sort-Object -Unique)

    [ordered]@{
        schemaVersion = 1
        packVersion = "1.0.0"
        profile = $Profile
        target = $mergedTarget
        thirdPartyInstalledByPack = ([bool]($old -and $old.thirdPartyInstalledByPack)) -or $ThirdPartyInstalledByPack
        firstPartySkills = $skills
        recommendedThirdPartySkills = @("ui-ux-pro-max","web-quality-audit")
    } | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $StateFile
}
