import os
import sys
from file import read_file, save_file
from html_utils import convert_markdown_to_html, generate_html_content, generate_index_html

def process_file(file_path, output_dir):
    """
    .mdファイルを処理し、HTMLファイルを生成する関数。

    Args:
        file_path (str): 処理するファイルのパス。
        output_dir (str): 出力先のディレクトリのパス。
    """
    md_content = read_file(file_path)
    html_content = convert_markdown_to_html(md_content)
    html_file = os.path.splitext(os.path.basename(file_path))[0] + ".html"
    html_path = os.path.join(output_dir, html_file)
    save_file(html_path, generate_html_content(os.path.splitext(os.path.basename(file_path))[0], html_content))

def generate_index_links(dir_path, output_dir):
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
            index_links += generate_index_links(item_path, output_dir)
        elif item.endswith(".md"):
            html_file = os.path.splitext(item)[0] + ".html"
            relative_path = os.path.relpath(item_path, dir_path)
            link_text = os.path.splitext(relative_path)[0].replace("\\", "/")
            index_links += f"<li><a href='{html_file}'>{link_text}</a></li>\n"
    return index_links

def main():
    """
    メイン関数。コマンドライン引数の処理、出力先の作成、docディレクトリの探索、index.htmlの生成と保存を行う。
    """
    # コマンドライン引数からdocフォルダのパスと出力先を取得
    if len(sys.argv) < 3:
        print("使用法: python script.py <docフォルダのパス> <出力先>")
        sys.exit(1)
    doc_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # 出力先のフォルダとcssフォルダが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    css_dir = os.path.join(output_dir, "css")
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)

    # docディレクトリ内の.mdファイルを処理
    for root, dirs, files in os.walk(doc_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                process_file(file_path, output_dir)

    # index.htmlに追加するリンクのHTMLを生成
    index_content = generate_index_links(doc_dir, output_dir)

    # index.htmlを生成して保存
    index_path = os.path.join(output_dir, "index.html")
    save_file(index_path, generate_index_html(index_content))

    print("変換が完了しました。")

if __name__ == "__main__":
    main()