import os

class Directory:
    def __init__(self, output_dir):
        self.output_dir = output_dir
    
    def create(self):
        """
        ディレクトリを作成するパブリックメソッド。
        """
        os.makedirs(self.output_dir, exist_ok=True)

    def create_required_directories(self):
        """
        必須の出力先ディレクトリを作成するパブリックメソッド。
        """
        self._create_output_root_directory(self.output_dir)
        self._create_output_css_directory()
    
    def _create_output_root_directory(self, output_dir=None):
        """
        出力先のディレクトリを作成するプライベートメソッド。
        """
        os.makedirs(output_dir, exist_ok=True)
    
    def _create_output_css_directory(self):
        """
        出力先のcssディレクトリを作成するプライベートメソッド。
        """
        css_dir = os.path.join(self.output_dir, "css")
        os.makedirs(css_dir, exist_ok=True)