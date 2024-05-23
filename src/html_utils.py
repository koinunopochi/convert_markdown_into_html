import re
import unicodedata
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os

from file_utils import read_file

def convert_markdown_to_html(md_content, icon_dir, anchor_links):
    """
    MarkdownをHTMLに変換する関数。

    Args:
        md_content (str): Markdownの内容。
        icon_dir (str): アイコンファイルのディレクトリパス。
        anchor_links (bool): アンカーリンクを生成するかどうか。

    Returns:
        str: 変換されたHTMLの内容。
    """
    # ネストされたリストを適切に処理
    md_content = convert_nested_lists(md_content)

    extensions = [
        'markdown.extensions.fenced_code', 
        'codehilite', 'markdown.extensions.toc', 
        'markdown.extensions.tables', 
        ]
    extension_configs = {
        'markdown.extensions.toc': {
            'anchorlink': anchor_links,
            'permalink': anchor_links,
            'toc_depth': '2-4',
        },
    }
    md = markdown.Markdown(extensions=extensions, extension_configs=extension_configs)

    html_content = md.convert(md_content)

    # 目次を取得
    toc = md.toc if anchor_links else ""

    # info、warn、errorのブロックを変換
    html_content = convert_info_warn_alert_blocks(html_content, icon_dir)

    # 目次を右側に配置
    if anchor_links:
        html_content = f"<div class='root'><div class='content'>{html_content}</div>{toc}</div>"
    else:
        html_content = f"<div class='root'><div class='content'>{html_content}</div></div>"

    return html_content

def slugify(value, separator):
    """
    文字列をスラッグ化する関数。

    Args:
        value (str): スラッグ化する文字列。
        separator (str): スラッグのセパレータ。

    Returns:
        str: スラッグ化された文字列。
    """
    slug = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    slug = re.sub(r'[^\w\s-]', '', slug).strip().lower()
    slug = re.sub(r'[-\s]+', separator, slug)
    return slug

# TODO:あまりにも汚いコードなのでリファクタリングする
def convert_nested_lists(md_content):
    """
    ネストされたリストを適切に処理する関数。

    Args:
        md_content (str): Markdownの内容。

    Returns:
        str: 変換されたMarkdownの内容。
    """
    # 番号なしリストを変換
    md_content = convert_unordered_list(md_content)
    # 番号付きリストを変換
    md_content = convert_ordered_list(md_content)
    return md_content

def convert_ordered_list(md_content):
    """
    番号付きリストを変換する関数。
    Args:
        md_content (str): Markdownの内容。
    Returns:
        str: 変換されたHTMLの内容。
    """
    # Markdownの内容を各行に分割
    lines = md_content.split('\n')
    # 変換後のHTMLの各行を格納するリスト
    converted_lines = []
    # リストのスタック（開いているリストの情報を追跡）
    list_stack = []
    # テーブルの状態を追跡するフラグ
    inside_table = False

    # 各行に対して処理を行う
    for line in lines:
        # テーブルの開始行を検出する
        if line.strip().startswith('|'):
            inside_table = True

        # テーブルの終了行を検出する
        if inside_table and not line.strip().startswith('|'):
            inside_table = False
            converted_lines.append('')  # テーブルの最後に改行を追加

        # テーブルや特別な記法の行を無視する
        if inside_table or line.strip().startswith('<div class="style-'):
            # 開いているリストがある場合は閉じる
            while list_stack:
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            converted_lines.append(line)
            continue

        # 行の先頭と末尾の空白を除去し、インデントレベルを計算
        stripped_line = line.strip()
        indent_level = len(line) - len(line.lstrip())

        # 現在の行が番号付きリストのアイテムで始まる場合
        if stripped_line and stripped_line[0].isdigit() and stripped_line.find('.') != -1:
            # リストスタックが空（新しいリストの開始）または現在のインデントレベルが直前のリストよりも深い場合
            if not list_stack or indent_level > list_stack[-1][1]:
                # リストスタックに新しいリスト（ol）を追加し、HTMLに<ol>タグを追加
                list_stack.append(('ol', indent_level))
                converted_lines.append('<ol>')
            else:
                # 直前のリストよりも浅いインデントレベルの場合、直前のリストを閉じる
                while list_stack and indent_level < list_stack[-1][1]:
                    converted_lines.append('</li>')
                    converted_lines.append('</{}>'.format(list_stack.pop()[0]))
                # 現在のインデントレベルが直前のリストと同じ場合、直前のリストアイテムを閉じる
                if list_stack and indent_level == list_stack[-1][1]:
                    converted_lines.append('</li>')

            # リストアイテムをHTMLに追加
            converted_lines.append(f'<li>{stripped_line[stripped_line.index(".") + 1:].strip()}')
        else:
            # 空白行、見出しの行、またはインデントレベルが減少した場合、直前のリストを閉じる
            while list_stack and (not stripped_line or stripped_line.startswith('#') or indent_level < list_stack[-1][1]):
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            # 現在の行が空でない場合、その行をHTMLに追加
            if stripped_line:
                converted_lines.append(line)

    # ループ終了後、残っている開いているリストをすべて閉じる
    while list_stack:
        converted_lines.append('</li>')
        converted_lines.append('</{}>'.format(list_stack.pop()[0]))

    # 変換されたHTMLを改行で結合して返す
    return '\n'.join(converted_lines)

def convert_unordered_list(md_content):
    """
    番号なしリストを変換する関数。
    Args:
        md_content (str): Markdownの内容。
    Returns:
        str: 変換されたHTMLの内容。
    """
    # Markdownの内容を各行に分割
    lines = md_content.split('\n')
    # 変換後のHTMLの各行を格納するリスト
    converted_lines = []
    # リストのスタック（開いているリストの情報を追跡）
    list_stack = []
    # テーブルの状態を追跡するフラグ
    inside_table = False

    # 各行に対して処理を行う
    for line in lines:
        # テーブルの開始行を検出する
        if line.strip().startswith('|'):
            inside_table = True

        # テーブルの終了行を検出する
        if inside_table and not line.strip().startswith('|'):
            inside_table = False
            converted_lines.append('')  # テーブルの最後に改行を追加

        # テーブルや特別な記法の行を無視する
        if inside_table or line.strip().startswith('<div class="style-'):
            # 開いているリストがある場合は閉じる
            while list_stack:
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            converted_lines.append(line)
            continue

        # 行の先頭と末尾の空白を除去し、インデントレベルを計算
        stripped_line = line.strip()
        indent_level = len(line) - len(line.lstrip())

        # 現在の行が番号なしリストのアイテムで始まる場合
        if stripped_line.startswith('- ') or stripped_line.startswith('* '):
            # リストスタックが空（新しいリストの開始）または現在のインデントレベルが直前のリストよりも深い場合
            if not list_stack or indent_level > list_stack[-1][1]:
                # リストスタックに新しいリスト（ul）を追加し、HTMLに<ul>タグを追加
                list_stack.append(('ul', indent_level))
                converted_lines.append('<ul>')
            else:
                # 直前のリストよりも浅いインデントレベルの場合、直前のリストを閉じる
                while list_stack and indent_level < list_stack[-1][1]:
                    converted_lines.append('</{}>'.format(list_stack.pop()[0]))
                # 現在のインデントレベルが直前のリストと同じ場合、直前のリストアイテムを閉じる
                if list_stack and indent_level == list_stack[-1][1]:
                    converted_lines.append('</li>')

            # リストアイテムをHTMLに追加
            converted_lines.append(f'<li>{stripped_line[2:]}')
        else:
            # 空白行、見出しの行、またはインデントレベルが減少した場合、直前のリストを閉じる
            while list_stack and (not stripped_line or stripped_line.startswith('#') or indent_level < list_stack[-1][1]):
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            # 現在の行が空でない場合、その行をHTMLに追加
            if stripped_line:
                converted_lines.append(line)

    # ループ終了後、残っている開いているリストをすべて閉じる
    while list_stack:
        converted_lines.append('</li>')
        converted_lines.append('</{}>'.format(list_stack.pop()[0]))

    # 変換されたHTMLを改行で結合して返す
    return '\n'.join(converted_lines)

def convert_info_warn_alert_blocks(html_content, icon_dir):
    """
    info、warn、alertのブロックを適切なHTMLに変換する関数。

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
        elif block_type == 'alert':
            icon_path = os.path.join(icon_dir, 'alert.svg')
            style = 'style-alert'
        
        # SVGファイルを読み込んでアイコンを生成
        with open(icon_path, 'r') as file:
            icon = file.read()
        
        # 複数行の場合は<br>タグを追加
        content = content.replace('\n', '<br>')
        
        return f'<div class="{style}">{icon}<p>{content}</p></div>'
    
    pattern = re.compile(r':::note (info|warn|alert)\s*(.*?):::(?!:)', re.DOTALL)
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
    template_path = os.path.join(os.path.dirname(__file__), 'template_content.html')
    template = read_file(template_path)
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
    return generate_html_content("Index", f"<div class='root'><div class='content'><h1>Files</h1><ul>{index_content}</ul></div></div>")

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