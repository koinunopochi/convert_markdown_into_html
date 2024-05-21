import sys

def validate_command_line_arguments():
    """
    コマンドライン引数を検証する関数。

    Returns:
        tuple: (doc_dir, output_dir, index_only) コマンドライン引数が有効な場合はdocフォルダのパス、出力先のパス、index_onlyフラグの値を返す。
    """
    if len(sys.argv) < 3:
        print("使用法: python script.py <docフォルダのパス> <出力先> [--index-only]")
        sys.exit(1)

    doc_dir = sys.argv[1]
    output_dir = sys.argv[2]
    index_only = False

    if len(sys.argv) > 3 and sys.argv[3] == "--index-only":
        index_only = True

    return doc_dir, output_dir, index_only