# docフォルダ配下にあるすべての.mdファイルを取得
# それぞれのファイルをHTMLに変換してpublicフォルダに保存
# 例: hoge.md -> hoge.html
# index.htmlはそれぞれの.mdファイルをリンクにして表示する
import os
import sys
import markdown
from file import read_file, save_file

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

def process_directory(dir_path, output_dir):
    """
    ディレクトリを再帰的に探索し、.mdファイルを処理する関数。

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
            index_links += process_directory(item_path, output_dir)
        else:
            if not item.endswith(".md"):
                continue
            
            md_content = read_file(item_path)
            html_content = convert_markdown_to_html(md_content)
            html_file = os.path.splitext(item)[0] + ".html"
            html_path = os.path.join(output_dir, html_file)
            
            save_file(html_path, generate_html_content(os.path.splitext(item)[0], html_content))
            
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
    
    # docディレクトリを再帰的に探索
    index_content = process_directory(doc_dir, output_dir)
    
    # index.htmlを生成して保存
    index_path = os.path.join(output_dir, "index.html")
    save_file(index_path, generate_index_html(index_content))
    
    print("変換が完了しました。")

if __name__ == "__main__":
    main()