$ErrorActionPreference = 'Stop'
Set-Location 'C:\Users\user\NTBE'
py -3 .\ntbe_l2_verify.py --root . --mode pilot
Write-Host 'Pilot completed. Inspect all pilot outputs BEFORE running full.'
