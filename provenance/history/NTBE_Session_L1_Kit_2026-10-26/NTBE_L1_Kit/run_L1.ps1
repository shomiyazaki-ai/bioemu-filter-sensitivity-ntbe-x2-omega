$ErrorActionPreference = 'Stop'
$root = 'C:\Users\user\NTBE'
$bench = Join-Path $root 'bioemu-benchmarks_code_release.zip'
if (-not (Test-Path -LiteralPath $bench)) {
    $bench = Join-Path $root 'bioemu-benchmarks_code_release(8).zip'
}
if (-not (Test-Path -LiteralPath $bench)) {
    throw '公式bioemu-benchmarks_code_release ZIPが見つかりません。'
}
$pyargs = @((Join-Path $root 'ntbe_l1_verify.py'), '--root', $root, '--benchmark', $bench, '--coordinate-qa')
$npz = Join-Path $root 'all_npz(1).zip'
if (Test-Path -LiteralPath $npz) { $pyargs += @('--all-npz', $npz) }
$systems = Join-Path $root 'NTBE_systems_154_reconciled(5).csv'
if (Test-Path -LiteralPath $systems) { $pyargs += @('--systems', $systems) }
py -3 @pyargs
if ($LASTEXITCODE -ne 0) { Write-Warning "L1結果はPASSではありません。終了コード=$LASTEXITCODE。L1_report.jsonを確認してください。" }
