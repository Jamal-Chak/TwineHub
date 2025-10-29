<#
Copies social icon PNG files from a source folder (Downloads by default) into the project's images/ folder.

Usage:
  # Dry-run (shows what would be copied)
  .\tools\install-social-icons.ps1 -WhatIf

  # Run and copy from default Downloads folder
  .\tools\install-social-icons.ps1

  # Specify a custom source folder
  .\tools\install-social-icons.ps1 -Source 'C:\Users\Tessl\Downloads'

The script looks for common filenames (facebook.png, instagram.png, whatsapp.png, social.png, facebook_icon.png, instagram_icon.png)
and copies them to the project's images directory with the expected names (facebook.png, instagram.png, whatsapp.png).
#>

param(
  [string]$Source = "$env:USERPROFILE\Downloads",
  [switch]$WhatIf
)

$projectRoot = Join-Path $PSScriptRoot '..' | Resolve-Path | Select-Object -ExpandProperty Path
$imagesDir = Join-Path $projectRoot 'images'

if (-not (Test-Path $imagesDir)) { New-Item -ItemType Directory -Path $imagesDir | Out-Null }

$candidates = @(
  @{src='facebook.png'; dest='facebook.png'},
  @{src='facebook_icon.png'; dest='facebook.png'},
  @{src='instagram.png'; dest='instagram.png'},
  @{src='instagram_icon.png'; dest='instagram.png'},
  @{src='whatsapp.png'; dest='whatsapp.png'},
  @{src='social.png'; dest='facebook.png'}  # try social.png as fallback for facebook
)

$found = @()
foreach ($c in $candidates) {
  $srcPath = Join-Path $Source $c.src
  if (Test-Path $srcPath) {
    $destPath = Join-Path $imagesDir $c.dest
    $found += [PSCustomObject]@{Src=$srcPath; Dest=$destPath}
  }
}

if ($found.Count -eq 0) {
  Write-Host "No candidate PNG files found in $Source. Checked filenames: $($candidates.src -join ', ')" -ForegroundColor Yellow
  Write-Host "You can pass -Source to point to a different folder or copy files manually into $imagesDir.";
  exit 1
}

Write-Host "Found the following files to copy:" -ForegroundColor Cyan
foreach ($f in $found) { Write-Host " $($f.Src) -> $($f.Dest)" }

if ($WhatIf) { Write-Host "Dry run (-WhatIf) - no files copied."; exit 0 }

foreach ($f in $found) {
  try {
    Copy-Item -Path $f.Src -Destination $f.Dest -Force
    Write-Host "Copied: $($f.Src) -> $($f.Dest)" -ForegroundColor Green
  } catch {
    Write-Host "Failed to copy $($f.Src): $_" -ForegroundColor Red
  }
}

Write-Host "Done. You can now open the site; social PNGs will be available in the images/ folder." -ForegroundColor Green
