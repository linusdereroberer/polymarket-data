param([string]$Destination = 'restored-data', [string[]]$Archives = @())
$ErrorActionPreference = 'Stop'
$restoreArgs = @("$PSScriptRoot/restore.py", '--manifest', "$PSScriptRoot/MANIFEST.json", '--destination', $Destination)
if ($Archives.Count) { $restoreArgs += '--archives'; $restoreArgs += $Archives }
python @restoreArgs
if ($LASTEXITCODE -ne 0) { throw "Restore failed with exit code $LASTEXITCODE" }
