import os
import shutil
# TODO：ファイル名を変更する

# TODO:クラス化する
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

# TODO:ファイルではないので、移動する
def create_output_directories(output_dir):
    """
    出力先のディレクトリとcssディレクトリを作成する関数。

    Args:
        output_dir (str): 出力先のディレクトリのパス。
    """
    os.makedirs(output_dir, exist_ok=True)
    css_dir = os.path.join(output_dir, "css")
    os.makedirs(css_dir, exist_ok=True)

# TODO:ファイルではないので、移動する
def copy_icon(output_dir):
    """
    styleディレクトリからiconディレクトリをコピーする関数。

    Args:
        output_dir (str): 出力先のディレクトリのパス。
    """
    style_dir = os.path.join(os.path.dirname(__file__), "style")
    
    icon_src_dir = os.path.join(style_dir, "icon")
    icon_dest_dir = os.path.join(output_dir, "icon")
    if os.path.exists(icon_src_dir):
        shutil.copytree(icon_src_dir, icon_dest_dir, dirs_exist_ok=True)

# TODO:ファイルではないので、移動する
def copy_css(output_dir):
    """
    styleディレクトリからcssディレクトリをコピーする関数。

    Args:
        output_dir (str): 出力先のディレクトリのパス。
    """
    style_dir = os.path.join(os.path.dirname(__file__), "style")

    css_src_dir = os.path.join(style_dir, "css")
    css_dest_dir = os.path.join(output_dir, "css")
    if os.path.exists(css_src_dir):
        shutil.copytree(css_src_dir, css_dest_dir, dirs_exist_ok=True)