"""
後方互換性のために、リファクタリングされたモジュールからすべての機能をインポートします。
このモジュールは、以前のバージョンとの互換性を保つためのインターフェースとして機能します。
"""

# リファクタリングされたモジュールのインポート
from .client import Notion, recursive_types, skip_types
from .markdown import markdown_to_notion_blocks, clean_blocks
from .extractors import extract_notion_page_id, extract_notion_page_ids, find_links
from .text_utils import lint_to_blocks

import logging
import re
import os


def get_page_markdown(url_or_id, recursive=True, depth=3):
    """
    NotionのURLまたはページIDからマークダウンテキストを取得します。

    Args:
        url_or_id (str): NotionのURLまたはページID
        recursive (bool, optional): 再帰的にブロックを取得するかどうか
        depth (int, optional): 再帰的に取得する深さの最大値

    Returns:
        str: マークダウンテキスト
    """
    # URLからページIDを抽出
    page_id = extract_notion_page_id(url_or_id) or url_or_id

    # Notionクライアントを初期化
    notion = Notion()

    # ページ情報を取得
    page_info = notion.get_page(page_id)
    logging.debug(f"Page info: {page_info}")

    # ページタイトルを取得
    title = ""
    properties = page_info.get("properties", {})
    if "title" in properties and "title" in properties["title"]:
        title_items = properties["title"]["title"]
        if title_items:
            title = "".join([item.get("plain_text", "") for item in title_items])
    markdown_text = f"# {title}\n\n"

    # ブロックを取得（再帰的または非再帰的）
    if recursive:
        blocks = notion.recursive_get_blocks(page_id, depth=depth)
    else:
        blocks = notion.get_all_block_children(page_id)

    logging.debug(f"Retrieved {len(blocks)} blocks")

    # ブロックをマークダウンに変換
    markdown_text += blocks_to_markdown(blocks)

    return markdown_text


def blocks_to_markdown(blocks, indent_level=0):
    """
    Notionのブロックをマークダウンテキストに変換します。

    Args:
        blocks (list): 変換するブロックのリスト
        indent_level (int, optional): インデントレベル

    Returns:
        str: マークダウンテキスト
    """
    markdown = ""
    indent = "    " * indent_level

    for block in blocks:
        block_type = block.get("type")
        block_id = block.get("id")

        if block_type == "paragraph":
            text = extract_text_from_rich_text(
                block.get("paragraph", {}).get("rich_text", [])
            )
            if text:
                markdown += f"{indent}{text}\n\n"

        elif block_type == "heading_1":
            text = extract_text_from_rich_text(
                block.get("heading_1", {}).get("rich_text", [])
            )
            markdown += f"{indent}# {text}\n\n"

        elif block_type == "heading_2":
            text = extract_text_from_rich_text(
                block.get("heading_2", {}).get("rich_text", [])
            )
            markdown += f"{indent}## {text}\n\n"

        elif block_type == "heading_3":
            text = extract_text_from_rich_text(
                block.get("heading_3", {}).get("rich_text", [])
            )
            markdown += f"{indent}### {text}\n\n"

        elif block_type == "bulleted_list_item":
            text = extract_text_from_rich_text(
                block.get("bulleted_list_item", {}).get("rich_text", [])
            )
            markdown += f"{indent}- {text}\n"

            # 子ブロックを再帰的に処理
            if (
                "children" in block.get("bulleted_list_item", {})
                and block["bulleted_list_item"]["children"]
            ):
                markdown += blocks_to_markdown(
                    block["bulleted_list_item"]["children"], indent_level + 1
                )
                markdown += "\n"  # 子リストの後に空行を追加

        elif block_type == "numbered_list_item":
            text = extract_text_from_rich_text(
                block.get("numbered_list_item", {}).get("rich_text", [])
            )
            markdown += f"{indent}1. {text}\n"

            # 子ブロックを再帰的に処理
            if (
                "children" in block.get("numbered_list_item", {})
                and block["numbered_list_item"]["children"]
            ):
                markdown += blocks_to_markdown(
                    block["numbered_list_item"]["children"], indent_level + 1
                )
                markdown += "\n"  # 子リストの後に空行を追加

        elif block_type == "quote":
            text = extract_text_from_rich_text(
                block.get("quote", {}).get("rich_text", [])
            )
            markdown += f"{indent}> {text}\n\n"

            # 子ブロックを再帰的に処理
            if "children" in block.get("quote", {}) and block["quote"]["children"]:
                child_markdown = blocks_to_markdown(
                    block["quote"]["children"], indent_level
                )
                markdown += f"{indent}> {child_markdown.replace('n', 'n> ')}\n"

        elif block_type == "code":
            text = extract_text_from_rich_text(
                block.get("code", {}).get("rich_text", [])
            )
            language = block.get("code", {}).get("language", "")
            markdown += f"{indent}```{language}\n{text}\n{indent}```\n\n"

        elif block_type == "divider":
            markdown += f"{indent}---\n\n"

        elif block_type == "to_do":
            text = extract_text_from_rich_text(
                block.get("to_do", {}).get("rich_text", [])
            )
            checked = block.get("to_do", {}).get("checked", False)
            checkbox = "x" if checked else " "
            markdown += f"{indent}- [{checkbox}] {text}\n"

        # その他のブロックタイプ
        else:
            logging.debug(f"Unsupported block type: {block_type}")

    return markdown


def extract_text_from_rich_text(rich_text):
    """
    リッチテキストからプレーンテキストを抽出します。

    Args:
        rich_text (list): リッチテキスト要素のリスト

    Returns:
        str: 抽出されたプレーンテキスト
    """
    if not rich_text:
        return ""

    text = ""
    for item in rich_text:
        if item.get("type") == "text":
            content = item.get("text", {}).get("content", "")
            annotations = item.get("annotations", {})
            link = item.get("text", {}).get("link")

            # 注釈を適用
            if annotations.get("bold"):
                content = f"**{content}**"
            if annotations.get("italic"):
                content = f"*{content}*"
            if annotations.get("strikethrough"):
                content = f"~~{content}~~"
            if annotations.get("underline"):
                content = f"__{content}__"
            if annotations.get("code"):
                content = f"`{content}`"

            # リンクを適用
            if link:
                url = link.get("url", "")
                content = f"[{content}]({url})"

            text += content

    return text


def get_page_database(url_or_id, filter_params=None):
    """
    指定されたデータベースからすべてのページを取得します。

        Args:
        url_or_id (str): NotionのURLまたはデータベースID
        filter_params (dict, optional): フィルタパラメータ

        Returns:
        list: データベース内のページのリスト
    """
    # URLからデータベースIDを抽出
    database_id = extract_notion_page_id(url_or_id) or url_or_id

    # Notionクライアントを初期化
    notion = Notion()

    # データベース情報を取得
    database_info = notion.get_database(database_id)
    logging.debug(f"Database info: {database_info}")

    # データベース内のページをクエリ
    response = notion.get_database_pages(database_id, filter_params)
    pages = response.get("results", [])

    return pages


def create_page_from_markdown(markdown_text, parent):
    """
    マークダウンテキストからNotionページを作成します。

        Args:
        markdown_text (str): ソースとなるマークダウンテキスト
        parent (str or dict): 親ページまたはデータベースの情報

    Returns:
        dict: 作成されたページ情報
    """
    # 親情報を処理
    if isinstance(parent, str):
        parent_id = extract_notion_page_id(parent) or parent
        # データベースまたはページに対する親情報を作成
        if re.match(r"^[a-f0-9]{32}$", parent_id):
            parent = {"database_id": parent_id}
        else:
            parent = {"page_id": parent_id}

    # Notionクライアントを初期化
    notion = Notion()

    # マークダウンをNotionブロックに変換
    blocks = markdown_to_notion_blocks(markdown_text)
    logging.debug(f"Generated {len(blocks)} blocks from markdown")

    # デフォルトのプロパティを設定
    properties = {"title": {"title": [{"text": {"content": "New Page From Markdown"}}]}}

    # タイトルを抽出（最初の見出しをタイトルとして使用）
    for block in blocks:
        if block.get("type") == "heading_1" and "heading_1" in block:
            rich_text = block["heading_1"].get("rich_text", [])
            if rich_text:
                title_text = "".join(
                    [rt.get("text", {}).get("content", "") for rt in rich_text]
                )
                properties["title"]["title"][0]["text"]["content"] = title_text
                # タイトルとして使った見出しはブロックから削除
                blocks.remove(block)
                break

    # ページを作成
    new_page = notion.create_page(parent, properties)
    page_id = new_page.get("id")
    logging.info(f"Created page with ID: {page_id}")

    # ブロックをページに追加（最大100ブロックずつ）
    for i in range(0, len(blocks), 100):
        chunk = blocks[i : i + 100]
        notion.append_blocks(page_id, chunk)
        logging.debug(f"Appended {len(chunk)} blocks to page")

    return new_page
