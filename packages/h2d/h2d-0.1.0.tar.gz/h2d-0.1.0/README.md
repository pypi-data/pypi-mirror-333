# H2D - HTML to DOCX Converter

H2D 是一个 Python 包，用于将 HTML 内容转换为 DOCX 文档，支持常见的 HTML 标签和图片下载，并允许用户设置全局字体。

## 功能特性

- 支持常见的 HTML 标签，如 `<h1>` 到 `<h6>`、`<p>`、`<img>`、`<a>`、`<ul>`、`<ol>`、`<table>` 等。
- 自动下载并嵌入 `<img>` 和 `<a>` 标签中的图片。
- 允许通过 `setFont` 函数设置全局字体，支持中文字体。
- 支持解析内联 CSS 样式，如字体大小、颜色等。

## 安装

您可以通过 PyPI 安装 H2D 包：

```bash
pip install h2d
```

## 使用示例

以下是一个简单的使用示例，展示如何将 HTML 转换为 DOCX，并设置全局字体为“宋体”：

```python
import h2d

# 设置全局字体（可选）
h2d.setFont('宋体')

# 定义 HTML 字符串
html = """
<h1>一级标题（中文）</h1>
<h2>二级标题（中文）</h2>
<p>这是一个段落，包含 <strong>粗体</strong> 和 <em>斜体</em>。</p>
<img src="https://example.com/image.jpg" alt="示例图片" />
<ul>
    <li>列表项 1</li>
    <li>列表项 2</li>
</ul>
<table>
    <tr><th>表头</th></tr>
    <tr><td>单元格</td></tr>
</table>
"""

# 转换为 DOCX 并保存
docx = h2d.convert(html)
docx.save("output.docx")
```

## 使用文档

### `setFont(font_name_or_path)`

设置全局字体。参数可以是字体名称（如 `'Arial'`、`'宋体'`）或字体文件路径。

### `convert(html_string)`

将 HTML 字符串转换为 DOCX Document 对象。

## 依赖库

- `python-docx`
- `requests`
- `beautifulsoup4`
- `cssutils`

## 许可证

本项目采用 MIT 许可证，详情请参见 [LICENSE](LICENSE) 文件。

## 报告问题

如有问题或建议，请通过 [GitHub Issues](https://github.com/yourusername/h2d/issues) 联系我们。
