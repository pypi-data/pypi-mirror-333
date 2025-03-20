import pytest
from notion_util.markdown import detect_indent_spaces, markdown_to_notion_blocks


def test_indent_detection_2spaces():
    """
    2スペースインデントの検出をテストします。
    """
    # 2スペースインデントのマークダウン
    markdown = """
- 項目1
- 項目2
  - ネストされた項目2.1
  - ネストされた項目2.2
    - 深くネストされた項目2.2.1
    - 深くネストされた項目2.2.2
  - ネストされた項目2.3
- 項目3
"""

    # インデントスペースの検出
    indent_spaces = detect_indent_spaces(markdown.split("\n"))
    assert (
        indent_spaces == 2
    ), f"2スペースインデントが検出されるべきですが、{indent_spaces}が検出されました"

    # markdownからNotionブロックへの変換
    blocks = markdown_to_notion_blocks(markdown)

    # 正しい数のトップレベル項目があることを確認
    top_level_items = [b for b in blocks if b["type"] == "bulleted_list_item"]
    assert len(top_level_items) == 3

    # 項目2に子項目があることを確認
    assert "children" in top_level_items[1]["bulleted_list_item"]
    assert len(top_level_items[1]["bulleted_list_item"]["children"]) == 3

    # 項目2.2に子項目があることを確認
    children_of_2 = top_level_items[1]["bulleted_list_item"]["children"]
    assert "children" in children_of_2[1]["bulleted_list_item"]
    assert len(children_of_2[1]["bulleted_list_item"]["children"]) == 2


def test_indent_detection_4spaces():
    """
    4スペースインデントの検出をテストします。
    """
    # 4スペースインデントのマークダウン
    markdown = """
- 項目1
- 項目2
    - ネストされた項目2.1
    - ネストされた項目2.2
        - 深くネストされた項目2.2.1
        - 深くネストされた項目2.2.2
    - ネストされた項目2.3
- 項目3
"""

    # インデントスペースの検出
    indent_spaces = detect_indent_spaces(markdown.split("\n"))
    assert (
        indent_spaces == 4
    ), f"4スペースインデントが検出されるべきですが、{indent_spaces}が検出されました"

    # markdownからNotionブロックへの変換
    blocks = markdown_to_notion_blocks(markdown)

    # 正しい数のトップレベル項目があることを確認
    top_level_items = [b for b in blocks if b["type"] == "bulleted_list_item"]
    assert len(top_level_items) == 3

    # 項目2に子項目があることを確認
    assert "children" in top_level_items[1]["bulleted_list_item"]
    assert len(top_level_items[1]["bulleted_list_item"]["children"]) == 3

    # 項目2.2に子項目があることを確認
    children_of_2 = top_level_items[1]["bulleted_list_item"]["children"]
    assert "children" in children_of_2[1]["bulleted_list_item"]
    assert len(children_of_2[1]["bulleted_list_item"]["children"]) == 2


def test_indent_detection_mixed():
    """
    混合インデント（タブと空白）の検出をテストします。
    """
    # タブと空白が混合したマークダウン
    markdown = """
- 項目1
- 項目2
\t- ネストされた項目2.1（タブ）
    - ネストされた項目2.2（4スペース）
\t\t- 深くネストされた項目2.2.1（2タブ）
        - 深くネストされた項目2.2.2（8スペース）
    - ネストされた項目2.3
- 項目3
"""

    # インデントスペースの検出（実際の検出結果を確認）
    indent_spaces = detect_indent_spaces(markdown.split("\n"))

    # markdownからNotionブロックへの変換
    blocks = markdown_to_notion_blocks(markdown)

    # 正しい数のトップレベル項目があることを確認
    top_level_items = [b for b in blocks if b["type"] == "bulleted_list_item"]
    assert len(top_level_items) == 3

    # ネスト構造が正しく処理されることを確認（子項目の存在を確認）
    assert "children" in top_level_items[1]["bulleted_list_item"]


def test_indent_detection_numbered_list():
    """
    番号付きリストのインデント検出をテストします。
    """
    # 番号付きリストのマークダウン（4スペースインデント）
    markdown = """
1. 項目1
2. 項目2
    1. ネストされた項目2.1
    2. ネストされた項目2.2
        1. 深くネストされた項目2.2.1
        2. 深くネストされた項目2.2.2
    3. ネストされた項目2.3
3. 項目3
"""

    # インデントスペースの検出
    indent_spaces = detect_indent_spaces(markdown.split("\n"))
    assert (
        indent_spaces == 4
    ), f"4スペースインデントが検出されるべきですが、{indent_spaces}が検出されました"

    # markdownからNotionブロックへの変換
    blocks = markdown_to_notion_blocks(markdown)

    # 正しい数のトップレベル項目があることを確認
    top_level_items = [b for b in blocks if b["type"] == "numbered_list_item"]
    assert len(top_level_items) == 3

    # 項目2に子項目があることを確認
    assert "children" in top_level_items[1]["numbered_list_item"]
    assert len(top_level_items[1]["numbered_list_item"]["children"]) == 3

    # 項目2.2に子項目があることを確認
    children_of_2 = top_level_items[1]["numbered_list_item"]["children"]
    assert "children" in children_of_2[1]["numbered_list_item"]
    assert len(children_of_2[1]["numbered_list_item"]["children"]) == 2


def test_maximum_nesting_level():
    """
    Notionの最大ネストレベル（2）を超えるネストの処理をテストします。
    """
    # 深くネストされたマークダウン
    markdown = """
- レベル1
  - レベル2
    - レベル3（MAX_NEST_LEVELの2を超える）
      - レベル4（更に深いネスト）
        - レベル5（非常に深いネスト）
  - 別のレベル2
"""

    # markdownからNotionブロックへの変換
    blocks = markdown_to_notion_blocks(markdown)

    # トップレベル項目があることを確認
    top_level_items = [b for b in blocks if b["type"] == "bulleted_list_item"]
    assert len(top_level_items) == 1

    # レベル1に子項目があることを確認
    assert "children" in top_level_items[0]["bulleted_list_item"]
    level1_children = top_level_items[0]["bulleted_list_item"]["children"]
    assert len(level1_children) == 2

    # レベル2（最初の項目）に子項目があることを確認
    assert "children" in level1_children[0]["bulleted_list_item"]
    level2_children = level1_children[0]["bulleted_list_item"]["children"]

    # レベル3以降はすべてレベル2の子として処理されることを確認
    assert len(level2_children) > 0
