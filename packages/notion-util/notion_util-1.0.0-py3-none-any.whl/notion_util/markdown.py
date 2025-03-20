"""
マークダウンテキストとNotionブロックの相互変換を行う機能を提供します。
"""

import re
import logging
from .text_utils import lint_to_blocks


def markdown_to_notion_blocks(markdown_text):
    """
    マークダウンテキストをNotionのブロック形式に変換します。

    Args:
        markdown_text (str): 変換するマークダウンテキスト

    Returns:
        list: Notionブロックのリスト
    """
    lines = markdown_text.split("\n")
    blocks = []
    current_indent_level = 0
    list_item_stack = [
        [] for _ in range(10)
    ]  # 10レベルのネストに対応するスタックを用意
    code_block_open = False
    code_language = ""
    code_content = []
    # 現在のリストタイプを追跡するための変数
    current_list_types = [""] * 10  # 各インデントレベルでのリストタイプを保存
    # Notionのリストネストの最大深さ（APIの制限に基づく）
    MAX_NEST_LEVEL = 2

    logging.debug(f"Processing {len(lines)} lines of markdown text")

    # リスト項目を処理する共通関数
    def process_list_item(indent_level, block, list_type):
        nonlocal current_indent_level

        # Notionの制限に合わせて、深すぎるネストレベルを制限する
        effective_indent_level = min(indent_level, MAX_NEST_LEVEL)

        # 現在のインデントレベルのリストタイプを更新
        current_list_types[effective_indent_level] = list_type

        if effective_indent_level == 0:  # トップレベル
            blocks.append(block)
            current_indent_level = 0
            list_item_stack[0] = [block]  # スタックをリセット
        elif effective_indent_level > current_indent_level:  # より深いインデント
            # インデックスエラーを防ぐためのチェック
            if (
                effective_indent_level >= len(list_item_stack)
                or not list_item_stack[effective_indent_level - 1]
            ):
                # スタックが不足している場合は調整
                for i in range(len(list_item_stack), effective_indent_level + 1):
                    list_item_stack.append([])
                # 親がない場合はトップレベルに追加
                blocks.append(block)
                list_item_stack[effective_indent_level] = [block]
            else:
                list_item_stack[effective_indent_level].append(block)
                # 親のリストタイプとブロックを取得
                parent_type = current_list_types[effective_indent_level - 1]
                parent_block = list_item_stack[effective_indent_level - 1][-1]
                # 親ブロックに子ブロックを追加
                add_child_to_parent(
                    parent_type, parent_block, block, effective_indent_level
                )
            current_indent_level = effective_indent_level
        elif effective_indent_level == current_indent_level:  # 同じインデントレベル
            # インデックスエラーを防ぐためのチェック
            if (
                effective_indent_level >= len(list_item_stack)
                or effective_indent_level - 1 >= len(list_item_stack)
                or not list_item_stack[effective_indent_level - 1]
            ):
                # スタックが不足している場合は調整
                for i in range(len(list_item_stack), effective_indent_level + 1):
                    list_item_stack.append([])
                # 親がない場合はトップレベルに追加
                blocks.append(block)
                list_item_stack[effective_indent_level] = [block]
            else:
                list_item_stack[effective_indent_level].append(block)
                # 親のリストタイプとブロックを取得
                parent_type = current_list_types[effective_indent_level - 1]
                parent_block = list_item_stack[effective_indent_level - 1][-1]
                # 親ブロックに子ブロックを追加
                add_child_to_parent(
                    parent_type, parent_block, block, effective_indent_level
                )
        else:  # インデントレベルが減少
            current_indent_level = effective_indent_level
            # インデックスエラーを防ぐためのチェック
            if effective_indent_level >= len(list_item_stack):
                # スタックが不足している場合は調整
                for i in range(len(list_item_stack), effective_indent_level + 1):
                    list_item_stack.append([])
            list_item_stack[effective_indent_level].append(block)
            if effective_indent_level > 0:  # 親リストが存在する場合
                # インデックスエラーを防ぐためのチェック
                if (
                    effective_indent_level - 1 >= len(list_item_stack)
                    or not list_item_stack[effective_indent_level - 1]
                ):
                    # 親がない場合はトップレベルに追加
                    blocks.append(block)
                else:
                    # 親のリストタイプとブロックを取得
                    parent_type = current_list_types[effective_indent_level - 1]
                    parent_block = list_item_stack[effective_indent_level - 1][-1]
                    # 親ブロックに子ブロックを追加
                    add_child_to_parent(
                        parent_type, parent_block, block, effective_indent_level
                    )

    # 親ブロックに子ブロックを追加する関数
    def add_child_to_parent(parent_type, parent_block, child_block, current_level):
        # ネストレベルがNotionの制限を超える場合は子ブロックを追加しない
        if current_level > MAX_NEST_LEVEL:
            # 制限を超えた場合はブロックをトップレベルに追加
            blocks.append(child_block)
            return

        if parent_type == "numbered_list_item" and "numbered_list_item" in parent_block:
            parent_block["numbered_list_item"]["children"].append(child_block)
        elif (
            parent_type == "bulleted_list_item" and "bulleted_list_item" in parent_block
        ):
            parent_block["bulleted_list_item"]["children"].append(child_block)

    for i, line in enumerate(lines):
        logging.debug(f"Line {i}: {line[:50]}...")

        # 空行はスキップ
        if not line.strip():
            continue

        # コードブロックの処理
        if line.strip().startswith("```"):
            if not code_block_open:
                # コードブロックの開始
                code_block_open = True
                code_language = line.strip()[3:].lower() or "plain_text"
                logging.debug(f"Opening code block with language: {code_language}")
                code_content = []
            else:
                # コードブロックの終了
                logging.debug(f"Closing code block with language: {code_language}")
                if code_language == "":
                    code_language = "markdown"  # デフォルト言語
                # Notion APIが期待する形式に変換
                if code_language == "plain_text":
                    code_language = "plain text"
                blocks.append(
                    {
                        "object": "block",
                        "type": "code",
                        "code": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": "\n".join(code_content)},
                                }
                            ],
                            "language": code_language,
                        },
                    }
                )
                code_block_open = False
                code_language = ""
                code_content = []
            continue
        elif code_block_open:
            # コードブロック内の行を追加
            code_content.append(line)
            continue

        # インデントレベルを計算
        indent_level = 0
        stripped_line = line.lstrip()
        indent_spaces = len(line) - len(stripped_line)
        indent_level = indent_spaces // 4  # 4スペースでインデントレベルを1と計算

        logging.debug(f"Indent level: {indent_level}")

        # 引用の処理
        if stripped_line.startswith(">"):
            quote_content = stripped_line[1:].strip()
            logging.debug(f"Processing quote: {quote_content[:20]}...")

            # 引用内のリッチテキストブロックを生成（マークダウン記法を解析）
            rich_text_blocks = lint_to_blocks(quote_content)

            if not rich_text_blocks:
                logging.debug("Skipping empty quote")
                continue

            blocks.append(
                {
                    "object": "block",
                    "type": "quote",
                    "quote": {
                        "rich_text": rich_text_blocks,
                    },
                }
            )
            continue

        # Markdown要素の種類をチェック
        if stripped_line.lstrip().startswith("#"):
            # '#'の数で見出しのレベルを判定
            heading_level = len(stripped_line.lstrip()) - len(stripped_line.lstrip("#"))
            heading_level = min(heading_level, 3)
            content = stripped_line.lstrip("#").strip()
            logging.debug(f"Processing heading {heading_level}: {content[:30]}...")
            rich_text_blocks = lint_to_blocks(content)
            if rich_text_blocks:
                block = {
                    "object": "block",
                    "type": f"heading_{heading_level}",
                    f"heading_{heading_level}": {
                        "rich_text": rich_text_blocks,
                    },
                }
                blocks.append(block)
            continue

        # numbered_list_item
        match_number_list = re.match(r"^\s*\d+\.\s+(.+)$", stripped_line)
        if match_number_list:
            content = match_number_list.group(
                1
            )  # 数字とドットとスペースを取り除いたテキスト
            logging.debug(f"Processing numbered list item: {content[:30]}...")

            # 取り消し線付きのテキストを特別に処理
            if content.startswith("~~") and content.endswith("~~") and len(content) > 4:
                # 取り消し線内部のテキストを取得
                strike_content = content[2:-2]
                # 取り消し線付きのリッチテキストブロックを生成
                rich_text_blocks = []

                # リンクを含む取り消し線の特別処理
                if "[" in strike_content and "](" in strike_content:
                    # リンク部分を検出
                    link_pattern = re.search(
                        r"\[([^\[\]]+)\]\(([^)]+)\)", strike_content
                    )
                    if link_pattern:
                        before_link = strike_content[: link_pattern.start()]
                        link_text = link_pattern.group(1)
                        link_url = link_pattern.group(2)
                        after_link = strike_content[link_pattern.end() :]

                        # リンク前のテキストを追加
                        if before_link:
                            rich_text_blocks.append(
                                {
                                    "type": "text",
                                    "text": {"content": before_link},
                                    "annotations": {
                                        "bold": False,
                                        "italic": False,
                                        "strikethrough": True,
                                        "underline": False,
                                        "code": False,
                                        "color": "default",
                                    },
                                }
                            )

                        # リンクを追加
                        rich_text_blocks.append(
                            {
                                "type": "text",
                                "text": {
                                    "content": link_text,
                                    "link": {"url": link_url},
                                },
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "default",
                                },
                            }
                        )

                        # リンク後のテキストを追加
                        if after_link:
                            rich_text_blocks.append(
                                {
                                    "type": "text",
                                    "text": {"content": after_link},
                                    "annotations": {
                                        "bold": False,
                                        "italic": False,
                                        "strikethrough": True,
                                        "underline": False,
                                        "code": False,
                                        "color": "default",
                                    },
                                }
                            )
                    else:
                        # リンクがない場合は通常の取り消し線テキスト
                        rich_text_blocks.append(
                            {
                                "type": "text",
                                "text": {"content": strike_content},
                                "annotations": {
                                    "bold": False,
                                    "italic": False,
                                    "strikethrough": True,
                                    "underline": False,
                                    "code": False,
                                    "color": "default",
                                },
                            }
                        )
                else:
                    # リンクがない場合は通常の取り消し線テキスト
                    rich_text_blocks.append(
                        {
                            "type": "text",
                            "text": {"content": strike_content},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": True,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                        }
                    )
            else:
                # 通常のリッチテキストブロックを生成
                rich_text_blocks = lint_to_blocks(content)

            if not rich_text_blocks:
                logging.debug("Skipping empty numbered list item")
                continue

            block = {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {
                    "rich_text": rich_text_blocks,
                    "children": [],
                },
            }

            process_list_item(indent_level, block, "numbered_list_item")
            continue

        # bulleted_list_item
        match_bullet_list = re.match(r"^\s*[\*\-]\s+(.+)$", stripped_line)
        if match_bullet_list:
            content = match_bullet_list.group(
                1
            )  # '*'または'-'とスペースを取り除いたテキスト
            logging.debug(f"Processing bulleted list item: {content[:30]}...")
            rich_text_blocks = lint_to_blocks(content)
            if not rich_text_blocks:
                logging.debug("Skipping empty bulleted list item")
                continue

            block = {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": rich_text_blocks,
                    "children": [],
                },
            }

            process_list_item(indent_level, block, "bulleted_list_item")
            continue

        # パラグラフ（普通のテキスト）の処理
        elif stripped_line != "":  # 空行を無視
            logging.debug(f"Processing paragraph: {stripped_line[:30]}...")
            rich_text_blocks = lint_to_blocks(stripped_line)
            if rich_text_blocks:
                block = {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": rich_text_blocks,
                    },
                }
                blocks.append(block)
            continue

    # スタックから空の子リストを削除
    for level_blocks in list_item_stack:
        for block in level_blocks:
            if (
                "bulleted_list_item" in block
                and "children" in block["bulleted_list_item"]
                and not block["bulleted_list_item"]["children"]
            ):
                del block["bulleted_list_item"]["children"]
            elif (
                "numbered_list_item" in block
                and "children" in block["numbered_list_item"]
                and not block["numbered_list_item"]["children"]
            ):
                del block["numbered_list_item"]["children"]

    # ブロックを浄化
    cleaned_blocks = clean_blocks(blocks)

    logging.debug(
        f"Generated {len(cleaned_blocks)} blocks from markdown (after cleaning)"
    )
    return cleaned_blocks


def clean_blocks(blocks):
    """
    Notionブロックを整理し、Noneや空のリッチテキストを削除します。

    Args:
        blocks (list): 浄化するNotionブロックのリスト

    Returns:
        list: 浄化されたNotionブロックのリスト
    """
    cleaned_blocks = []
    for block in blocks:
        try:
            # リッチテキストを持つブロックタイプを検知
            if "paragraph" in block:
                rich_text_property = "paragraph"
            elif "bulleted_list_item" in block:
                rich_text_property = "bulleted_list_item"
            elif "numbered_list_item" in block:
                rich_text_property = "numbered_list_item"
            elif "quote" in block:
                rich_text_property = "quote"
            elif "heading_1" in block:
                rich_text_property = "heading_1"
            elif "heading_2" in block:
                rich_text_property = "heading_2"
            elif "heading_3" in block:
                rich_text_property = "heading_3"
            else:
                # テキストブロックではない場合、そのまま追加
                cleaned_blocks.append(block)
                continue

            # リッチテキスト配列からNone値を除去
            if rich_text_property in block and "rich_text" in block[rich_text_property]:
                # None値と空の内容を持つブロックを除去
                block[rich_text_property]["rich_text"] = [
                    rt
                    for rt in block[rich_text_property]["rich_text"]
                    if rt is not None
                    and rt.get("text", {}).get("content", "").strip() != ""
                ]
                # リッチテキストが空の場合はスキップ
                if block[rich_text_property]["rich_text"]:
                    cleaned_blocks.append(block)
            else:
                # リッチテキストプロパティがない場合、そのまま追加
                cleaned_blocks.append(block)

            # 子ブロックの処理（リスト項目の場合）
            if (
                rich_text_property in ["bulleted_list_item", "numbered_list_item"]
                and "children" in block[rich_text_property]
            ):
                # 子ブロックも同様に浄化
                clean_children = []
                for child_block in block[rich_text_property]["children"]:
                    # 子ブロックのタイプを特定
                    child_type = None
                    for type_key in [
                        "paragraph",
                        "bulleted_list_item",
                        "numbered_list_item",
                        "quote",
                        "heading_1",
                        "heading_2",
                        "heading_3",
                    ]:
                        if type_key in child_block:
                            child_type = type_key
                            break

                    if child_type and "rich_text" in child_block.get(child_type, {}):
                        # 子ブロックからもNone値と空の内容を持つブロックを除去
                        child_block[child_type]["rich_text"] = [
                            rt
                            for rt in child_block[child_type]["rich_text"]
                            if rt is not None
                            and rt.get("text", {}).get("content", "").strip() != ""
                        ]
                        if child_block[child_type]["rich_text"]:
                            clean_children.append(child_block)
                    else:
                        clean_children.append(child_block)

                # 浄化した子ブロックで置き換え
                if clean_children:
                    block[rich_text_property]["children"] = clean_children
                else:
                    # 子ブロックが全て削除された場合は、children属性を削除
                    del block[rich_text_property]["children"]
        except Exception as e:
            logging.warning(f"Error cleaning block: {str(e)}")
            # エラーが発生した場合は安全のためブロックをスキップ
            continue

    return cleaned_blocks
