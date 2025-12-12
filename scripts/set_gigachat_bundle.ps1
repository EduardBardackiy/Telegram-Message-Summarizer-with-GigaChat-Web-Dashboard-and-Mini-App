$path = "F:\Zerocoder\Intensive\TGBot\certs\giga_chain.pem"
$envPath = ".env"

if (-not (Test-Path $envPath)) {
    Write-Host ".env not found"
    exit 1
}

$content = Get-Content $envPath
$updated = $false
for ($i = 0; $i -lt $content.Length; $i++) {
    if ($content[$i] -match '^GIGACHAT_CA_BUNDLE=') {
        $content[$i] = "GIGACHAT_CA_BUNDLE=$path"
        $updated = $true
    }
}

if (-not $updated) {
    $content += "GIGACHAT_CA_BUNDLE=$path"
}

Set-Content $envPath $content
Write-Host "Set GIGACHAT_CA_BUNDLE to $path"

