from directory_utils import process_markdown_files_in_directory, generate_and_save_index_html
from infrastructure.cli.command_line import validate_command_line_arguments
from file_utils import create_output_directories, copy_css, copy_icon
from html_utils import generate_pygments_css
from markdownignore import read_markdownignore
import os

def main():
    """
    メイン関数。コマンドライン引数の処理、出力先の作成、docディレクトリの探索、index.htmlの生成と保存を行う。
    """
    doc_dir, output_dir,index_only,no_index,no_style, anchor_links  = validate_command_line_arguments()

    create_output_directories(output_dir)
    copy_icon(output_dir)
    # --no-styleオプションが指定された場合はCSSのコピーをスキップ
    if not no_style:
        copy_css(output_dir)
    else:
        print('CSSのコピーをスキップしました。')
    
    ignore_patterns = read_markdownignore(doc_dir)

    # --index-onlyオプションが指定された場合はindex.htmlのみ生成
    if index_only:
        generate_and_save_index_html(doc_dir, output_dir, ignore_patterns, anchor_links)
        print("index.htmlの生成が完了しました。")
        return
    
    icon_dir = os.path.join(output_dir, 'icon')
    process_markdown_files_in_directory(doc_dir, output_dir, icon_dir, ignore_patterns, anchor_links)

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