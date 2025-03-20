"""
マークダウンテキストとNotionブロックの相互変換を行う機能を提供します。
"""

import re
import logging
from .text_utils import lint_to_blocks

# 定数定義
# インデント自動検出のための初期値（後で自動検出された値に上書きされる）
DEFAULT_INDENT_SPACES = 2
MAX_NEST_LEVEL = 2  # Notionのリストネストの最大深さ（APIの制限に基づく）
DEFAULT_CODE_LANGUAGE = "markdown"
PLAIN_TEXT = "plain text"

# 共通のブロックタイプ
BLOCK_TYPES = [
    "paragraph",
    "bulleted_list_item",
    "numbered_list_item",
    "quote",
    "heading_1",
    "heading_2",
    "heading_3",
]


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
    current_list_types = [""] * 10  # 各インデントレベルでのリストタイプを保存

    # インデントスペースを自動検出
    indent_spaces = detect_indent_spaces(lines)
    logging.debug(f"Detected indent spaces: {indent_spaces}")

    # コードブロック処理用の変数
    code_block_state = {"is_open": False, "language": "", "content": []}

    logging.debug(f"Processing {len(lines)} lines of markdown text")

    for i, line in enumerate(lines):
        logging.debug(f"Line {i}: {line[:50]}...")

        # 空行はスキップ
        if not line.strip():
            continue

        # コードブロックの処理
        if line.strip().startswith("```"):
            if process_code_block_delimiter(line, code_block_state, blocks):
                continue
        elif code_block_state["is_open"]:
            # コードブロック内の行を追加
            code_block_state["content"].append(line)
            continue

        # インデントレベルを計算
        indent_level, stripped_line = calculate_indent_level(line, indent_spaces)
        logging.debug(f"Indent level: {indent_level}")

        # 各種ブロックタイプの処理
        if process_block(
            stripped_line,
            indent_level,
            blocks,
            list_item_stack,
            current_list_types,
            current_indent_level,
        ):
            continue

    # 後処理: スタックから空の子リストを削除
    clean_list_item_stack(list_item_stack)

    # ブロックを浄化
    cleaned_blocks = clean_blocks(blocks)

    logging.debug(
        f"Generated {len(cleaned_blocks)} blocks from markdown (after cleaning)"
    )
    return cleaned_blocks


def detect_indent_spaces(lines):
    """
    マークダウン行のリスト項目のインデントスペース数を検出する関数

    Args:
        lines (list): マークダウンのテキスト行のリスト

    Returns:
        int: 検出されたインデントスペース数（デフォルトは2）
    """
    # インデントされた行を見つけてインデントスペース数を収集
    indent_counts = {}
    prev_indent = 0

    for line in lines:
        stripped = line.lstrip()
        # 空行はスキップ
        if not stripped:
            continue

        # リスト項目のみを対象とする
        if re.match(r"^\s*[\*\-]\s+.*$", line) or re.match(r"^\s*\d+\.\s+.*$", line):
            current_indent = len(line) - len(stripped)

            # 前の行より深いインデントの場合、その差分を記録
            if current_indent > prev_indent and prev_indent > 0:
                diff = current_indent - prev_indent
                if diff > 0:
                    indent_counts[diff] = indent_counts.get(diff, 0) + 1

            prev_indent = current_indent

    # 最も頻繁に使われているインデント差分を見つける
    if indent_counts:
        most_common_indent = max(indent_counts.items(), key=lambda x: x[1])[0]
        return most_common_indent

    # 検出できなかった場合はデフォルト値を返す
    return DEFAULT_INDENT_SPACES


def calculate_indent_level(line, indent_spaces):
    """インデントレベルを計算する関数"""
    stripped_line = line.lstrip()
    actual_spaces = len(line) - len(stripped_line)

    # 実際のスペース数をインデント単位で割って、レベルを計算
    indent_level = actual_spaces // indent_spaces if indent_spaces > 0 else 0

    # インデントスペースがある場合は最低でもレベル1とする
    if actual_spaces > 0 and indent_level == 0:
        indent_level = 1

    logging.debug(
        f"Indent calculation: spaces={actual_spaces}, unit={indent_spaces}, level={indent_level}"
    )

    return indent_level, stripped_line


def process_code_block_delimiter(line, code_block_state, blocks):
    """コードブロックの開始・終了を処理する関数"""
    if not code_block_state["is_open"]:
        # コードブロックの開始
        code_block_state["is_open"] = True
        code_block_state["language"] = line.strip()[3:].lower() or "plain_text"
        code_block_state["content"] = []
        logging.debug(
            f"Opening code block with language: {code_block_state['language']}"
        )
        return True
    else:
        # コードブロックの終了
        logging.debug(
            f"Closing code block with language: {code_block_state['language']}"
        )
        language = code_block_state["language"]

        if language == "":
            language = DEFAULT_CODE_LANGUAGE
        # Notion APIが期待する形式に変換
        if language == "plain_text":
            language = PLAIN_TEXT

        blocks.append(
            {
                "object": "block",
                "type": "code",
                "code": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "\n".join(code_block_state["content"])},
                        }
                    ],
                    "language": language,
                },
            }
        )

        # 状態をリセット
        code_block_state["is_open"] = False
        code_block_state["language"] = ""
        code_block_state["content"] = []
        return True

    return False


def process_block(
    stripped_line,
    indent_level,
    blocks,
    list_item_stack,
    current_list_types,
    current_indent_level,
):
    """Markdownの行の種類に応じた処理を行う関数"""
    # 画像リンクの処理（最初に処理する）
    image_match = re.match(r"^!\[([^\[\]]*)\]\(([^)]+)\)$", stripped_line)
    if image_match:
        image_alt = image_match.group(1)
        image_url = image_match.group(2)
        return process_image(image_alt, image_url, blocks)

    # 引用の処理
    if stripped_line.startswith(">"):
        return process_quote(stripped_line, blocks)

    # 見出しの処理
    if stripped_line.lstrip().startswith("#"):
        return process_heading(stripped_line, blocks)

    # 番号付きリストの処理
    match_number_list = re.match(r"^\s*\d+\.\s+(.+)$", stripped_line)
    if match_number_list:
        content = match_number_list.group(
            1
        )  # 数字とドットとスペースを取り除いたテキスト
        return process_numbered_list_item(
            content,
            indent_level,
            blocks,
            list_item_stack,
            current_list_types,
            current_indent_level,
        )

    # 箇条書きリストの処理
    match_bullet_list = re.match(r"^\s*[\*\-]\s+(.+)$", stripped_line)
    if match_bullet_list:
        content = match_bullet_list.group(
            1
        )  # '*'または'-'とスペースを取り除いたテキスト
        return process_bulleted_list_item(
            content,
            indent_level,
            blocks,
            list_item_stack,
            current_list_types,
            current_indent_level,
        )

    # パラグラフ（通常テキスト）の処理
    if stripped_line != "":
        return process_paragraph(stripped_line, blocks)

    return False


def process_quote(stripped_line, blocks):
    """引用ブロックを処理する関数"""
    quote_content = stripped_line[1:].strip()
    logging.debug(f"Processing quote: {quote_content[:20]}...")

    # 引用内のリッチテキストブロックを生成（マークダウン記法を解析）
    rich_text_blocks = lint_to_blocks(quote_content)

    if not rich_text_blocks:
        logging.debug("Skipping empty quote")
        return True

    blocks.append(
        {
            "object": "block",
            "type": "quote",
            "quote": {
                "rich_text": rich_text_blocks,
            },
        }
    )
    return True


def process_heading(stripped_line, blocks):
    """見出しブロックを処理する関数"""
    # '#'の数で見出しのレベルを判定
    heading_level = len(stripped_line.lstrip()) - len(stripped_line.lstrip("#"))
    heading_level = min(heading_level, 3)  # Notionは3レベルまでの見出しをサポート
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
    return True


def process_paragraph(stripped_line, blocks):
    """通常のパラグラフブロックを処理する関数"""
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
    return True


def process_numbered_list_item(
    content,
    indent_level,
    blocks,
    list_item_stack,
    current_list_types,
    current_indent_level,
):
    """番号付きリスト項目を処理する関数"""
    logging.debug(f"Processing numbered list item: {content[:30]}...")

    # 取り消し線付きのテキストの特別処理
    if content.startswith("~~") and content.endswith("~~") and len(content) > 4:
        rich_text_blocks = process_strikethrough_text(content)
    else:
        # 通常のリッチテキストブロックを生成
        rich_text_blocks = lint_to_blocks(content)

    if not rich_text_blocks:
        logging.debug("Skipping empty numbered list item")
        return True

    # 初期化時には children キーを含めない
    block = {
        "object": "block",
        "type": "numbered_list_item",
        "numbered_list_item": {
            "rich_text": rich_text_blocks,
        },
    }

    process_list_item(
        indent_level,
        block,
        "numbered_list_item",
        blocks,
        list_item_stack,
        current_list_types,
        current_indent_level,
    )
    return True


def process_bulleted_list_item(
    content,
    indent_level,
    blocks,
    list_item_stack,
    current_list_types,
    current_indent_level,
):
    """箇条書きリスト項目を処理する関数"""
    logging.debug(f"Processing bulleted list item: {content[:30]}...")
    rich_text_blocks = lint_to_blocks(content)

    if not rich_text_blocks:
        logging.debug("Skipping empty bulleted list item")
        return True

    # 初期化時には children キーを含めない
    block = {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "rich_text": rich_text_blocks,
        },
    }

    process_list_item(
        indent_level,
        block,
        "bulleted_list_item",
        blocks,
        list_item_stack,
        current_list_types,
        current_indent_level,
    )
    return True


def process_strikethrough_text(content):
    """取り消し線付きテキストを処理する関数"""
    # 取り消し線内部のテキストを取得
    strike_content = content[2:-2]
    rich_text_blocks = []

    # リンクを含む取り消し線の特別処理
    if "[" in strike_content and "](" in strike_content:
        # リンク部分を検出
        link_pattern = re.search(r"\[([^\[\]]+)\]\(([^)]+)\)", strike_content)
        if link_pattern:
            before_link = strike_content[: link_pattern.start()]
            link_text = link_pattern.group(1)
            link_url = link_pattern.group(2)
            after_link = strike_content[link_pattern.end() :]

            # リンク前のテキストを追加
            if before_link:
                rich_text_blocks.append(create_strikethrough_text_block(before_link))

            # リンクを追加
            rich_text_blocks.append(
                create_strikethrough_link_block(link_text, link_url)
            )

            # リンク後のテキストを追加
            if after_link:
                rich_text_blocks.append(create_strikethrough_text_block(after_link))
        else:
            # リンクがない場合は通常の取り消し線テキスト
            rich_text_blocks.append(create_strikethrough_text_block(strike_content))
    else:
        # リンクがない場合は通常の取り消し線テキスト
        rich_text_blocks.append(create_strikethrough_text_block(strike_content))

    return rich_text_blocks


def create_strikethrough_text_block(text):
    """取り消し線付きテキストブロックを作成する関数"""
    return {
        "type": "text",
        "text": {"content": text},
        "annotations": {
            "bold": False,
            "italic": False,
            "strikethrough": True,
            "underline": False,
            "code": False,
            "color": "default",
        },
    }


def create_strikethrough_link_block(text, url):
    """取り消し線付きリンクブロックを作成する関数"""
    return {
        "type": "text",
        "text": {
            "content": text,
            "link": {"url": url},
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


def process_list_item(
    indent_level,
    block,
    list_type,
    blocks,
    list_item_stack,
    current_list_types,
    current_indent_level,
):
    """リスト項目を処理する共通関数"""
    # 実際のインデントレベルを保存
    actual_indent_level = indent_level
    # Notionの制限に合わせて最大ネストレベルを適用
    effective_indent_level = min(indent_level, MAX_NEST_LEVEL)

    logging.debug(
        f"Processing list item: type={list_type}, indent_level={indent_level}, "
        f"effective_indent_level={effective_indent_level}, current_indent_level={current_indent_level}"
    )

    # 現在のインデントレベルのリストタイプを更新
    if actual_indent_level > MAX_NEST_LEVEL:
        # 3レベル以上の深いネストの場合、親の最大レベルにリストタイプを設定
        current_list_types[MAX_NEST_LEVEL] = list_type
    else:
        current_list_types[effective_indent_level] = list_type

    if effective_indent_level == 0:  # トップレベル
        add_top_level_list_item(block, blocks, list_item_stack)
        return 0
    elif effective_indent_level > current_indent_level:  # より深いインデント
        # 深すぎるネストの場合でも、適切な親に追加されるようにする
        return handle_deeper_indentation(
            effective_indent_level,
            block,
            list_type,
            blocks,
            list_item_stack,
            current_list_types,
        )
    elif effective_indent_level == current_indent_level:  # 同じインデントレベル
        # 深すぎるネストの場合、同じレベルとして処理する
        return handle_same_indentation(
            effective_indent_level,
            block,
            list_type,
            blocks,
            list_item_stack,
            current_list_types,
        )
    else:  # インデントレベルが減少
        return handle_decreased_indentation(
            effective_indent_level,
            block,
            list_type,
            blocks,
            list_item_stack,
            current_list_types,
        )


def add_top_level_list_item(block, blocks, list_item_stack):
    """トップレベルのリスト項目を追加する関数"""
    logging.debug(f"Adding top level list item to blocks")
    blocks.append(block)
    list_item_stack[0] = [block]  # スタックをリセット
    return 0


def handle_deeper_indentation(
    effective_indent_level,
    block,
    list_type,
    blocks,
    list_item_stack,
    current_list_types,
):
    """より深いインデントを処理する関数"""
    logging.debug(f"Deeper indent level: {effective_indent_level}")

    # インデックスエラーを防ぐためのチェック
    if (
        effective_indent_level >= len(list_item_stack)
        or not list_item_stack[effective_indent_level - 1]
    ):
        # スタックが不足している場合は調整
        logging.debug(f"Stack adjustment needed for level {effective_indent_level}")
        for i in range(len(list_item_stack), effective_indent_level + 1):
            list_item_stack.append([])

        # 親がない場合はトップレベルに追加
        blocks.append(block)
        list_item_stack[effective_indent_level] = [block]
        logging.debug(f"No parent found, adding to top level blocks")
    else:
        list_item_stack[effective_indent_level].append(block)
        # 親のリストタイプとブロックを取得
        parent_type = current_list_types[effective_indent_level - 1]
        parent_block = list_item_stack[effective_indent_level - 1][-1]
        logging.debug(f"Found parent: type={parent_type}")

        # 親ブロックに子ブロックを追加
        add_child_to_parent(
            parent_type, parent_block, block, effective_indent_level, blocks
        )

    return effective_indent_level


def handle_same_indentation(
    effective_indent_level,
    block,
    list_type,
    blocks,
    list_item_stack,
    current_list_types,
):
    """同じインデントレベルを処理する関数"""
    logging.debug(f"Same indent level: {effective_indent_level}")

    # インデックスエラーを防ぐためのチェック
    if (
        effective_indent_level >= len(list_item_stack)
        or effective_indent_level - 1 >= len(list_item_stack)
        or not list_item_stack[effective_indent_level - 1]
    ):

        # スタックが不足している場合は調整
        logging.debug(f"Stack adjustment needed for level {effective_indent_level}")
        for i in range(len(list_item_stack), effective_indent_level + 1):
            list_item_stack.append([])

        # 親がない場合はトップレベルに追加
        blocks.append(block)
        list_item_stack[effective_indent_level] = [block]
        logging.debug(f"No parent found, adding to top level blocks")
    else:
        list_item_stack[effective_indent_level].append(block)
        # 親のリストタイプとブロックを取得
        parent_type = current_list_types[effective_indent_level - 1]
        parent_block = list_item_stack[effective_indent_level - 1][-1]
        logging.debug(f"Found parent: type={parent_type}")

        # 親ブロックに子ブロックを追加
        add_child_to_parent(
            parent_type, parent_block, block, effective_indent_level, blocks
        )

    return effective_indent_level


def handle_decreased_indentation(
    effective_indent_level,
    block,
    list_type,
    blocks,
    list_item_stack,
    current_list_types,
):
    """インデントレベルが減少した場合の処理関数"""
    logging.debug(f"Decreased indent level: {effective_indent_level}")

    # インデックスエラーを防ぐためのチェック
    if effective_indent_level >= len(list_item_stack):
        # スタックが不足している場合は調整
        logging.debug(f"Stack adjustment needed for level {effective_indent_level}")
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
            logging.debug(f"No parent found, adding to top level blocks")
        else:
            # 親のリストタイプとブロックを取得
            parent_type = current_list_types[effective_indent_level - 1]
            parent_block = list_item_stack[effective_indent_level - 1][-1]
            logging.debug(f"Found parent: type={parent_type}")

            # 親ブロックに子ブロックを追加
            add_child_to_parent(
                parent_type, parent_block, block, effective_indent_level, blocks
            )

    return effective_indent_level


def add_child_to_parent(parent_type, parent_block, child_block, current_level, blocks):
    """親ブロックに子ブロックを追加する関数"""
    # ネストレベルがNotionの制限を超える場合は子ブロックを追加しない
    if current_level > MAX_NEST_LEVEL:
        # 制限を超えた場合はブロックをトップレベルに追加
        blocks.append(child_block)
        logging.debug(
            f"Nest level {current_level} exceeds max {MAX_NEST_LEVEL}, adding to top level"
        )
        return

    if parent_type == "numbered_list_item" and "numbered_list_item" in parent_block:
        # childrenキーがない場合は作成する
        if "children" not in parent_block["numbered_list_item"]:
            parent_block["numbered_list_item"]["children"] = []
        parent_block["numbered_list_item"]["children"].append(child_block)
        logging.debug(
            f"Added child to numbered_list_item parent, children count: "
            f"{len(parent_block['numbered_list_item']['children'])}"
        )
    elif parent_type == "bulleted_list_item" and "bulleted_list_item" in parent_block:
        # childrenキーがない場合は作成する
        if "children" not in parent_block["bulleted_list_item"]:
            parent_block["bulleted_list_item"]["children"] = []
        parent_block["bulleted_list_item"]["children"].append(child_block)
        logging.debug(
            f"Added child to bulleted_list_item parent, children count: "
            f"{len(parent_block['bulleted_list_item']['children'])}"
        )


def clean_list_item_stack(list_item_stack):
    """スタックから空の子リストを削除する関数"""
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
            rich_text_property = get_rich_text_property(block)

            if not rich_text_property:
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
                clean_child_blocks(block, rich_text_property)

        except Exception as e:
            logging.warning(f"Error cleaning block: {str(e)}")
            # エラーが発生した場合は安全のためブロックをスキップ
            continue

    return cleaned_blocks


def get_rich_text_property(block):
    """ブロックからリッチテキストプロパティを取得する関数"""
    for block_type in BLOCK_TYPES:
        if block_type in block:
            return block_type
    return None


def clean_child_blocks(block, rich_text_property):
    """子ブロックを浄化する関数"""
    # 子ブロックも同様に浄化
    clean_children = []
    for child_block in block[rich_text_property]["children"]:
        # 子ブロックのタイプを特定
        child_type = get_rich_text_property(child_block)

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


def process_image(image_alt, image_url, blocks):
    """画像ブロックを処理する関数"""
    logging.debug(f"Processing image: alt='{image_alt}', url='{image_url}'")

    # 画像URLが空の場合はスキップ
    if not image_url:
        logging.debug("Empty image URL, skipping")
        return True

    # 画像ブロックを作成
    blocks.append(
        {
            "object": "block",
            "type": "image",
            "image": {
                "type": "external",
                "external": {"url": image_url},
                "caption": (
                    [{"type": "text", "text": {"content": image_alt}}]
                    if image_alt
                    else []
                ),
            },
        }
    )

    return True
