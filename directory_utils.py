import os
from file_utils import read_file, save_file
from html_utils import convert_markdown_to_html, generate_html_content, generate_index_html, generate_link_html

def process_markdown_files_in_directory(doc_dir, output_dir):
    """
    ディレクトリ内の.mdファイルを処理する関数。

    Args:
        doc_dir (str): 探索するディレクトリのパス。
        output_dir (str): 出力先のディレクトリのパス。
    """
    for root, dirs, files in os.walk(doc_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                convert_markdown_file_to_html(file_path, output_dir)

def generate_and_save_index_html(doc_dir, output_dir):
    """
    index.htmlを生成して保存する関数。

    Args:
        doc_dir (str): 探索するディレクトリのパス。
        output_dir (str): 出力先のディレクトリのパス。
    """
    index_content = generate_index_links_from_directory(doc_dir, output_dir)
    index_path = os.path.join(output_dir, "index.html")
    save_file(index_path, generate_index_html(index_content))

def convert_markdown_file_to_html(file_path, output_dir):
    """
    .mdファイルをHTMLファイルに変換して保存する関数。

    Args:
        file_path (str): 変換するMarkdownファイルのパス。
        output_dir (str): 出力先のディレクトリのパス。
    """
    md_content = read_file(file_path)
    html_content = convert_markdown_to_html(md_content)
    html_file = os.path.splitext(os.path.basename(file_path))[0] + ".html"
    html_path = os.path.join(output_dir, html_file)
    save_file(html_path, generate_html_content(os.path.splitext(os.path.basename(file_path))[0], html_content))

def generate_index_links_from_directory(dir_path, output_dir):
    """
    ディレクトリ内の.mdファイルからindex.htmlに追加するリンクのHTMLを生成する関数。

    Args:
        dir_path (str): 探索するディレクトリのパス。
        output_dir (str): 出力先のディレクトリのパス。

    Returns:
        str: index.htmlに追加するリンクのHTML。
    """
    index_links = ""
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        if os.path.isdir(item_path):
            index_links += generate_index_links_from_directory(item_path, output_dir)
        elif item.endswith(".md"):
            html_file = generate_html_file_name(item)
            relative_path = generate_relative_path(item_path, dir_path)
            link_text = generate_link_text(relative_path)
            index_links += generate_link_html(html_file, link_text)
    return index_links

def generate_html_file_name(item):
    """
    アイテム名からHTMLファイル名を生成する関数。

    Args:
        item (str): アイテム名。

    Returns:
        str: 生成されたHTMLファイル名。
    """
    return os.path.splitext(item)[0] + ".html"

def generate_relative_path(item_path, dir_path):
    """
    相対パスを生成する関数。

    Args:
        item_path (str): アイテムのパス。
        dir_path (str): ディレクトリのパス。

    Returns:
        str: 生成された相対パス。
    """
    return os.path.relpath(item_path, dir_path)

def generate_link_text(relative_path):
    """
    リンクテキストを生成する関数。

    Args:
        relative_path (str): 相対パス。

    Returns:
        str: 生成されたリンクテキスト。
    """
    return os.path.splitext(relative_path)[0].replace("\\", "/")