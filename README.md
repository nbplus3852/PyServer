# PyServer

PyServer 是一个轻量且高效的基于 Python 的 Web 服务器，旨在处理 HTTP 请求并提供 Web 静态页面。

## 特性

- 易于设置和使用
- 轻量且高效
- 支持 HTTP/1.1
- 可定制的请求处理

## 安装

要安装 PyServer，请克隆仓库并安装所需的依赖项：

```bash
git clone https://github.com/nbplus3852/PyServer.git
```

## 使用

目前仅在Python3.13版本中通过测试

要启动服务器，请运行以下命令：

```bash
python main.py
```

默认情况下，服务器将运行在 `http://127.0.0.1:8080`。您可以通过修改 `settings.json` 文件来自定义主机和端口。

## 配置

服务器配置可以在 `settings.json` 文件中自定义。以下是一些可用的选项：

- `HOST`: 绑定服务器的主机名（默认值：`127.0.0.1`）
- `PORT`: 绑定服务器的端口号（默认值：`8080`）

## 贡献

欢迎贡献！请 fork 仓库并提交 pull request 以进行更改。

## 许可证

此项目根据 GPLv3 许可证授权。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 联系

如有任何问题或咨询，请联系 nbplus3852@outlook.com。
