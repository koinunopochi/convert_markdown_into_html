import sys

def validate_command_line_arguments():
    """
    コマンドライン引数を検証する関数。

    Returns:
        tuple: (doc_dir, output_dir) コマンドライン引数が有効な場合はdocフォルダのパスと出力先のパスを返す。
    """
    if len(sys.argv) < 3:
        print("使用法: python script.py <docフォルダのパス> <出力先>")
        sys.exit(1)
    doc_dir = sys.argv[1]
    output_dir = sys.argv[2]
    return doc_dir, output_dir