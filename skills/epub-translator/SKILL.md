---
name: epub-translator
description: 翻译 EPUB 电子书文件，同时保留格式、结构和元数据。当用户需要翻译 .epub 文件时使用此技能，支持：(1) 完整书籍翻译，(2) 章节选择性翻译，(3) 翻译前样本预览，(4) 自定义翻译规则（保留术语、人名等），(5) 多语言互译
---

# EPUB 翻译器

将 EPUB 电子书从一种语言翻译为另一种语言，同时保持原始格式、章节结构和元数据完整。

## 快速开始

基本用法：

```
将这个 EPUB 从英文翻译成中文
```

带自定义规则：

```
翻译成中文，保留所有人名和地名的英文原文
```

## 工作流程

### 1. 文件分析

读取用户上传的 EPUB 文件：

```javascript
const fileData = await window.fs.readFile(filename);
```

EPUB 是 ZIP 格式，包含：
- `META-INF/container.xml` - 指向内容清单
- `content.opf` - 元数据和文件清单
- `toc.ncx` - 目录
- HTML/XHTML 章节文件（通常在 `OEBPS/`, `EPUB/` 或 `text/` 目录）

提取并展示：
- 书籍标题和作者
- 章节数量
- 估计字数

### 2. 确认翻译参数

询问用户：
- 目标语言
- 特殊要求（保留术语、人名处理方式等）
- 是否需要查看样本

### 3. 样本翻译（推荐）

翻译第一章或前 1000 字，展示给用户确认翻译风格和质量。

### 4. 执行翻译

逐章翻译内容：
- 提取 HTML 中的文本节点
- 保留 HTML 标签结构
- 翻译文本内容
- 维护跨章节的术语一致性


**进度更新**：大型书籍每完成 2-3 章更新一次进度

### 5. 重建 EPUB

- 将翻译后的文本插回 HTML 结构
- 翻译目录（如有）
- 更新 `content.opf` 元数据（添加语言标记）
- 保持原始文件结构
- 重新打包为 ZIP（.epub 扩展名）

### 6. 质量验证

检查：
- 所有章节是否完整
- HTML 标签是否闭合
- 特殊字符是否正确编码

## 翻译指南

### 文本处理

- 保持段落完整，不拆分句子
- 跨段落的上下文保持一致
- 对话使用目标语言的引号规范

### 目录处理
目录也要进行翻译。
目录文件名一般为：`toc.ncx`，只需要翻译`<text></text>`标签内的文本。

### 格式保留

- 只翻译文本内容，完全保留所有 HTML 标签、属性、样式。
- 段落结构不变
- 示例：`<p class="text">Hello</p>` → `<p class="text">你好</p>`

### 术语一致性

建立术语表，确保：
- 人物名称统一
- 地名翻译一致
- 专有名词处理规范
- 人名、地名等第一次出现：译名(原名)
- 后续出现只用译名：于连·索雷尔
- 示例：于连·索雷尔(Julien Sorel)

### 翻译质量

- 准确、流畅、符合目标语言的表达习惯
- 保持原文的文学风格和语气
- 注意上下文，不要逐字翻译

## 技术实现

### 依赖库

使用 JSZip 处理 EPUB：

```javascript
// 解压 EPUB
const zip = await JSZip.loadAsync(fileData);

// 读取文件
const content = await zip.file('OEBPS/chapter1.html').async('string');

// 修改后重新打包
zip.file('OEBPS/chapter1.html', translatedContent);
const newEpub = await zip.generateAsync({type: 'blob'});
```

### HTML 解析

分离文本与标签：

```javascript
// 提取文本节点，保留标签
const parser = new DOMParser();
const doc = parser.parseFromString(html, 'text/html');

// 遍历文本节点翻译
function translateTextNodes(node) {
  if (node.nodeType === Node.TEXT_NODE) {
    node.textContent = translate(node.textContent);
  } else {
    node.childNodes.forEach(translateTextNodes);
  }
}
```

### 元数据更新

在 `content.opf` 中添加语言标记：

```xml
<!-- 假设源文件被翻译为了中文，就插入zh -->
<dc:language>zh</dc:language>
<meta property="dcterms:modified">2026-01-20T12:00:00Z</meta>
```

## 边缘情况

### 混合语言内容

书中已有多种语言时：
- 询问用户是否翻译所有内容
- 或仅翻译主要语言部分

### 特殊格式

- **诗歌**：保持行分隔，注意韵律损失
- **表格**：仅翻译表格内文本，保持结构
- **代码块**：默认不翻译，除非用户指定

### 大文件处理

超过 5MB 或 50 章的书籍：
- 提供分批翻译选项
- 定期保存进度
- 允许从中断处继续

## 限制说明

**无法处理**：
- DRM 加密的 EPUB
- 图片中的嵌入文字（仅翻译 alt 文本）
- 固定布局 EPUB（需特殊处理）

**质量提醒**：
大型文献（学术书籍、技术手册）建议用户审核样本章节，确认专业术语翻译准确。

## 示例交互

**示例 1：基础翻译**

```
用户：将这本英文小说翻译成中文
助手：好的，让我先分析这个 EPUB 文件...

发现：
- 书名：The Great Gatsby
- 作者：F. Scott Fitzgerald
- 章节：9 章
- 约 47,000 词

在翻译全书前，我先翻译第一章给您看看翻译风格：

[展示第一章样本]

翻译风格如何？需要调整吗？
```

**示例 2：自定义规则**

```
用户：翻译成日语，但保留所有魔法咒语为英文原文
助手：明白了，我会：
1. 将叙述和对话翻译成日语
2. 识别魔法咒语（通常为斜体或特殊标记）
3. 保留这些咒语的英文原文

开始翻译...
```

## 输出格式

生成可下载的 .epub 文件：
- 文件名：`[原书名]_[目标语言].epub`
- 元数据包含翻译信息
- 兼容标准 EPUB 阅读器（Calibre、Apple Books 等）