$thisdir=Get-ChildItem
if ($thisdir.Name.IndexOf("build") -eq -1) {
    New-Item -Name build -ItemType directory
}
$allfile=Get-ChildItem .\src
foreach ($f in $allfile) {
    if (($f.Name.IndexOf("wormv.") -eq -1) -and ($f.Mode[0] -ne 'd')) {
        Copy-Item ".\src\$f" ".\build\$f"
    }
}
cl /Fe: .\build\wormv.exe .\src\wormv.cpp
Remove-Item .\wormv.obj
Set-Location .\build
Rename-Item wocr.py -NewName wocr.pyw
Set-Location ..