from directory_utils import generate_and_save_index_html,MarkdownProcessor
from infrastructure.cli.command_line import validate_command_line_arguments
from infrastructure.common.directory import Directory
from infrastructure.common.copy import Copy
from html_utils import generate_pygments_css
from markdownignore import read_markdownignore
import os

def main():
    """
    メイン関数。コマンドライン引数の処理、出力先の作成、docディレクトリの探索、index.htmlの生成と保存を行う。
    """
    doc_dir, output_dir,index_only,no_index,no_style, anchor_links  = validate_command_line_arguments()

    # 出力先のディレクトリを作成
    Directory(output_dir).create_required_directories()

    # iconディレクトリとcssディレクトリをコピー
    copy = Copy(output_dir)
    copy.copy_icon_directory()
    # --no-styleオプションが指定された場合はCSSのコピーをスキップ
    if not no_style:
        copy.copy_css_directory()
    else:
        print('CSSのコピーをスキップしました。')
    
    ignore_patterns = read_markdownignore(doc_dir)

    # --index-onlyオプションが指定された場合はindex.htmlのみ生成
    if index_only:
        generate_and_save_index_html(doc_dir, output_dir, ignore_patterns, anchor_links)
        print("index.htmlの生成が完了しました。")
        return
    
    icon_dir = os.path.join(output_dir, 'icon')
    # process_markdown_files_in_directory(doc_dir, output_dir, icon_dir, ignore_patterns, anchor_links)
    MarkdownProcessor(doc_dir, output_dir, icon_dir, ignore_patterns, anchor_links).process_markdown_files()

    # --no-indexオプションが指定された場合はindex.htmlを生成しない
    if no_index:
        print('index.htmlの生成をスキップしました。')
    else:
        generate_and_save_index_html(doc_dir, output_dir, ignore_patterns)

    # Pygmentsのスタイルを使用してハイライト用のCSSファイルを生成
    generate_pygments_css(output_dir)
    print("変換が完了しました。")

if __name__ == "__main__":
    main()