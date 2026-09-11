<#
.SYNOPSIS
  Deploy every skill bundle in skills/ to a DSH user skill root.

.DESCRIPTION
  Walks skills/ (one directory = one bundle, must contain SKILL.md) and copies
  each bundle to the target skill root. The DSH watcher hot-reloads the newly
  installed skills; no restart is needed.

.EXAMPLE
  .\install.ps1                          # default: ~/.dsh/skills
  .\install.ps1 -Target C:\other\skills  # custom root
  .\install.ps1 -WhatIf                  # dry run
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$Target = "$env:USERPROFILE\.dsh\skills"
)

$ErrorActionPreference = 'Stop'
$src = Join-Path $PSScriptRoot 'skills'
if (-not (Test-Path $src)) { throw "skills/ not found next to install.ps1" }

New-Item -ItemType Directory -Force -Path $Target | Out-Null

$installed = 0
foreach ($bundle in (Get-ChildItem $src -Directory)) {
    if (-not (Test-Path (Join-Path $bundle.FullName 'SKILL.md'))) {
        Write-Warning "skip $($bundle.Name): no SKILL.md"
        continue
    }
    $dest = Join-Path $Target $bundle.Name
    if ($PSCmdlet.ShouldProcess($dest, 'install skill bundle')) {
        # Copy-Item -Recurse NESTS the source inside an existing destination
        # (dest\name\...). Clean-replace instead: remove, then copy fresh.
        if (Test-Path $dest) { Remove-Item $dest -Recurse -Force }
        Copy-Item $bundle.FullName $dest -Recurse
        $installed++
        Write-Host "installed: $($bundle.Name)"
    }
}

Write-Host "done: $installed skills -> $Target"
