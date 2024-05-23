class File:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read(self):
        """
        ファイルを読み込むメソッド。
        
        Returns:
            str: ファイルの内容。
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            return file.read()
    
    def save(self, content):
        """
        ファイルを保存するメソッド。
        
        Args:
            content (str): 保存するファイルの内容。
        """
        with open(self.file_path, "w", encoding="utf-8") as file:
            file.write(content)