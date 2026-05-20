$urls = @(
  "https://juejin.cn/editor/drafts/new",
  "https://zhuanlan.zhihu.com/write",
  "https://www.v2ex.com/new",
  "https://linux.do/new-topic",
  "https://segmentfault.com/write",
  "https://my.oschina.net/u/0/blog/write",
  "https://editor.csdn.net/md",
  "https://i.cnblogs.com/posts/edit",
  "https://meta.appinn.net/new-topic"
)

foreach ($url in $urls) {
  Start-Process $url
  Start-Sleep -Milliseconds 300
}

Write-Host "Opened publish pages. Use copy-post.ps1 to copy platform-specific drafts."
