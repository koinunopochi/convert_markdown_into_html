import re
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os

from file_utils import read_file
def convert_markdown_to_html(md_content, icon_dir):
    """
    MarkdownをHTMLに変換する関数。

    Args:
        md_content (str): Markdownの内容。
        icon_dir (str): アイコンファイルのディレクトリパス。

    Returns:
        str: 変換されたHTMLの内容。
    """
    extensions = ['markdown.extensions.fenced_code', 'codehilite']
    html_content = markdown.markdown(md_content, extensions=extensions)
    
    # info、warn、errorのブロックを変換
    html_content = convert_info_warn_error_blocks(html_content, icon_dir)
    
    return html_content

def convert_info_warn_error_blocks(html_content, icon_dir):
    """
    info、warn、errorのブロックを適切なHTMLに変換する関数。

    Args:
        html_content (str): HTMLの内容。
        icon_dir (str): アイコンファイルのディレクトリパス。

    Returns:
        str: 変換後のHTMLの内容。
    """
    def replace_block(match):
        block_type = match.group(1)
        content = match.group(2).strip()
        
        if block_type == 'info':
            icon_path = os.path.join(icon_dir, 'info.svg')
            style = 'style-info'
        elif block_type == 'warn':
            icon_path = os.path.join(icon_dir, 'warn.svg')
            style = 'style-warn'
        elif block_type == 'error':
            icon_path = os.path.join(icon_dir, 'error.svg')
            style = 'style-error'
        
        # SVGファイルを読み込んでアイコンを生成
        with open(icon_path, 'r') as file:
            icon = file.read()
        
        # 複数行の場合は<br>タグを追加
        content = content.replace('\n', '<br>')
        
        return f'<div class="{style}">{icon}<p>{content}</p></div>'
    
    pattern = re.compile(r':::note (info|warn|error)\s*(.*?):::(?!:)', re.DOTALL)
    html_content = pattern.sub(replace_block, html_content)
    
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