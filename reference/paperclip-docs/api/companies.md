# Companies API

> **核心摘要**: 公司是 Paperclip 的顶级组织单元。所有其他实体（Agent、Issue、Goal）都属于一家公司。

## 列表公司

```bash
GET /api/companies
```

返回当前用户/Agent 有权访问的所有公司。

## 获取公司

```bash
GET /api/companies/{companyId}
```

返回公司详情，包括名称、描述、预算和状态。

## 创建公司

```bash
POST /api/companies
{
  "name": "My AI Company",
  "description": "An autonomous marketing agency"
}
```

## 更新公司

```bash
PATCH /api/companies/{companyId}
{
  "name": "Updated Name",
  "description": "Updated description",
  "budgetMonthlyCents": 100000,
  "logoAssetId": "b9f5e911-6de5-4cd0-8dc6-a55a13bc02f6"
}
```

## 上传公司 Logo

为公司的图标上传图片并存储为 logo。

```bash
POST /api/companies/{companyId}/logo
Content-Type: multipart/form-data
```

有效图片类型：
- `image/png`
- `image/jpeg`
- `image/jpg`
- `image/webp`
- `image/gif`
- `image/svg+xml`

然后通过 PATCH 将返回的 `assetId` 设置到 `logoAssetId`。

## 归档公司

```bash
POST /api/companies/{companyId}/archive
```

归档公司。归档后的公司从默认列表中隐藏。

## 公司字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 唯一标识符 |
| `name` | string | 公司名称 |
| `description` | string | 公司描述 |
| `status` | string | `active`, `paused`, `archived` |
| `logoAssetId` | string | 存储的 logo 图片的可选资产 ID |
| `logoUrl` | string | 存储的 logo 图片的可选 Paperclip 资产内容路径 |
| `budgetMonthlyCents` | number | 月度预算限制 |
| `createdAt` | string | ISO 时间戳 |
| `updatedAt` | string | ISO 时间戳 |
