import re
import unicodedata
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import os

from infrastructure.common.file import File

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

    # `で囲まれた部分を変換
    html_content = convert_backquotes(html_content)

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

def convert_backquotes(md_content):
    """
    `で囲まれた部分を変換する関数。ただし、コードブロック内は無視する。
    Args:
        md_content (str): Markdownの内容。
    Returns:
        str: 変換されたMarkdownの内容。
    """
    # コードブロックを検出する正規表現パターン
    code_block_pattern = r'```[\s\S]*?```'
    
    # コードブロックを一時的に置き換える
    code_blocks = []
    def replace_code_block(match):
        code_blocks.append(match.group(0))
        return f'{{CODE_BLOCK_{len(code_blocks)-1}}}'
    md_content = re.sub(code_block_pattern, replace_code_block, md_content)
    
    # `で囲まれた部分を探す正規表現パターン
    pattern = r'`([^`]+)`'
    
    # `で囲まれた部分を<span>タグに置換する
    converted_content = re.sub(pattern, r'<span class="backquote">\1</span>', md_content)
    
    # コードブロックを元に戻す
    for i, code_block in enumerate(code_blocks):
        converted_content = converted_content.replace(f'{{CODE_BLOCK_{i}}}', code_block)
    
    return converted_content

# TODO:あまりにも汚いコードなのでリファクタリングする
def convert_nested_lists(md_content):
    """
    ネストされたリストを適切に処理する関数。

    Args:
        md_content (str): Markdownの内容。

    Returns:
        str: 変換されたMarkdownの内容。
    """
    # コードブロックをプレースホルダーに置き換える
    code_blocks = re.findall(r'```.*?```', md_content, flags=re.DOTALL)
    for i, block in enumerate(code_blocks):
        md_content = md_content.replace(block, f"<!-- CODE_BLOCK_{i} -->")

    # 番号なしリストを変換
    md_content = convert_unordered_list(md_content)
    # 番号付きリストを変換
    md_content = convert_ordered_list(md_content)

    # プレースホルダーを元のコードブロックに戻す
    for i, block in enumerate(code_blocks):
        md_content = md_content.replace(f"<!-- CODE_BLOCK_{i} -->", block)

    return md_content

def convert_ordered_list(md_content):
    """
    番号付きリストを変換する関数。

    Args:
        md_content (str): Markdownの内容。

    Returns:
        str: 変換されたHTMLの内容。
    """
    lines = md_content.split('\n')
    converted_lines = []
    list_stack = []
    inside_table = False

    for line in lines:
        if line.strip().startswith('|'):
            inside_table = True
        if inside_table and not line.strip().startswith('|'):
            inside_table = False
            converted_lines.append('')
        if inside_table or line.strip().startswith('<div class="style-'):
            while list_stack:
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            converted_lines.append(line)
            continue

        stripped_line = line.strip()
        indent_level = len(line) - len(line.lstrip())

        if stripped_line and stripped_line[0].isdigit() and stripped_line.find('.') != -1:
            if not list_stack or indent_level > list_stack[-1][1]:
                list_stack.append(('ol', indent_level))
                converted_lines.append('<ol>')
            else:
                while list_stack and indent_level < list_stack[-1][1]:
                    converted_lines.append('</li>')
                    converted_lines.append('</{}>'.format(list_stack.pop()[0]))
                if list_stack and indent_level == list_stack[-1][1]:
                    converted_lines.append('</li>')
            converted_lines.append(f'<li>{stripped_line[stripped_line.index(".") + 1:].strip()}')
        else:
            while list_stack and (not stripped_line or stripped_line.startswith('#') or indent_level < list_stack[-1][1]):
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            if stripped_line:
                converted_lines.append(line)

    while list_stack:
        converted_lines.append('</li>')
        converted_lines.append('</{}>'.format(list_stack.pop()[0]))

    return '\n'.join(converted_lines)

def convert_unordered_list(md_content):
    """
    番号なしリストを変換する関数。

    Args:
        md_content (str): Markdownの内容。

    Returns:
        str: 変換されたHTMLの内容。
    """
    lines = md_content.split('\n')
    converted_lines = []
    list_stack = []
    inside_table = False

    for line in lines:
        if line.strip().startswith('|'):
            inside_table = True
        if inside_table and not line.strip().startswith('|'):
            inside_table = False
            converted_lines.append('')
        if inside_table or line.strip().startswith('<div class="style-'):
            while list_stack:
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            converted_lines.append(line)
            continue

        stripped_line = line.strip()
        indent_level = len(line) - len(line.lstrip())

        if stripped_line.startswith('- ') or stripped_line.startswith('* '):
            if not list_stack or indent_level > list_stack[-1][1]:
                list_stack.append(('ul', indent_level))
                converted_lines.append('<ul>')
            else:
                while list_stack and indent_level < list_stack[-1][1]:
                    converted_lines.append('</{}>'.format(list_stack.pop()[0]))
                if list_stack and indent_level == list_stack[-1][1]:
                    converted_lines.append('</li>')
            converted_lines.append(f'<li>{stripped_line[2:]}')
        else:
            while list_stack and (not stripped_line or stripped_line.startswith('#') or indent_level < list_stack[-1][1]):
                converted_lines.append('</li>')
                converted_lines.append('</{}>'.format(list_stack.pop()[0]))
            if stripped_line:
                converted_lines.append(line)

    while list_stack:
        converted_lines.append('</li>')
        converted_lines.append('</{}>'.format(list_stack.pop()[0]))

    return '\n'.join(converted_lines)


def convert_info_warn_alert_blocks(html_content, icon_dir):
    """
    info、warn、alertのブロックを適切なHTMLに変換する関数。ただし、<code>タグ内は無視する。
    
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
    
    # <code>タグを検出する正規表現パターン
    code_block_pattern = r'<code>.*?</code>'

    # <code>タグ内の内容を一時的にプレースホルダーに置き換える
    code_blocks = re.findall(code_block_pattern, html_content, flags=re.DOTALL)
    for i, block in enumerate(code_blocks):
        html_content = html_content.replace(block, f"<!-- CODE_BLOCK_{i} -->")

    # :::note ブロックを置換
    html_content = re.sub(r':::note (info|warn|alert)\s*(.*?):::', replace_block, html_content, flags=re.DOTALL)

    # プレースホルダーを元のコードブロックに戻す
    for i, block in enumerate(code_blocks):
        html_content = html_content.replace(f"<!-- CODE_BLOCK_{i} -->", block)

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
    template = File(template_path).read()
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