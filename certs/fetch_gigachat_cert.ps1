# Fetch GigaChat TLS certificate chain and save as PEM.
# Usage: powershell -ExecutionPolicy Bypass -File certs/fetch_gigachat_cert.ps1

$hostName = "ngw.devices.sberbank.ru"
$port = 9443
$outPath = Join-Path $PSScriptRoot "giga_chain.pem"

$tcp = New-Object Net.Sockets.TcpClient($hostName, $port)
$ssl = New-Object Net.Security.SslStream($tcp.GetStream(), $false, { $true })
$ssl.AuthenticateAsClient($hostName)

$chain = New-Object System.Security.Cryptography.X509Certificates.X509Chain
$chain.Build($ssl.RemoteCertificate) | Out-Null

$sb = New-Object System.Text.StringBuilder
foreach ($element in $chain.ChainElements) {
    $bytes = $element.Certificate.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
    $base64 = [System.Convert]::ToBase64String($bytes)
    $sb.AppendLine("-----BEGIN CERTIFICATE-----") | Out-Null
    for ($i = 0; $i -lt $base64.Length; $i += 64) {
        $len = [Math]::Min(64, $base64.Length - $i)
        $sb.AppendLine($base64.Substring($i, $len)) | Out-Null
    }
    $sb.AppendLine("-----END CERTIFICATE-----") | Out-Null
}

[IO.File]::WriteAllText($outPath, $sb.ToString())

$ssl.Dispose()
$tcp.Close()

Write-Host "Saved chain to $outPath"

