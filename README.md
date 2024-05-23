# Markdown to HTML Converter

このプロジェクトは、Markdown ファイルを HTML ファイルに変換する Python スクリプトです。

## 動作環境

- Python 3.9.13


## 使用方法

1. このリポジトリをクローンまたはダウンロードします。

```bash
git clone https://github.com/koinunopochi/convert_markdown_into_html.git
cd convert_markdown_into_html
```

2. 必要な Python パッケージをインストールします。

```bash
pip install -r requirements.txt
```

3. setup.pyのあるディレクトリで実行し、setupします。

```bash
 pip install -e .
```

1. 以下のコマンドでスクリプトを実行します。

```bash
mkToHtml <docフォルダのパス> <出力先> [オプション]
```

- `docフォルダのパス`: Markdown ファイルが格納されているフォルダのパスを指定します。
- `出力先`: 変換後の HTML ファイルを出力するフォルダのパスを指定します。
- オプション:
  - `--index-only`: インデックスファイルのみを生成します。
  - `--no-index`: インデックスファイルを生成しません。
  - `--no-style`: スタイルファイルをコピーしません。
  - `--anchor-links`: ページ内リンクを生成します。
  - `--help`: ヘルプメッセージを表示します。

例:

```bash
mkToHtml ${pwd}\sample\ ${pwd}\.sample-nginx\public --anchor-links
```

4. 変換が完了しました。

## 機能

- Markdown ファイルを HTML ファイルに変換します。
- インデックスファイルを生成し、各 HTML ファイルへのリンクを提供します。
- スタイルファイルを自動的にコピーし、HTML ファイルに適用します。
- ページ内リンクを生成し、目次からのナビゲーションを可能にします。
- カスタムブロック（info、warn、alert）をサポートし、視覚的な強調表示を提供します。
- `.markdownignore`ファイルに記載することで、変換を無視することができます。

## 制限事項・注意事項

- 短時間で作成しているため、異常終了する可能性があります。
  - 適宜修正していきますので、issue よりご連絡ください。

## ライセンス

このプロジェクトは、GPL-3.0 ライセンスの下で公開されています。詳細については、[LICENSE](LICENSE.md)ファイルを参照してください。

## 基本的なMarkdown記法

### 見出し
```markdown
# 見出し1
## 見出し2
### 見出し3
#### 見出し4
##### 見出し5
###### 見出し6
```
# 見出し1
## 見出し2
### 見出し3
#### 見出し4
##### 見出し5
###### 見出し6

### リスト

#### 番号なしリスト

```markdown
- アイテム1
  - サブアイテム1
  - サブアイテム2
- アイテム2
- アイテム3
```

- アイテム1
  - サブアイテム1
  - サブアイテム2
- アイテム2
- アイテム3


#### 番号付きリスト

```markdown
1. アイテム1
2. アイテム2
3. アイテム3
   1. サブアイテム1
   2. サブアイテム2
4. アイテム4
```

1. アイテム1
2. アイテム2
3. アイテム3
   1. サブアイテム1
   2. サブアイテム2
4. アイテム4


### 強調

```markdown
**太字**
*斜体 shatai*
~~打ち消し線~~
```

**太字**
*斜体 shatai*
~~打ち消し線~~

:::note warn
残念ながら、打消し線については現在サポートしておりません
:::


### リンク

```markdown
[リンクのテキスト](https://www.example.com)
```

[リンクのテキスト](https://www.example.com)


### 画像

```markdown
![代替テキスト](https://www.example.com/image.jpg)
```

![代替テキスト](https://www.example.com/image.jpg)


### コードブロック

```markdown
  ```言語名
  コードの内容
  ```
```

```言語名
コードの内容
```

例:
```markdown
  ```python
  def hello_world():
      print("Hello, World!")
  ```
```

```python
def hello_world():
    print("Hello, World!")
```

### 引用

```markdown
> これは引用です。
```

> これは引用です。

### 表

```markdown
| 左寄せ | 中央寄せ | 右寄せ |
| :------- | :-------: | -------: |
| セル1   | セル2   | セル3   |
| セル4   | セル5   | セル6   |
```

| 左寄せ | 中央寄せ | 右寄せ |
| :------- | :-------: | -------: |
| セル1   | セル2   | セル3   |
| セル4   | セル5   | セル6   |


## 特別な記法

```markdown
:::note info
これは情報メッセージです。
:::
```

:::note info
これは情報メッセージです。
:::

```markdown
:::note warn
これは警告メッセージです。
:::
```

:::note warn
これは警告メッセージです。
:::

```markdown
:::note alert
これは警告メッセージです。
:::
```

:::note alert
これは警告メッセージです。
:::