param (
    [string]$InputFile,
    [string]$Resources,
    [int]$Width,
    [int]$Height,
    [string]$ExtraParams
)

Write-Host "InputFile: $InputFile"
Write-Host "Resources: $Resources"
Write-Host "Width: $Width"
Write-Host "Height: $Height"
Write-Host "ExtraParams: $ExtraParams"

$env:POVRAY_INPUT_FILE = "$InputFile"
$env:POVRAY_RESOURCES = "$Resources"
$env:POVRAY_WIDTH = "$Width"
$env:POVRAY_HEIGHT = "$Height"
$env:POVRAY_EXTRA_PARAMS = "$ExtraParams"

docker-compose -f (Join-Path $PSScriptRoot "docker-compose.yml") up