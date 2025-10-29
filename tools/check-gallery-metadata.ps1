<#
Check gallery metadata vs files.
Usage:
  Open PowerShell in project root and run:
    .\tools\check-gallery-metadata.ps1
#>

$galleryDir = Join-Path $PSScriptRoot '..\gallery' | Resolve-Path | Select-Object -ExpandProperty Path -ErrorAction SilentlyContinue
if (-not $galleryDir) { $galleryDir = Join-Path (Get-Location) 'gallery' }
$metaFile = Join-Path (Join-Path $PSScriptRoot '..') 'gallery\metadata.json'

Write-Host "Gallery dir: $galleryDir"
Write-Host "Metadata file: $metaFile"

# Only consider image files in the gallery folder (ignore metadata.json and others)
$files = @()
if (Test-Path $galleryDir) {
  $files = Get-ChildItem -Path $galleryDir -File | Where-Object { $_.Extension -match '\.jpg$|\.jpeg$|\.png$|\.gif$|\.webp$|\.svg$' } | Select-Object -ExpandProperty Name
}
else { Write-Host "Gallery folder not found: $galleryDir" -ForegroundColor Yellow; exit 1 }

if (-not (Test-Path $metaFile)) {
  Write-Host "metadata.json not found at $metaFile" -ForegroundColor Yellow
  Write-Host "Found image files:"; $files | ForEach-Object { Write-Host " - $_" }
  exit 1
}

$meta = Get-Content -Raw -Path $metaFile | ConvertFrom-Json

# Normalize metadata srcs (strip any leading folder components) for comparison
$metaSrcs = $meta | ForEach-Object { ([IO.Path]::GetFileName($_.src)) }

# Files without metadata entries
$orphanFiles = $files | Where-Object { $_ -notin $metaSrcs }

# Metadata entries pointing to missing files: check existence by trying both the raw src and the filename inside the gallery dir
$missingFiles = @()
foreach ($entry in $meta) {
  $raw = $entry.src -as [string]
  $candidatePaths = @()
  # if src is an absolute or relative path (e.g., 'gallery/image1.jpg'), try both as-is relative to project root, and as filename inside gallery dir
  $candidatePaths += Join-Path $galleryDir ([IO.Path]::GetFileName($raw))
  # also try root-relative (project root + src)
  $projRelative = Join-Path (Join-Path $PSScriptRoot '..') $raw
  $candidatePaths += $projRelative

  $exists = $false
  foreach ($p in $candidatePaths) {
    if (Test-Path $p) { $exists = $true; break }
  }
  if (-not $exists) { $missingFiles += $entry }
}

if ($orphanFiles.Count -eq 0) { Write-Host "No orphan image files found." -ForegroundColor Green }
else {
  Write-Host "Files that have no metadata entry:" -ForegroundColor Cyan
  $orphanFiles | ForEach-Object { Write-Host " - $_" }
}

if ($missingFiles.Count -eq 0) { Write-Host "No metadata entries pointing to missing files." -ForegroundColor Green }
else {
  Write-Host "Metadata entries with missing files:" -ForegroundColor Magenta
  $missingFiles | ForEach-Object { Write-Host " - id:$($_.id) src:$($_.src) title:$($_.title)" }
}

# Quick summary
Write-Host "\nSummary:" -ForegroundColor White
Write-Host " Total image files: $($files.Count)"
Write-Host " Metadata entries : $($meta.Count)"

if ($orphanFiles.Count -gt 0 -or $missingFiles.Count -gt 0) { exit 2 } else { exit 0 }
