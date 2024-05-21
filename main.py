# docフォルダ配下にあるすべての.mdファイルを取得
# それぞれのファイルをHTMLに変換してpublicフォルダに保存
# 例: hoge.md -> hoge.html
# index.htmlはそれぞれの.mdファイルをリンクにして表示する
import os
import sys
import markdown

# コマンドライン引数からdocフォルダのパスを取得
if len(sys.argv) < 3:
    print("使用法: python script.py <docフォルダのパス> <publicフォルダのパス>")
    sys.exit(1)

doc_dir = sys.argv[1]

# publicフォルダのパス
public_dir = sys.argv[2]

# cssフォルダのパス
css_dir = os.path.join(public_dir, "css")

# publicフォルダとcssフォルダが存在しない場合は作成
if not os.path.exists(public_dir):
    os.makedirs(public_dir)
if not os.path.exists(css_dir):
    os.makedirs(css_dir)

# index.htmlの内容を格納する文字列
global index_html
index_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Markdown Files</title>
    <link rel="stylesheet" type="text/css" href="css/base.css">
</head>
<body>
    <h1>Markdown Files</h1>
    <ul>
"""

# 再帰的にディレクトリを探索し、.mdファイルを処理する関数
def process_directory(dir_path):
    global index_html
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        
        # ディレクトリの場合は再帰的に探索
        if os.path.isdir(item_path):
            process_directory(item_path)
        
        # .mdファイルの場合は処理
        elif item.endswith(".md"):
            # .mdファイルの内容を読み込む
            with open(item_path, "r", encoding="utf-8") as file:
                md_content = file.read()
            
            # Markdownを変換してHTMLを生成（コメントを無視する拡張機能を追加）
            html_content = markdown.markdown(md_content, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'])
            
            # HTMLファイル名を生成
            html_file = os.path.splitext(item)[0] + ".html"
            
            # HTMLファイルのフルパスを取得
            html_path = os.path.join(public_dir, html_file)
            
            # 自動生成されたHTMLファイルにbase.cssを読み込むコードを追加
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{os.path.splitext(item)[0]}</title>
    <link rel="stylesheet" type="text/css" href="css/base.css">
</head>
<body>
    {html_content}
</body>
</html>
"""
            
            # HTMLファイルを保存
            with open(html_path, "w", encoding="utf-8") as file:
                file.write(html_content)
            
            # index.htmlにリンクを追加
            relative_path = os.path.relpath(item_path, doc_dir)
            link_text = os.path.splitext(relative_path)[0].replace("\\", "/")
            index_html += f"      <li><a href='{html_file}'>{link_text}</a></li>\n"

# docディレクトリを再帰的に探索
process_directory(doc_dir)

# index.htmlの終了タグを追加
index_html += """
    </ul>
</body>
</html>
"""

# index.htmlのフルパスを取得
index_path = os.path.join(public_dir, "index.html")

# index.htmlを保存
with open(index_path, "w", encoding="utf-8") as file:
    file.write(index_html)

print("変換が完了しました。")