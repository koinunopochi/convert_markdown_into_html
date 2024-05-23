import os

# TODO：目的があいまいなため、早いうちにファイル名を変更する。
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