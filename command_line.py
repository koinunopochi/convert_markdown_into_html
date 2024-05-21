import sys

def validate_command_line_arguments():
    """
    コマンドライン引数を検証する関数。

    Returns:
        tuple: (doc_dir, output_dir, index_only, no_index, no_style, anchor_links) コマンドライン引数が有効な場合はdocフォルダのパス、出力先のパス、index_onlyフラグの値、no_indexフラグの値、no_styleフラグの値、anchor_linksフラグの値を返す。
    """
    if "--help" in sys.argv:
        print_help()
        sys.exit(0)
    
    if len(sys.argv) < 3:
        print("使用法: python script.py <docフォルダのパス> <出力先> [--index-only] [--no-index] [--no-style] [--anchor-links]")
        sys.exit(1)

    doc_dir = sys.argv[1]
    output_dir = sys.argv[2]
    index_only = False
    no_index = False
    no_style = False
    anchor_links = False

    if "--index-only" in sys.argv:
        index_only = True

    if "--no-index" in sys.argv:
        no_index = True

    if "--no-style" in sys.argv:
        no_style = True

    if "--anchor-links" in sys.argv:
        anchor_links = True

    return doc_dir, output_dir, index_only, no_index, no_style, anchor_links

def print_help():
    """
    ヘルプメッセージを表示する関数。
    """
    help_message = """
使用法: python script.py <docフォルダのパス> <出力先> [オプション]

オプション:
--index-only  インデックスファイルのみを生成する
--no-index    インデックスファイルを生成しない
--no-style    スタイルファイルをコピーしない
--anchor-links  ページ内リンクを生成する
--help        ヘルプメッセージを表示する
"""
    print(help_message)