param([Parameter(ValueFromRemainingArguments=$true)][string[]]$Args)
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
$Python=if(Get-Command python -ErrorAction SilentlyContinue){"python"}elseif(Get-Command py -ErrorAction SilentlyContinue){"py"}else{throw "Python required"}
& $Python (Join-Path $Root "weap.py") @Args
exit $LASTEXITCODE
