from directory_utils import process_markdown_files_in_directory, generate_and_save_index_html
from command_line import validate_command_line_arguments
from file_utils import create_output_directories
from html_utils import generate_pygments_css
import os

def main():
    """
    メイン関数。コマンドライン引数の処理、出力先の作成、docディレクトリの探索、index.htmlの生成と保存を行う。
    """
    doc_dir, output_dir,index_only = validate_command_line_arguments()

    create_output_directories(output_dir)
    # --index-onlyオプションが指定された場合はindex.htmlのみ生成
    if index_only:
        generate_and_save_index_html(doc_dir, output_dir)
        print("index.htmlの生成が完了しました。")
        return
    
    icon_dir = os.path.join(output_dir, 'icon')
    process_markdown_files_in_directory(doc_dir, output_dir, icon_dir)
    generate_and_save_index_html(doc_dir, output_dir)
    # Pygmentsのスタイルを使用してハイライト用のCSSファイルを生成
    generate_pygments_css(output_dir)
    print("変換が完了しました。")

if __name__ == "__main__":
    main()