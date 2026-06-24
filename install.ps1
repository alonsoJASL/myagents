#Requires -Version 5
<#
.SYNOPSIS
  Installs myagents into %USERPROFILE%\.claude on Windows.

.DESCRIPTION
  Windows has no reliable symlink without elevation, so this copies the files
  instead of linking them. Because they are copies, re-run this script after
  editing anything in the repo for the changes to take effect.

  The custom status line (statusline.sh) is bash/jq based and is not installed
  on Windows; the statusLine setting is stripped from the copied settings.json
  so Claude Code falls back to its default status line.

.PARAMETER Force
  Overwrite files that already exist. Without it, existing files are skipped.
#>
param(
    [switch]$Force,
    [switch]$Agy,
    [switch]$Gemini
)

$ErrorActionPreference = 'Stop'

if ($Agy -or $Gemini) {
    $forceArg = ""
    if ($Force) { $forceArg = "--force" }
    # Invoke the python helper script (Windows copies files by default via --copy)
    python (Join-Path $PSScriptRoot 'install_agy.py') --copy $forceArg
    exit
}

$RepoDir     = $PSScriptRoot
$ClaudeDir   = Join-Path $env:USERPROFILE '.claude'
$CommandsDir = Join-Path $ClaudeDir 'commands'
$SkillsDir   = Join-Path $ClaudeDir 'skills'

function Copy-Item-Tracked {
    param(
        [string]$Source,
        [string]$Destination
    )
    if ((Test-Path $Destination) -and -not $Force) {
        Write-Host "  skipped  " -ForegroundColor Yellow -NoNewline
        Write-Host "$Destination (already exists; use -Force to overwrite)"
        return
    }
    Copy-Item -Path $Source -Destination $Destination -Force
    Write-Host "  copied   " -ForegroundColor Green -NoNewline
    Write-Host $Destination
}

Write-Host ""
Write-Host "Installing myagents into $ClaudeDir"
Write-Host ""

New-Item -ItemType Directory -Path $CommandsDir -Force | Out-Null

# CLAUDE.md
Copy-Item-Tracked (Join-Path $RepoDir 'CLAUDE.md') (Join-Path $ClaudeDir 'CLAUDE.md')

# settings.json with the (bash-based) statusLine stripped out
$SettingsDst = Join-Path $ClaudeDir 'settings.json'
if ((Test-Path $SettingsDst) -and -not $Force) {
    Write-Host "  skipped  " -ForegroundColor Yellow -NoNewline
    Write-Host "$SettingsDst (already exists; use -Force to overwrite)"
} else {
    $settings = Get-Content (Join-Path $RepoDir 'settings.json') -Raw | ConvertFrom-Json
    $settings.PSObject.Properties.Remove('statusLine')
    $settings | ConvertTo-Json -Depth 100 | Set-Content -Path $SettingsDst -Encoding UTF8
    Write-Host "  copied   " -ForegroundColor Green -NoNewline
    Write-Host "$SettingsDst (statusLine removed; Windows uses the default)"
}

# commands/*.md
Get-ChildItem -Path (Join-Path $RepoDir 'commands') -Filter '*.md' | ForEach-Object {
    Copy-Item-Tracked $_.FullName (Join-Path $CommandsDir $_.Name)
}

# Skills (each is a directory containing SKILL.md). Copied recursively, assets
# and all. Existing skill dirs are replaced only with -Force.
New-Item -ItemType Directory -Path $SkillsDir -Force | Out-Null
Get-ChildItem -Path $RepoDir -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName 'SKILL.md')
} | ForEach-Object {
    $dst = Join-Path $SkillsDir $_.Name
    if ((Test-Path $dst) -and -not $Force) {
        Write-Host "  skipped  " -ForegroundColor Yellow -NoNewline
        Write-Host "$dst (already exists; use -Force to overwrite)"
    } else {
        if (Test-Path $dst) { Remove-Item -Path $dst -Recurse -Force }
        Copy-Item -Path $_.FullName -Destination $dst -Recurse -Force
        Write-Host "  copied   " -ForegroundColor Green -NoNewline
        Write-Host $dst
    }
}

Write-Host ""
Write-Host "Done. These are copies, not symlinks: re-run install.ps1 after editing the repo."
Write-Host "Start a new Claude Code session to pick up the changes."
Write-Host ""
