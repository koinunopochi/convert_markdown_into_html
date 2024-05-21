# file.py
import os

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

def create_output_directories(output_dir):
    """
    出力先のディレクトリとcssディレクトリを作成する関数。

    Args:
        output_dir (str): 出力先のディレクトリのパス。
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    css_dir = os.path.join(output_dir, "css")
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)