$PackVersion = "1.0.0"
$BackupRoot = if ($env:AI_AGENT_PACK_BACKUP_ROOT) { $env:AI_AGENT_PACK_BACKUP_ROOT } else { Join-Path $HOME ".ai-agent-pack-backups" }

function Ensure-BackupRoot { New-Item -ItemType Directory -Force -Path $BackupRoot | Out-Null }

function Copy-IfExists([string]$Source,[string]$Destination) {
  if (Test-Path $Source) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
    Copy-Item -Recurse -Force $Source $Destination
    return $true
  }
  return $false
}

function New-AgentPackSnapshot([string]$Reason="install") {
  Ensure-BackupRoot
  $stamp=Get-Date -Format "yyyyMMdd-HHmmss"
  $dest=Join-Path $BackupRoot $stamp
  $i=0
  while(Test-Path $dest){$i++;$dest=Join-Path $BackupRoot "$stamp-$i"}
  New-Item -ItemType Directory -Force -Path $dest | Out-Null

  $codexHome=if($env:CODEX_HOME){$env:CODEX_HOME}else{Join-Path $HOME ".codex"}
  $claudeHome=if($env:CLAUDE_CONFIG_DIR){$env:CLAUDE_CONFIG_DIR}else{Join-Path $HOME ".claude"}
  $codexSkills=if($env:AI_AGENT_PACK_CODEX_SKILLS_HOME){$env:AI_AGENT_PACK_CODEX_SKILLS_HOME}else{Join-Path $HOME ".agents\skills"}
  $stateFile=if($env:AI_AGENT_PACK_STATE_FILE){$env:AI_AGENT_PACK_STATE_FILE}else{Join-Path $HOME ".ai-agent-pack-state.json"}

  $items=[ordered]@{
    codexAgentsMd=(Copy-IfExists (Join-Path $codexHome "AGENTS.md") (Join-Path $dest "codex\AGENTS.md"))
    codexAgents=(Copy-IfExists (Join-Path $codexHome "agents") (Join-Path $dest "codex\agents"))
    codexSkills=(Copy-IfExists $codexSkills (Join-Path $dest "codex\skills"))
    claudeMd=(Copy-IfExists (Join-Path $claudeHome "CLAUDE.md") (Join-Path $dest "claude\CLAUDE.md"))
    claudeAgents=(Copy-IfExists (Join-Path $claudeHome "agents") (Join-Path $dest "claude\agents"))
    claudeSkills=(Copy-IfExists (Join-Path $claudeHome "skills") (Join-Path $dest "claude\skills"))
    installState=(Copy-IfExists $stateFile (Join-Path $dest "state\install-state.json"))
  }

  $manifest=[ordered]@{schemaVersion=1;packVersion=$PackVersion;createdAt=(Get-Date).ToString("o");reason=$Reason;codexHome=$codexHome;claudeHome=$claudeHome;codexSkillsHome=$codexSkills;items=$items}
  $manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 (Join-Path $dest "manifest.json")
  return $dest
}
