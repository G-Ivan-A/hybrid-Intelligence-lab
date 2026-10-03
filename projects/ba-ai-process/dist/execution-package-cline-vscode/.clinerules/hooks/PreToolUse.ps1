try {
    [Console]::InputEncoding = New-Object System.Text.UTF8Encoding($false)
    $OutputEncoding = New-Object System.Text.UTF8Encoding($false)
    $env:PYTHONUTF8 = '1'
    $payload = [Console]::In.ReadToEnd()
    $runner = Join-Path $PSScriptRoot '..\..\tools\cline_hook.py'
    $response = $payload | & python $runner
    if ($LASTEXITCODE -ne 0 -or -not $response) {
        throw 'Python hook failed'
    }
    Write-Output $response
} catch {
    Write-Output '{"cancel":true,"errorMessage":"Windows hook failed; check Python installation"}'
}
