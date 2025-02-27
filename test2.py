# import streamlit as st
import markdown
import pdfkit
# from datetime import datetime
import os

# 设置保存 PDF 文件的目录

def save_pdf(markdown_content, pdf_path = r"generated_pdfs/output.pdf"):
    path_wk = r'.\wkhtmltopdf\bin\wkhtmltopdf.exe' #安装位置
    # markdown_content = 'markdown_content'
    # pdf_filename = "output.pdf"
    SAVE_DIR = "generated_pdfs"
    os.makedirs(SAVE_DIR, exist_ok=True)  # 如果目录不存在，则创建



    # # Streamlit 页面标题
    # st.title("Markdown 转 PDF")

    # # 用户输入 Markdown 内容
    # markdown_content = st.text_area("请输入 Markdown 内容：")

    if markdown_content:
        # 将 Markdown 转换为 HTML
        html_content = markdown.markdown(markdown_content,output_format='html',extensions=['tables'])
        styled_html = html_content
        # 添加基本的 HTML 样式
        styled_html = f"""
        <html>
            <head>
                <style>
                    body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    padding: 20px;
                    color: #333; /* 主文本颜色 */
                }}
                h1, h2, h3 {{
                    color: #000; /* 标题颜色为纯黑 */
                    margin-top: 1.5em;
                    margin-bottom: 0.5em;
                }}
                p {{
                    margin: 0.8em 0;
                }}
                code {{
                    background-color: #f5f5f5; /* 代码块背景色为浅灰 */
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: monospace;
                    color: #333; /* 代码文本颜色 */
                }}
                pre {{
                    background-color: #f5f5f5; /* 代码块背景色为浅灰 */
                    padding: 10px;
                    border-radius: 5px;
                    overflow-x: auto;
                    font-family: monospace;
                    color: #333; /* 代码文本颜色 */
                }}
                a {{
                    color: #007BFF; /* 链接颜色为蓝色 */
                    text-decoration: none;
                }}
                a:hover {{
                    text-decoration: underline;
                }}
                ul, ol {{
                    margin: 0.8em 0;
                    padding-left: 20px;
                }}
                blockquote {{
                    border-left: 4px solid #ddd; /* 引用块边框颜色为浅灰 */
                    padding-left: 10px;
                    color: #555; /* 引用文本颜色为深灰 */
                    margin: 1em 0;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1em 0;
                }}
                th, td {{
                    border: 1px solid #ddd; /* 表格边框颜色为浅灰 */
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f9f9f9; /* 表头背景色为浅灰 */
                    font-weight: bold;
                }}
                @page {{
                    size: A4;
                    margin: 20mm;
                    @top-center {{
                        content: "文档标题";
                        font-size: 12px;
                        color: #666; /* 页眉颜色为深灰 */
                    }}
                    @bottom-center {{
                        content: "第 " counter(page) " 页";
                        font-size: 12px;
                        color: #666; /* 页脚颜色为深灰 */
                    }}
                }}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """

        

        # 生成 PDF 文件
        
        # pdf_path = os.path.join(SAVE_DIR, pdf_filename)
        # print(pdf_path)
        # 使用 pdfkit 将 HTML 转换为 PDF
        try:
            
            config = pdfkit.configuration(wkhtmltopdf = path_wk)
            pdfkit.from_string(styled_html, pdf_path,configuration=config, options={'encoding': 'utf-8'})
            # st.success("PDF 文件已生成！")

            # 提供下载链接
            # with open(pdf_path, "rb") as f:
            #     pdf_bytes = f.read()
            # st.download_button(
            #     label="下载 PDF 文件",
            #     data=pdf_bytes,
            #     file_name=pdf_filename,
            #     mime="application/pdf"
            # )
        except Exception as e:
            raise e
            # st.error(f"生成 PDF 文件时出错：{e}")
if __name__ == '__main__':
    test = """
# 这h哈哈哈哈哈哈哈

## 这是一个 H2 标题

### 这是一个 H3 标题

下面是一个无序列表：

- 第一项
- 第二项
- 第三项

下面是一个有序列表：

1. 第一项
2. 第二项
3. 第三项

### 表格示例

| 姓名   | 年龄 | 职业     |
|--------|------|----------|
| 张三   | 25   | 程序员   |
| 李四   | 30   | 数据分析 |
| 王五   | 22   | 设计师   |

### 强调和代码示例

- 这是**加粗**文本
- 这是*斜体*文本
- 这是~~删除线~~文本

```python
# 这是一个 Python 代码块
def hello_world():
    print("Hello, World!")

    """
    save_pdf(test)