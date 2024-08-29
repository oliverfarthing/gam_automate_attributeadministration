# Define source and destination folder paths
$sourceFolder = "C:\gamsync\automate\servicerecruitment_meetings"
$destinationFolder = "C:\gamsync\automate\servicerecruitment_meetings\logs"

# Check if the destination folder exists; if not, create it
if (-not (Test-Path -Path $destinationFolder)) {
    New-Item -Path $destinationFolder -ItemType Directory
    Write-Host "Created logs directory at $destinationFolder"
}

# Get all CSV files from the source folder
$csvFiles = Get-ChildItem -Path $sourceFolder -Filter *.csv

# Loop through each file
foreach ($file in $csvFiles) {
    # Create a timestamp in the format "yyyy-MM-dd_HHmmss"
    $timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
    
    # Generate the destination file name with the timestamp
    $newFileName = "{0}_{1}{2}" -f $file.BaseName, $timestamp, $file.Extension
    
    # Copy the file to the destination folder with the new name
    Copy-Item -Path $file.Name -Destination (Join-Path $destinationFolder $newFileName)
}

Write-Host "CSV files copied with timestamps!"
