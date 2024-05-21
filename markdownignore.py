import os
import fnmatch

def read_markdownignore(doc_dir):
    """
    .markdownignoreファイルを読み込む関数。

    Args:
        doc_dir (str): docフォルダのパス。

    Returns:
        list: 無視するパターンのリスト。
    """
    markdownignore_path = os.path.join(doc_dir, ".markdownignore")
    if os.path.exists(markdownignore_path):
        with open(markdownignore_path, "r", encoding="utf-8") as file:
            return file.read().splitlines()
    return []

def is_ignored(path, ignore_patterns):
    """
    指定されたパスが無視するパターンにマッチするかどうかを判定する関数。

    Args:
        path (str): 判定するパス。
        ignore_patterns (list): 無視するパターンのリスト。

    Returns:
        bool: 無視する場合はTrue、無視しない場合はFalse。
    """
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False