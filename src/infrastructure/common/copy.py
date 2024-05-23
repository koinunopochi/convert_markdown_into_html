import os
import shutil

class Copy:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def copy_icon_directory(self):
        """
        iconディレクトリをコピーするパブリックメソッド。
        """
        output_dir = self.output_dir
        print(output_dir)
        style_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "style")
        icon_src_dir = os.path.join(style_dir, "icon")
        icon_dest_dir = os.path.join(output_dir, "icon")
        print(icon_src_dir)
        if os.path.exists(icon_src_dir):
            shutil.copytree(icon_src_dir, icon_dest_dir, dirs_exist_ok=True)

    def copy_css_directory(self):
        """
        iconディレクトリをコピーするパブリックメソッド。
        """
        output_dir = self.output_dir
        style_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "style")
        css_src_dir = os.path.join(style_dir, "css")
        css_dest_dir = os.path.join(output_dir, "css")
        if os.path.exists(css_src_dir):
            shutil.copytree(css_src_dir, css_dest_dir, dirs_exist_ok=True)