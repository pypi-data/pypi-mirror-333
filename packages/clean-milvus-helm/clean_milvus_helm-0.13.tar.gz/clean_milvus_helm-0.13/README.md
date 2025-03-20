# Clean Milvus Helm

一个用于清理旧的 Helm releases 的工具，主要用于清理 Milvus 相关的 helm charts。

## 功能特点

- 支持清理指定天数前的 helm releases
- 支持指定要清理的 chart 类型
- 提供干运行模式，可以预览将要删除的内容
- 支持自定义清理的 chart 类型列表

## 安装

```bash
pip install clean-milvus-helm
```

## 使用方法

```bash
# 干运行模式，显示3天前的待删除releases
clean-milvus-helm

# 实际执行删除操作
clean-milvus-helm --execute

# 自定义天数
clean-milvus-helm --days 7

# 自定义chart类型
clean-milvus-helm --charts "milvus,etcd"
```

## 参数说明

- `--execute`: 执行实际删除操作，不带此参数时为干运行模式
- `--days`: 指定清理几天前的releases，默认为3天
- `--charts`: 指定要清理的chart类型，用逗号分隔，默认为"milvus,etcd,minio,kafka"
