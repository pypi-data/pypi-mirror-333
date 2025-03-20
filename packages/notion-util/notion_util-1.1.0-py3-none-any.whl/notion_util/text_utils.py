"""
テキスト処理とマークダウン変換に関するユーティリティ関数。
"""

import re
import logging


def lint_to_blocks(line):
    """
    マークダウン形式のテキスト行をNotionのリッチテキストブロックに変換します。

    Args:
        line (str): 処理するマークダウンテキスト

    Returns:
        list: Notionリッチテキストブロックのリスト
    """
    blocks = []
    # プレーンなテキストも含めて全て検出しparagraphを完成させる

    # マークダウン要素をNotionブロックに変換する関数
    def create_text_block(content, annotations=None, link=None):
        if not content:
            return None

        default_annotations = {
            "bold": False,
            "italic": False,
            "strikethrough": False,
            "underline": False,
            "code": False,
            "color": "default",
        }

        if annotations:
            default_annotations.update(annotations)

        block = {
            "type": "text",
            "text": {"content": content},
            "annotations": default_annotations,
        }

        if link:
            block["text"]["link"] = {"url": link}

        return block

    # テキスト内の装飾を再帰的に処理する関数
    def process_text_decorations(text):
        if not text or not text.strip():
            return [create_text_block(text)]

        result_blocks = []

        # エスケープ文字の処理
        escaped_pattern = re.search(r"\\([*_`~\[\]\(\)\\])", text)
        if escaped_pattern:
            before_escaped = text[: escaped_pattern.start()]
            escaped_char = escaped_pattern.group(1)  # エスケープされた文字
            after_escaped = text[escaped_pattern.end() :]

            # エスケープ前のテキストを処理
            if before_escaped:
                result_blocks.extend(process_text_decorations(before_escaped))

            # エスケープされた文字を通常の文字として追加
            block = create_text_block(escaped_char)
            if block:
                result_blocks.append(block)

            # エスケープ後のテキストを処理
            if after_escaped:
                result_blocks.extend(process_text_decorations(after_escaped))

            return result_blocks

        # リンクの処理（最初に処理）
        link_match = re.search(r"\[([^\[\]]+)\]\(([^)]+)\)", text)
        if link_match:
            before_link = text[: link_match.start()]
            link_text = link_match.group(1)
            link_url = link_match.group(2)
            after_link = text[link_match.end() :]

            # リンク前のテキストを処理
            if before_link:
                result_blocks.extend(process_text_decorations(before_link))

            # リンクテキスト内の装飾を処理
            link_text_blocks = process_text_decorations(link_text)
            # リンクテキスト内の装飾を保持しつつ、リンクを適用
            for block in link_text_blocks:
                if block:  # None値をスキップ
                    block["text"]["link"] = {"url": link_url}
                    result_blocks.append(block)

            # リンク後のテキストを処理
            if after_link:
                result_blocks.extend(process_text_decorations(after_link))

            return result_blocks

        # 太字とコードの組み合わせ処理（**`text`**）- 最初に処理
        bold_code_match = re.search(r"\*\*`(.*?)`\*\*", text)
        if bold_code_match:
            before_bold_code = text[: bold_code_match.start()]
            code_content = bold_code_match.group(1)
            after_bold_code = text[bold_code_match.end() :]

            # 太字+コード前のテキストを処理
            if before_bold_code:
                result_blocks.extend(process_text_decorations(before_bold_code))

            # 太字+コードのブロックを作成
            block = create_text_block(
                code_content, annotations={"bold": True, "code": True}
            )
            if block:
                result_blocks.append(block)

            # 太字+コード後のテキストを処理
            if after_bold_code:
                result_blocks.extend(process_text_decorations(after_bold_code))

            return result_blocks

        # URL直接記述の処理
        url_match = re.search(r"(https?://[^\s)]+)", text)
        if url_match:
            before_url = text[: url_match.start()]
            url = url_match.group(1)
            after_url = text[url_match.end() :]

            # URL前のテキストを処理
            if before_url:
                result_blocks.extend(process_text_decorations(before_url))

            # URLをリンクとして追加
            block = create_text_block(url, link=url)
            if block:  # None値をスキップ
                result_blocks.append(block)

            # URL後のテキストを処理
            if after_url:
                result_blocks.extend(process_text_decorations(after_url))

            return result_blocks

        # 打ち消し線の処理 (~~text~~)
        strike_match = re.search(r"~~(.*?)~~", text)
        if strike_match:
            before_strike = text[: strike_match.start()]
            strike_content = strike_match.group(1)
            after_strike = text[strike_match.end() :]

            # 打ち消し線前のテキストを処理
            if before_strike:
                result_blocks.extend(process_text_decorations(before_strike))

            # 打ち消し線ブロックを追加（内部の装飾も再帰的に処理）
            if strike_content:
                # リンクを含む取り消し線テキストを特別に処理
                if "[" in strike_content and "](" in strike_content:
                    link_pattern = re.search(
                        r"\[([^\[\]]+)\]\(([^)]+)\)", strike_content
                    )
                    if link_pattern:
                        before_link = strike_content[: link_pattern.start()]
                        link_text = link_pattern.group(1)
                        link_url = link_pattern.group(2)
                        after_link = strike_content[link_pattern.end() :]

                        # リンク前のテキストを取り消し線付きで処理
                        if before_link:
                            block = create_text_block(
                                before_link, annotations={"strikethrough": True}
                            )
                            if block:
                                result_blocks.append(block)

                        # リンクテキストを取り消し線付きで処理
                        link_block = create_text_block(
                            link_text,
                            annotations={"strikethrough": True},
                            link=link_url,
                        )
                        if link_block:
                            result_blocks.append(link_block)

                        # リンク後のテキストを取り消し線付きで処理
                        if after_link:
                            block = create_text_block(
                                after_link, annotations={"strikethrough": True}
                            )
                            if block:
                                result_blocks.append(block)
                    else:
                        # 通常の取り消し線処理
                        strike_blocks = process_text_decorations(strike_content)
                        for block in strike_blocks:
                            if block:  # None値をスキップ
                                block["annotations"]["strikethrough"] = True
                                result_blocks.append(block)
                else:
                    # 通常の取り消し線処理
                    strike_blocks = process_text_decorations(strike_content)
                    for block in strike_blocks:
                        if block:  # None値をスキップ
                            block["annotations"]["strikethrough"] = True
                            result_blocks.append(block)
            else:
                # 空の取り消し線の場合は空のブロックを追加
                result_blocks.append(
                    create_text_block("", annotations={"strikethrough": True})
                )

            # 打ち消し線後のテキストを処理
            if after_strike:
                result_blocks.extend(process_text_decorations(after_strike))

            return result_blocks

        # コードの処理
        code_match = re.search(r"`(.*?)`", text)
        if code_match:
            before_code = text[: code_match.start()]
            code_content = code_match.group(1)
            after_code = text[code_match.end() :]

            # コード前のテキストを処理
            if before_code:
                result_blocks.extend(process_text_decorations(before_code))

            # コードブロックを追加
            # 太字とコードの組み合わせに対応するため、親の装飾情報を継承できるようにする
            block = create_text_block(code_content, annotations={"code": True})
            if block:  # None値をスキップ
                result_blocks.append(block)

            # コード後のテキストを処理
            if after_code:
                result_blocks.extend(process_text_decorations(after_code))

            return result_blocks

        # 太字の処理
        bold_match = re.search(r"\*\*(.*?)\*\*", text)
        if bold_match:
            before_bold = text[: bold_match.start()]
            bold_content = bold_match.group(1)
            after_bold = text[bold_match.end() :]

            # 太字前のテキストを処理
            if before_bold:
                result_blocks.extend(process_text_decorations(before_bold))

            # 太字ブロックを追加（内部の装飾も再帰的に処理）
            bold_blocks = process_text_decorations(bold_content)
            for block in bold_blocks:
                if block:  # None値をスキップ
                    block["annotations"]["bold"] = True
                    result_blocks.append(block)

            # 太字後のテキストを処理
            if after_bold:
                result_blocks.extend(process_text_decorations(after_bold))

            return result_blocks

        # アンダーラインの処理
        underline_match = re.search(r"__(.*?)__", text)
        if underline_match:
            before_underline = text[: underline_match.start()]
            underline_content = underline_match.group(1)
            after_underline = text[underline_match.end() :]

            # アンダーライン前のテキストを処理
            if before_underline:
                result_blocks.extend(process_text_decorations(before_underline))

            # アンダーラインブロックを追加（内部の装飾も再帰的に処理）
            underline_blocks = process_text_decorations(underline_content)
            for block in underline_blocks:
                if block:  # None値をスキップ
                    block["annotations"]["underline"] = True
                    result_blocks.append(block)

            # アンダーライン後のテキストを処理
            if after_underline:
                result_blocks.extend(process_text_decorations(after_underline))

            return result_blocks

        # 斜体の処理 (特に注意: 斜体を最後に処理)
        italic_match = re.search(r"\*(.*?)\*", text)
        if italic_match:
            before_italic = text[: italic_match.start()]
            italic_content = italic_match.group(1)
            after_italic = text[italic_match.end() :]

            # 斜体前のテキストを処理
            if before_italic:
                result_blocks.extend(process_text_decorations(before_italic))

            # 斜体ブロックを追加（内部の装飾も再帰的に処理）
            italic_blocks = process_text_decorations(italic_content)
            for block in italic_blocks:
                if block:  # None値をスキップ
                    block["annotations"]["italic"] = True
                    result_blocks.append(block)

            # 斜体後のテキストを処理
            if after_italic:
                result_blocks.extend(process_text_decorations(after_italic))

            return result_blocks

        # 装飾なしのプレーンテキスト
        block = create_text_block(text)
        if block:  # None値をスキップ
            return [block]
        return []

    # 行全体を処理
    if not line.strip():
        return None

    # None値を取り除く
    blocks = [block for block in process_text_decorations(line) if block is not None]
    return blocks
