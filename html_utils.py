# html.py

import markdown
from file import read_file

def convert_markdown_to_html(md_content):
    """
    MarkdownをHTMLに変換する関数。

    Args:
        md_content (str): Markdownの内容。

    Returns:
        str: 変換されたHTMLの内容。
    """
    return markdown.markdown(md_content, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'])

def generate_html_content(title, content):
    """
    HTMLファイルの内容を生成する関数。

    Args:
        title (str): HTMLファイルのタイトル。
        content (str): HTMLファイルの本文。

    Returns:
        str: 生成されたHTMLファイルの内容。
    """
    template = read_file("template_content.html")
    return template.format(title=title, content=content)

def generate_index_html(content):
    """
    index.htmlの内容を生成する関数。

    Args:
        content (str): index.htmlに追加するリンクのHTML。

    Returns:
        str: 生成されたindex.htmlの内容。
    """
    return generate_html_content("Index", f"<h1>Files</h1><ul>{content}</ul>")