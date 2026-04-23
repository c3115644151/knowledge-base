# 存储配置

> **核心摘要**: Paperclip 使用可配置存储提供者存储上传文件（Issue 附件、图片）。支持本地磁盘（默认）和 S3 兼容存储。

## 本地磁盘（默认）

文件存储在：

```
~/.paperclip/instances/default/data/storage/
```

无需配置。适用于本地开发和单机部署。

## S3 兼容存储

用于生产或多节点部署，使用 S3 兼容对象存储（AWS S3、MinIO、Cloudflare R2 等）。

通过 CLI 配置：

```bash
pnpm paperclipai configure --section storage
```

## 配置选项

| 提供商 | 最佳场景 |
|--------|----------|
| `local_disk` | 本地开发、单机器部署 |
| `s3` | 生产、多节点、云部署 |

存储配置存储在实例配置文件中：

```
~/.paperclip/instances/default/config.json
```
