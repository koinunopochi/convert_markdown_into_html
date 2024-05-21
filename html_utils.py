import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os

from file_utils import read_file


def convert_markdown_to_html(md_content):
    """
    MarkdownをHTMLに変換する関数。

    Args:
        md_content (str): Markdownの内容。

    Returns:
        str: 変換されたHTMLの内容。
    """
    extensions = ['markdown.extensions.fenced_code', 'codehilite']
    html_content = markdown.markdown(md_content, extensions=extensions)
    return html_content

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

def generate_pygments_css(output_dir):
    """
    Pygmentsのスタイルを使用してハイライト用のCSSファイルを生成する関数。

    Args:
        output_dir (str): 出力先のディレクトリのパス。
    """
    formatter = HtmlFormatter(style='default')
    css_content = formatter.get_style_defs('.codehilite')
    css_dir = os.path.join(output_dir, 'css')
    os.makedirs(css_dir, exist_ok=True)
    css_path = os.path.join(css_dir, 'pygments.css')
    with open(css_path, 'w', encoding='utf-8') as file:
        file.write(css_content)

def generate_index_html(index_content):
    """
    index.htmlの内容を生成する関数。

    Args:
        index_content (str): index.htmlに追加するリンクのHTML。

    Returns:
        str: 生成されたindex.htmlの内容。
    """
    return generate_html_content("Index", f"<h1>Files</h1><ul>{index_content}</ul>")

def generate_link_html(html_file, link_text):
    """
    リンクのHTMLを生成する関数。

    Args:
        html_file (str): HTMLファイル名。
        link_text (str): リンクテキスト。

    Returns:
        str: 生成されたリンクのHTML。
    """
    return f"<li><a href='{html_file}'>{link_text}</a></li>\n"