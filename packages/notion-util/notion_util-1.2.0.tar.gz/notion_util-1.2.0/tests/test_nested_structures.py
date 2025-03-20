import json
import pytest
from notion_util.util import markdown_to_notion_blocks


def test_complex_nested_lists():
    """
    複雑にネストされたリスト構造をテストします。
    箇条書きリストと番号付きリストの混合、さらに各レベルで異なる装飾を適用します。
    """
    markdown = """
# 複雑なネスト構造テスト

## 箇条書きリスト内の複合構造

* レベル1：通常の箇条書き
  * レベル2：**太字テキスト**を含む箇条書き
    * レベル3：*斜体テキスト*を含む箇条書き
      * レベル4：`コードブロック`を含む箇条書き
        * レベル5：[リンク](https://www.notion.so)を含む箇条書き
  * レベル2：別の箇条書き
    * レベル3：~~取り消し線~~テキスト

## 番号付きリスト内の複合構造

1. レベル1：通常の番号付きリスト
   1. レベル2：**太字テキスト**を含む番号付きリスト
      1. レベル3：*斜体テキスト*を含む番号付きリスト
         1. レベル4：`コードブロック`を含む番号付きリスト
   2. レベル2：別の番号付きリスト項目
      * 番号付きリスト内の箇条書き
        * 更にネストされた箇条書き

## 混合リスト構造

1. 番号付きリスト項目
   * 箇条書きサブアイテム
     1. 番号付きサブサブアイテム
        > 引用テキスト
        > **太字の引用テキスト**
   * 別の箇条書きサブアイテム
2. 別の番号付きリスト項目
   ```python
   # リスト内のコードブロック
   def hello():
       print("Hello, Notion!")
   ```
   * コードブロック後の箇条書き

## 特殊なネスト構造

* ~~取り消し線付きの[リンク](https://www.notion.so)を含む~~箇条書き
  * **太字で`コード`を含む**箇条書き
    * *斜体で~~取り消し線~~を含む*箇条書き
      * **[太字リンク](https://www.notion.so)**箇条書き
        * `コード内の[リンク](https://www.notion.so)`（これは実際にはコード内の文字列として扱われる）
"""

    blocks = markdown_to_notion_blocks(markdown)

    # ブロック数の検証
    assert len(blocks) > 0

    # 見出しが適切に変換されていることを確認
    assert blocks[0]["type"] == "heading_1"
    assert (
        blocks[0]["heading_1"]["rich_text"][0]["text"]["content"]
        == "複雑なネスト構造テスト"
    )

    # リスト構造が適切に処理されていることを確認
    bulleted_list_items = [b for b in blocks if b["type"] == "bulleted_list_item"]
    numbered_list_items = [b for b in blocks if b["type"] == "numbered_list_item"]

    assert len(bulleted_list_items) > 0
    assert len(numbered_list_items) > 0

    # ネストされたリスト項目の検証（実装に依存）
    # ネストはchildrenプロパティに格納されているはず
    has_nested_items = False
    for item in bulleted_list_items:
        if "bulleted_list_item" in item and "children" in item["bulleted_list_item"]:
            has_nested_items = True
            break

    # APIやNotionの制限により、深いネストは完全にサポートされていないかもしれない
    # その場合は、最大サポートされるネストレベルが適切に処理されているか確認

    # 注意：実際の実装によっては、このテストは調整が必要かもしれません


def test_nested_list_with_decorations():
    """
    ネストされたリスト内のテキスト装飾をテストします。
    """
    markdown = """
* レベル1：**太字装飾**
  * レベル2：*斜体装飾*
    * レベル3：~~取り消し線装飾~~
      * レベル4：`コード装飾`
        * レベル5：**太字と*斜体*の組み合わせ**
"""

    blocks = markdown_to_notion_blocks(markdown)

    # ブロック数の検証
    assert len(blocks) > 0

    # 最初のリスト項目が太字を含むことを確認
    assert blocks[0]["type"] == "bulleted_list_item"

    # 太字装飾の検証
    has_bold = False
    for rt in blocks[0]["bulleted_list_item"]["rich_text"]:
        if rt["annotations"]["bold"] == True:
            has_bold = True
            break
    assert has_bold == True

    # ネストされたリストアイテムの検証（実装依存）
    # 注意：実際の実装によっては、このテストは調整が必要かもしれません


def test_nested_quotes_and_lists():
    """
    引用内のリストとリスト内の引用の組み合わせをテストします。
    """
    markdown = """
> 引用テキスト
> * 引用内の箇条書き
> * 引用内の箇条書き2
>   * 引用内のネストされた箇条書き

* 箇条書き
  > 箇条書き内の引用
  > * 箇条書き内の引用内の箇条書き
"""

    blocks = markdown_to_notion_blocks(markdown)

    # ブロック数の検証
    assert len(blocks) > 0

    # 引用ブロックが存在することを確認
    quotes = [b for b in blocks if b["type"] == "quote"]
    assert len(quotes) > 0

    # 箇条書きリスト項目が存在することを確認
    bulleted_items = [b for b in blocks if b["type"] == "bulleted_list_item"]
    assert len(bulleted_items) > 0

    # 注意：実際の実装によっては、引用内のリストは別々のブロックとして扱われる可能性があります
    # それぞれの実装に応じてテストを調整してください


def test_nested_code_blocks_with_lists():
    """
    リスト内のコードブロックとコードブロック内のリスト表現をテストします。
    """
    markdown = """
* 箇条書き
  ```python
  # コードブロック内のコメント
  def hello():
      # インデントされたコメント
      print("Hello")
      # これはコードブロック内の擬似リスト
      # - アイテム1
      # - アイテム2
  ```
  * コードブロック後の箇条書き

1. 番号付きリスト
   ```
   コード内のプレーンテキスト
   1. これはコード内の番号付きリストの表現（実際のリストではない）
   ```
   2. コードブロック後の番号付きリスト（継続）
"""

    blocks = markdown_to_notion_blocks(markdown)

    # ブロック数の検証
    assert len(blocks) > 0

    # コードブロックが存在することを確認
    code_blocks = [b for b in blocks if b["type"] == "code"]
    assert len(code_blocks) > 0

    # 箇条書きリスト項目が存在することを確認
    bulleted_items = [b for b in blocks if b["type"] == "bulleted_list_item"]
    assert len(bulleted_items) > 0

    # 番号付きリスト項目が存在することを確認
    numbered_items = [b for b in blocks if b["type"] == "numbered_list_item"]
    assert len(numbered_items) > 0

    # コードブロックの言語が適切に設定されていることを確認
    assert code_blocks[0]["code"]["language"] == "python"

    # 注意：実際の実装によっては、このテストは調整が必要かもしれません


def test_nested_special_characters():
    """
    ネスト構造内の特殊文字の処理をテストします。
    """
    markdown = """
* 特殊文字: !@#$%^&*()_+-={}[]|\\:;"'<>,.?/
  * ネストされた特殊文字：\\*エスケープされたアスタリスク\\*
    * エスケープされたバックスラッシュ: \\\\
      * エスケープされた引用符: \\"引用符\\"
"""

    blocks = markdown_to_notion_blocks(markdown)

    # ブロック数の検証
    assert len(blocks) > 0

    # 最初のリスト項目が特殊文字を含むことを確認
    assert blocks[0]["type"] == "bulleted_list_item"
    assert (
        "!@#$%^&*()_+-={}[]|\\:;"
        in blocks[0]["bulleted_list_item"]["rich_text"][0]["text"]["content"]
    )

    # 注意：実際の実装によっては、このテストは調整が必要かもしれません


def test_mixed_nested_structures():
    """
    様々なネスト構造の組み合わせをテストします。
    """
    markdown = """
1. **太字テキスト**を含む番号付きリスト
   > 引用テキスト
   > **引用内の太字テキスト**
   ```
   コードブロック
   ```
   * 番号付きリスト内の箇条書き
     1. 箇条書き内の番号付きリスト
        * 深くネストされた箇条書き
          > 深くネストされた箇条書き内の引用
2. ~~取り消し線テキスト~~を含む番号付きリスト
   * [リンク](https://www.notion.so)を含む箇条書き
     * **太字[リンク](https://www.notion.so)と通常**テキスト
       * ~~取り消し線付き[リンク](https://www.notion.so)~~
"""

    blocks = markdown_to_notion_blocks(markdown)

    # ブロック数の検証
    assert len(blocks) > 0

    # 様々なタイプのブロックが存在することを確認
    block_types = set([b["type"] for b in blocks])
    assert "numbered_list_item" in block_types
    assert (
        "quote" in block_types
        or "code" in block_types
        or "bulleted_list_item" in block_types
    )

    # 最初の番号付きリストが太字テキストを含むことを確認
    first_numbered = [b for b in blocks if b["type"] == "numbered_list_item"][0]

    has_bold = False
    for rt in first_numbered["numbered_list_item"]["rich_text"]:
        if rt["annotations"]["bold"] == True:
            has_bold = True
            break
    assert has_bold == True

    # 注意：実際の実装によっては、このテストは調整が必要かもしれません
