param (
    [string]$InputFile,
    [string]$Resources,
    [int]$Width,
    [int]$Height,
    [string]$ExtraParams
)

$env:POVRAY_INPUT_FILE = $InputFile
$env:POVRAY_RESOURCES = $Resources
$env:POVRAY_WIDTH = $Width
$env:POVRAY_HEIGHT = $Height
$env:POVRAY_EXTRA_PARAMS = $ExtraParams

docker-compose up