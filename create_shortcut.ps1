<#
create_shortcut.ps1
Creates a Desktop shortcut (.lnk) pointing to a target executable.
Usage:
  .\create_shortcut.ps1 -TargetPath <path> [-IconPath <path>] [-Name <name>] [-Force]

Parameters:
  -TargetPath (required) : path to the target executable or file
  -IconPath  (optional)  : path to an .ico (or exe/dll) to use as icon
  -Name      (optional)  : friendly name for the shortcut (default: "Local TTS")
  -Force     (switch)    : overwrite existing shortcut if present
#>

param(
    [Parameter(Mandatory=$true)] [string]$TargetPath,
    [Parameter(Mandatory=$false)] [string]$IconPath = "",
    [Parameter(Mandatory=$false)] [string]$Name = "Local TTS",
    [switch]$Force
)

function Write-ErrAndExit($msg) {
    Write-Error $msg
    exit 1
}

# Resolve full paths and validate
try {
    $resolvedTarget = (Resolve-Path -Path $TargetPath -ErrorAction Stop).ProviderPath
} catch {
    Write-ErrAndExit "TargetPath '$TargetPath' not found or not accessible."
}

if ($IconPath -and $IconPath.Trim() -ne '') {
    try {
        $resolvedIcon = (Resolve-Path -Path $IconPath -ErrorAction Stop).ProviderPath
    } catch {
        Write-Warning "IconPath '$IconPath' not found - continuing without custom icon."
        $resolvedIcon = ""
    }
} else {
    $resolvedIcon = ""
}

$desktop = [Environment]::GetFolderPath('Desktop')
$lnkPath = Join-Path $desktop ("$Name.lnk")

if (Test-Path $lnkPath) {
    if ($Force) {
        Remove-Item $lnkPath -Force -ErrorAction SilentlyContinue
    } else {
        Write-Host "Shortcut already exists at $lnkPath. Use -Force to overwrite."; exit 0
    }
}

$ws = New-Object -ComObject WScript.Shell
$lnk = $ws.CreateShortcut($lnkPath)
$lnk.TargetPath = $resolvedTarget
if ($resolvedIcon -and (Test-Path $resolvedIcon)) { $lnk.IconLocation = $resolvedIcon }
$lnk.WorkingDirectory = (Get-Item $resolvedTarget).DirectoryName
$lnk.Save()

Write-Host "SHORTCUT_CREATED:`t$lnkPath"