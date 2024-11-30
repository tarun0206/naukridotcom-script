$LocalTempDir = $env:TEMP
$ChromeInstaller = "ChromeInstaller.exe"
(new-object System.Net.WebClient).DownloadFile('http://dl.google.com/chrome/install/375.126/chrome_installer.exe', "$LocalTempDir\$ChromeInstaller")
& "$LocalTempDir\$ChromeInstaller" /silent /install
$Process2Monitor = "ChromeInstaller"
Do { 
    $ProcessesFound = Get-Process | Where-Object {$Process2Monitor -contains $_.Name} | Select-Object -ExpandProperty Name
    If ($ProcessesFound) { Start-Sleep -Seconds 2 } 
} Until (!$ProcessesFound)
Remove-Item "$LocalTempDir\$ChromeInstaller" -ErrorAction SilentlyContinue
