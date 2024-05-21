# file.py

def read_file(file_path):
    """
    ファイルを読み込む関数。

    Args:
        file_path (str): 読み込むファイルのパス。

    Returns:
        str: ファイルの内容。
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def save_file(file_path, content):
    """
    ファイルを保存する関数。

    Args:
        file_path (str): 保存するファイルのパス。
        content (str): 保存するファイルの内容。
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)