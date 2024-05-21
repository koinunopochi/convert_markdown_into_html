# Markdown to HTML Converter

このプロジェクトは、Markdownファイルを HTMLファイルに変換するPythonスクリプトです。

## 動作環境

<!-- 動作環境に関する情報を記載してください -->
- Python X.X.X
- 必要なPythonパッケージ:
  - markdown
  - pygments

## 使用方法

<!-- 使用方法を記載してください -->
1. このリポジトリをクローンまたはダウンロードします。
2. 必要なPythonパッケージをインストールします。
```bash
pip install -r requirements.txt
```
3. 以下のコマンドでスクリプトを実行します。
```bash
python script.py <docフォルダのパス> <出力先> [オプション]
```

- `<docフォルダのパス>`: Markdownファイルが格納されているフォルダのパスを指定します。
- `<出力先>`: 変換後のHTMLファイルを出力するフォルダのパスを指定します。
- オプション:
  - `--index-only`: インデックスファイルのみを生成します。
  - `--no-index`: インデックスファイルを生成しません。
  - `--no-style`: スタイルファイルをコピーしません。
  - `--anchor-links`: ページ内リンクを生成します。
  - `--help`: ヘルプメッセージを表示します。

## 機能

<!-- 主な機能や特徴を記載してください -->
- Markdownファイルを HTMLファイルに変換します。
- インデックスファイルを生成し、各HTMLファイルへのリンクを提供します。
- スタイルファイルを自動的にコピーし、HTMLファイルに適用します。
- ページ内リンクを生成し、目次からのナビゲーションを可能にします。
- カスタムブロック（info、warn、alert）をサポートし、視覚的な強調表示を提供します。

## 制限事項・注意事項

<!-- 制限事項や注意点を記載してください。情報が不足している場合は、XXXと記載してください。 -->
- 短時間で作成しているため、異常終了する可能性があります
  - 適宜修正していきますので、issueよりご連絡ください

## ライセンス

<!-- ライセンス情報を記載してください。GPLライセンスを使用する場合は以下のように記載できます。 -->
このプロジェクトは、GPL-3.0ライセンスの下で公開されています。詳細については、[LICENSE](LICENSE.md)ファイルを参照してください。