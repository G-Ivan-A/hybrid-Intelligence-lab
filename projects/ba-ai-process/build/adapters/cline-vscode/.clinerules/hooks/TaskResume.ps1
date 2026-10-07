try {
    [Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false)
    $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $env:PYTHONUTF8 = '1'
    $payload = [Console]::In.ReadToEnd()
    $runner = Join-Path $PSScriptRoot '..\..\tools\cline_hook.py'
    $response = $null
    # "python" may be missing or be the Microsoft Store alias (exit 9009); then use the py launcher.
    if (Get-Command python -ErrorAction SilentlyContinue) {
        $response = $payload | & python $runner
        if ($LASTEXITCODE -ne 0) { $response = $null }
    }
    if (-not $response -and (Get-Command py -ErrorAction SilentlyContinue)) {
        $response = $payload | & py -3 $runner
        if ($LASTEXITCODE -ne 0) { $response = $null }
    }
    if (-not $response) {
        throw 'Python hook failed'
    }
    Write-Output $response
} catch {
    Write-Output '{"cancel":true,"errorMessage":"Windows hook failed; check Python installation"}'
}
