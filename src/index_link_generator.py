from markdownignore import is_ignored
import os
from infrastructure.common.file import File
from utils import generate_relative_path, generate_link_text

class IndexLinkGenerator:
    def __init__(self, output_dir, ignore_patterns):
        self.output_dir = output_dir
        self.ignore_patterns = ignore_patterns

    def generate_index_links(self, dir_path, level=0):
        """
        ディレクトリ内の.mdファイルからindex.htmlに追加するリンクのHTMLを生成するメソッド。
        Args:
            dir_path (str): 探索するディレクトリのパス。
            level (int): 階層レベル（デフォルトは0）。
        Returns:
            str: index.htmlに追加するリンクのHTML。
        """
        index_links = ""
        indent = self._generate_indent(level)

        index_links += self._generate_directory_name(dir_path, indent)
        index_links += self._generate_opening_ul_tag(indent)

        for item in os.listdir(dir_path):
            item_path = os.path.join(dir_path, item)
            relative_path = os.path.relpath(item_path, dir_path)

            if not is_ignored(relative_path, self.ignore_patterns):
                index_links += self._generate_item_link(item_path, dir_path, level, indent)

        index_links += self._generate_closing_ul_tag(indent)

        return index_links

    def _generate_indent(self, level):
        """
        インデントを生成するプライベートメソッド。
        """
        return " " * level

    def _generate_directory_name(self, dir_path, indent):
        """
        ディレクトリ名を生成するプライベートメソッド。
        """
        return f"{indent}<li>{os.path.basename(dir_path)}/</li>\n"

    def _generate_opening_ul_tag(self, indent):
        """
        開始の<ul>タグを生成するプライベートメソッド。
        """
        return f"{indent}<ul>\n"

    def _generate_closing_ul_tag(self, indent):
        """
        終了の</ul>タグを生成するプライベートメソッド。
        """
        return f"{indent}</ul>\n"

    def _generate_item_link(self, item_path, dir_path, level, indent):
        """
        アイテム（ディレクトリまたはファイル）のリンクを生成するプライベートメソッド。
        """
        if os.path.isdir(item_path):
            return self._generate_sub_directory_links(item_path, level + 1)
        elif item_path.endswith(".md"):
            return self._generate_markdown_file_link(item_path, dir_path, indent)
        else:
            return ""

    def _generate_sub_directory_links(self, sub_dir_path, level):
        """
        サブディレクトリ内のリンクを生成するプライベートメソッド。
        """
        sub_links = self.generate_index_links(sub_dir_path, level)
        return sub_links

    def _generate_markdown_file_link(self, item_path, dir_path, indent):
        """
        Markdownファイルのリンクを生成するプライベートメソッド。
        """
        html_file = File(item_path).generate_html_file_name()
        relative_path = generate_relative_path(item_path, dir_path)
        link_text = generate_link_text(relative_path)
        link = f"{indent} <li><a href='{html_file}'>{link_text}</a></li>\n"
        return link
