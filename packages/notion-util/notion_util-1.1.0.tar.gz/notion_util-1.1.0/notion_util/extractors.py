"""
Notionの関連URLからページIDなどを抽出するユーティリティ関数。
"""

import re


def extract_notion_page_id(url):
    """
    NotionのURLからページIDを抽出します。

    Args:
        url (str): NotionのURL

    Returns:
        str: 抽出されたページID。見つからない場合はNone。
    """
    # Find URLs that starts with "https://www.notion.so" and extracts the UUID
    patterns = [
        r"https://www\.notion\.so/[^/]+/[^/]+-([a-f0-9]{32})",
        r"https://www\.notion\.so/[^/]+/([a-f0-9]{32})",
        r"https://www\.notion\.so/[^/]+-([a-f0-9]{32})",
        r"https://www\.notion\.so/([a-f0-9]{32})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def extract_notion_page_ids(message):
    """
    テキストメッセージからNotionのページIDをすべて抽出します。

    Args:
        message (str): Notionの URL を含むテキスト

    Returns:
        list: 抽出されたページIDのリスト
    """
    patterns = [
        r"https://www\.notion\.so/[^/]+/[^/]+-([a-f0-9]{32})",
        r"https://www\.notion\.so/[^/]+/([a-f0-9]{32})",
        r"https://www\.notion\.so/[^/]+-([a-f0-9]{32})",
        r"https://www\.notion\.so/([a-f0-9]{32})",
    ]

    page_ids = []
    for pattern in patterns:
        matches = re.findall(pattern, message)
        if matches:
            page_ids.extend(matches)
    return page_ids


def find_links(text):
    """
    テキスト内のリンクを検出します。

    Args:
        text (str): リンクを含む可能性のあるテキスト

    Returns:
        tuple: (リンクタイプ, リンクテキスト, URL)のタプル。リンクがない場合はNone。
    """
    pattern_url = re.compile(r"(https?://[^\s)]+)")
    pattern_loose = re.compile(r"\[([^\[\]]+)\]\(([^)]+)\)")
    markdown_match = pattern_loose.search(text)
    url_match = pattern_url.search(text)

    if markdown_match:
        return ("markdown", markdown_match.group(1), markdown_match.group(2))
    elif url_match:
        return ("url", url_match.group(1), url_match.group(1))
    else:
        return None
