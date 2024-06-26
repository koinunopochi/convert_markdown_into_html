import os
from infrastructure.common.file import File
from html_utils import convert_markdown_to_html, generate_html_content, generate_index_html
from index_link_generator import IndexLinkGenerator
from markdownignore import is_ignored

# TODO:ネストは１つまでにする
class MarkdownProcessor:
    def __init__(self, doc_dir, output_dir, icon_dir, ignore_patterns, anchor_links):
        self.doc_dir = doc_dir
        self.output_dir = output_dir
        self.icon_dir = icon_dir
        self.ignore_patterns = ignore_patterns
        self.anchor_links = anchor_links

    def process_markdown_files(self):
        """
        ディレクトリ内の.mdファイルを処理するメソッド。
        """
        for root, dirs, files in os.walk(self.doc_dir):
            for file in files:
                self._setup_markdown_file(file, root)

    def _setup_markdown_file(self, file, root):
        """
        Markdownファイルを変換するためのセットアップを行うプライベートメソッド。
        """
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, self.doc_dir)
            self._convert_markdown_file(relative_path, file_path)

    def _convert_markdown_file(self, relative_path, file_path):
        """
        無視されないMarkdownファイルを変換するプライベートメソッド。
        """
        print(relative_path)
        # print(self.ignore_patterns)
        if not is_ignored(relative_path, self.ignore_patterns):
            convert_markdown_file_to_html(file_path,self.output_dir, self.icon_dir, self.anchor_links)


# TODO；Save fileの処理を移動する
def generate_and_save_index_html(doc_dir, output_dir, ignore_patterns):
    """
    index.htmlを生成して保存する関数。

    Args:
        doc_dir (str): 探索するディレクトリのパス。
        output_dir (str): 出力先のディレクトリのパス。
        ignore_patterns (list): 無視するパターンのリスト。
    """
    # index_content = generate_index_links_from_directory(doc_dir, output_dir, ignore_patterns)
    index_content = IndexLinkGenerator(output_dir, ignore_patterns).generate_index_links(doc_dir)
    index_path = os.path.join(output_dir, "index.html")
    File(index_path).save(generate_index_html(index_content))

# TODO；Save fileの処理を移動する
def convert_markdown_file_to_html(file_path, output_dir, icon_dir,anchor_links):
    """
    .mdファイルをHTMLファイルに変換して保存する関数。

    Args:
        file_path (str): 変換するMarkdownファイルのパス。
        output_dir (str): 出力先のディレクトリのパス。
    """
    md_content = File(file_path).read()
    html_content = convert_markdown_to_html(md_content, icon_dir,anchor_links)
    html_file = os.path.splitext(os.path.basename(file_path))[0] + ".html"
    html_path = os.path.join(output_dir, html_file)
    File(html_path).save(generate_html_content(os.path.splitext(os.path.basename(file_path))[0], html_content))