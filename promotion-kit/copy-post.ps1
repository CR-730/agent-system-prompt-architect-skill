param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("juejin", "zhihu", "v2ex", "linux-do", "segmentfault", "oschina", "csdn", "cnblogs", "appinn")]
  [string]$Platform
)

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$post = Join-Path $root "posts\$Platform.md"

if (-not (Test-Path -LiteralPath $post)) {
  throw "Post file not found: $post"
}

$content = Get-Content -LiteralPath $post -Raw -Encoding UTF8
Set-Clipboard -Value $content
Write-Host "Copied $Platform post to clipboard: $post"
