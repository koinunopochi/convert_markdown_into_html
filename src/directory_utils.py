import os
from infrastructure.common.file import File
from html_utils import convert_markdown_to_html, generate_html_content, generate_index_html
from markdownignore import is_ignored

# TODO:ネストは１つまでにする
def process_markdown_files_in_directory(doc_dir, output_dir, icon_dir, ignore_patterns,anchor_links):
    """
    ディレクトリ内の.mdファイルを処理する関数。

    Args:
        doc_dir (str): 探索するディレクトリのパス。
        output_dir (str): 出力先のディレクトリのパス。
        icon_dir (str): アイコンファイルのディレクトリパス。
        ignore_patterns (list): 無視するパターンのリスト。
    """
    for root, dirs, files in os.walk(doc_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, doc_dir)
                if not is_ignored(relative_path, ignore_patterns):
                  convert_markdown_file_to_html(file_path, output_dir, icon_dir,anchor_links)

# TODO；Save fileの処理を移動する
def generate_and_save_index_html(doc_dir, output_dir, ignore_patterns):
    """
    index.htmlを生成して保存する関数。

    Args:
        doc_dir (str): 探索するディレクトリのパス。
        output_dir (str): 出力先のディレクトリのパス。
        ignore_patterns (list): 無視するパターンのリスト。
    """
    index_content = generate_index_links_from_directory(doc_dir, output_dir, ignore_patterns)
    index_path = os.path.join(output_dir, "index.html")
    File(index_path).save(generate_index_html(index_content))

# TODO；Save fileの処理を移動する
def convert_markdown_file_to_html(file_path, output_dir, icon_dir,anchor_links):
    """
    .mdファイルをHTMLファイルに変換して保存する関数。

    Args:
        file_path (str): 変換するMarkdownファイルのパス。
        output_dir (str): 出力先のディレクトリのパス。
    """
    md_content = File(file_path).read()
    html_content = convert_markdown_to_html(md_content, icon_dir,anchor_links)
    html_file = os.path.splitext(os.path.basename(file_path))[0] + ".html"
    html_path = os.path.join(output_dir, html_file)
    File(html_path).save(generate_html_content(os.path.splitext(os.path.basename(file_path))[0], html_content))


# TODO:ネストは１つまでにする
def generate_index_links_from_directory(dir_path, output_dir, ignore_patterns, level=0):
    """
    ディレクトリ内の.mdファイルからindex.htmlに追加するリンクのHTMLを生成する関数。

    Args:
        dir_path (str): 探索するディレクトリのパス。
        output_dir (str): 出力先のディレクトリのパス。
        ignore_patterns (list): 無視するパターンのリスト。
        level (int): 階層レベル（デフォルトは0）。

    Returns:
        str: index.htmlに追加するリンクのHTML。
    """
    index_links = ""
    indent = "  " * level  # インデントを表現するための空白文字列

    # ディレクトリ名を表示
    index_links += f"{indent}<li>{os.path.basename(dir_path)}/</li>\n"
    index_links += f"{indent}<ul>\n"

    for item in os.listdir(dir_path):
        
        item_path = os.path.join(dir_path, item)
        relative_path = os.path.relpath(item_path, dir_path)

        if not is_ignored(relative_path, ignore_patterns):

          if os.path.isdir(item_path):
              # 再帰的にサブディレクトリを探索
              index_links += generate_index_links_from_directory(item_path, output_dir, ignore_patterns, level + 1)

          elif item.endswith(".md"):
              html_file = File(item_path).generate_html_file_name()
              relative_path = generate_relative_path(item_path, dir_path)
              link_text = generate_link_text(relative_path)
              index_links += f"{indent}  <li><a href='{html_file}'>{link_text}</a></li>\n"

    index_links += f"{indent}</ul>\n"
    return index_links

# ################ 相対パスやリンクテキストの生成に関する関数 ################
# TODO:移動する
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