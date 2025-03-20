"""
NotionのAPIとの通信を行うクライアントクラスを提供します。
"""

import os
import logging
import json
import re
import time
from typing import Optional, List, Dict, Any, Union

# リトライ回数と待機時間の設定
MAX_RETRIES = 3
RETRY_DELAY = 0.5  # 秒

# NotionのAPIエンドポイント
API_BASE_URL = "https://api.notion.com/v1"

# 再帰的に取得するブロックタイプ
recursive_types = [
    "bulleted_list_item",
    "numbered_list_item",
    "quote",
    "toggle",
    "callout",
    "synced_block",
]

# 再帰的に取得しないブロックタイプ
skip_types = [
    "page",
    "child_page",
    "child_database",
    "link_to_page",
    "embed",
    "bookmark",
    "table_of_contents",
]


class Notion:
    """
    NotionのAPIと通信するためのクライアントクラス。
    """

    def __init__(self, api_key=None):
        """
        Notionクライアントを初期化します。

        Args:
            api_key (str, optional): NotionのAPIキー。指定されていない場合は環境変数から取得します。
        """
        self.api_key = api_key or os.environ.get("NOTION_SECRET")
        if not self.api_key:
            raise ValueError(
                "APIキーが指定されていません。api_key引数または環境変数NOTION_SECRETを設定してください。"
            )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }
        logging.debug("Notion clientを初期化しました")

    def _request(self, method, endpoint, data=None, params=None):
        """
        NotionのAPIにリクエストを送信します。

        Args:
            method (str): HTTPメソッド（'GET', 'POST', 'PATCH', 'DELETE'）
            endpoint (str): APIのエンドポイント
            data (dict, optional): リクエストボディ
            params (dict, optional): クエリパラメータ

        Returns:
            dict: レスポンスのJSON
        """
        import requests

        url = f"{API_BASE_URL}{endpoint}"
        logging.debug(f"{method} {url}")

        retries = 0
        while retries < MAX_RETRIES:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=data,
                    params=params,
                )
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code == 429:  # Rate limit
                    retry_after = int(response.headers.get("Retry-After", RETRY_DELAY))
                    logging.warning(
                        f"Rate limit exceeded. Retrying after {retry_after} seconds."
                    )
                    time.sleep(retry_after)
                    retries += 1
                    continue
                elif response.status_code >= 500:  # Server error
                    if retries < MAX_RETRIES - 1:
                        wait_time = RETRY_DELAY * (2**retries)
                        logging.warning(
                            f"Server error {response.status_code}. Retrying after {wait_time} seconds."
                        )
                        time.sleep(wait_time)
                        retries += 1
                        continue
                logging.error(f"HTTP Error: {e}")
                if hasattr(response, "text"):
                    logging.error(f"Response: {response.text}")
                raise
            except requests.exceptions.RequestException as e:
                if retries < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (2**retries)
                    logging.warning(
                        f"Request failed: {e}. Retrying after {wait_time} seconds."
                    )
                    time.sleep(wait_time)
                    retries += 1
                    continue
                logging.error(f"Request Exception: {e}")
                raise

        raise Exception(f"Failed after {MAX_RETRIES} retries")

    def get_block(self, block_id):
        """
        指定されたIDのブロックを取得します。

        Args:
            block_id (str): 取得するブロックのID

        Returns:
            dict: ブロック情報
        """
        return self._request("GET", f"/blocks/{block_id}")

    def get_page(self, page_id):
        """
        指定されたIDのページ情報を取得します。

        Args:
            page_id (str): 取得するページのID

        Returns:
            dict: ページ情報
        """
        return self._request("GET", f"/pages/{page_id}")

    def get_database(self, database_id):
        """
        指定されたIDのデータベース情報を取得します。

        Args:
            database_id (str): 取得するデータベースのID

        Returns:
            dict: データベース情報
        """
        return self._request("GET", f"/databases/{database_id}")

    def get_database_pages(self, database_id, filter_params=None):
        """
        データベース内のページをクエリします。

        Args:
            database_id (str): データベースのID
            filter_params (dict, optional): フィルタパラメータ

        Returns:
            list: データベース内のページリスト
        """
        data = filter_params or {}
        return self._request("POST", f"/databases/{database_id}/query", data=data)

    def get_block_children(self, block_id, page_size=100, start_cursor=None):
        """
        ブロックの子ブロックを取得します。

        Args:
            block_id (str): 親ブロックのID
            page_size (int, optional): 1回のリクエストで取得する最大数
            start_cursor (str, optional): ページネーションカーソル

        Returns:
            dict: 子ブロックのリストとページネーション情報
        """
        params = {"page_size": page_size}
        if start_cursor:
            params["start_cursor"] = start_cursor

        return self._request("GET", f"/blocks/{block_id}/children", params=params)

    def get_all_block_children(self, block_id):
        """
        ブロックのすべての子ブロックを取得します（ページネーション対応）。

        Args:
            block_id (str): 親ブロックのID

        Returns:
            list: すべての子ブロックのリスト
        """
        has_more = True
        cursor = None
        all_children = []

        while has_more:
            response = self.get_block_children(block_id, start_cursor=cursor)
            all_children.extend(response.get("results", []))
            has_more = response.get("has_more", False)
            cursor = response.get("next_cursor")

        return all_children

    def recursive_get_blocks(self, block_id, depth=10, current_depth=1):
        """
        ブロックとその子孫ブロックを再帰的に取得します。

        Args:
            block_id (str): 親ブロックのID
            depth (int, optional): 再帰的に取得する深さの最大値
            current_depth (int, optional): 現在の深さ

        Returns:
            list: 取得したブロックのリスト（子孫ブロックを含む）
        """
        if current_depth > depth:
            return []

        children = self.get_all_block_children(block_id)
        all_blocks = []

        for child in children:
            all_blocks.append(child)
            child_id = child.get("id")
            block_type = child.get("type")

            # 再帰的に取得すべきブロックタイプの場合
            if block_type in recursive_types and child_id:
                # 特定のブロックタイプはスキップする
                if block_type in skip_types:
                    continue

                # 再帰的に子ブロックを取得
                child_blocks = self.recursive_get_blocks(
                    child_id, depth, current_depth + 1
                )
                if child_blocks:
                    # 子ブロックを親ブロックの適切な場所に追加
                    if (
                        block_type == "bulleted_list_item"
                        and "bulleted_list_item" in child
                    ):
                        if "children" not in child["bulleted_list_item"]:
                            child["bulleted_list_item"]["children"] = []
                        child["bulleted_list_item"]["children"].extend(child_blocks)
                    elif (
                        block_type == "numbered_list_item"
                        and "numbered_list_item" in child
                    ):
                        if "children" not in child["numbered_list_item"]:
                            child["numbered_list_item"]["children"] = []
                        child["numbered_list_item"]["children"].extend(child_blocks)
                    elif block_type == "quote" and "quote" in child:
                        if "children" not in child["quote"]:
                            child["quote"]["children"] = []
                        child["quote"]["children"].extend(child_blocks)
                    elif block_type == "toggle" and "toggle" in child:
                        if "children" not in child["toggle"]:
                            child["toggle"]["children"] = []
                        child["toggle"]["children"].extend(child_blocks)
                    elif block_type == "callout" and "callout" in child:
                        if "children" not in child["callout"]:
                            child["callout"]["children"] = []
                        child["callout"]["children"].extend(child_blocks)
                    elif block_type == "synced_block" and "synced_block" in child:
                        if "children" not in child["synced_block"]:
                            child["synced_block"]["children"] = []
                        child["synced_block"]["children"].extend(child_blocks)

        return all_blocks

    def create_page(self, parent, properties, children=None):
        """
        新しいページを作成します。

        Args:
            parent (dict): 親ページまたはデータベースの情報
            properties (dict): ページのプロパティ（タイトルなど）
            children (list, optional): ページの子ブロックのリスト

        Returns:
            dict: 作成されたページ情報
        """
        data = {
            "parent": parent,
            "properties": properties,
        }
        if children:
            data["children"] = children

        return self._request("POST", "/pages", data=data)

    def append_blocks(self, block_id, children):
        """
        既存のブロックに子ブロックを追加します。

        Args:
            block_id (str): 親ブロックのID
            children (list): 追加する子ブロックのリスト

        Returns:
            dict: 追加結果
        """
        return self._request(
            "PATCH", f"/blocks/{block_id}/children", data={"children": children}
        )

    def update_page(self, page_id, properties):
        """
        既存のページを更新します。

        Args:
            page_id (str): 更新するページのID
            properties (dict): 更新するプロパティ

        Returns:
            dict: 更新されたページ情報
        """
        return self._request(
            "PATCH", f"/pages/{page_id}", data={"properties": properties}
        )

    def delete_block(self, block_id):
        """
        指定されたブロックを削除します（正確にはアーカイブします）。

        Args:
            block_id (str): 削除するブロックのID

        Returns:
            dict: 削除結果
        """
        return self._request("DELETE", f"/blocks/{block_id}")

    def update_block(self, block_id, block_data):
        """
        既存のブロックを更新します。

        Args:
            block_id (str): 更新するブロックのID
            block_data (dict): 更新するブロックデータ

        Returns:
            dict: 更新されたブロック情報
        """
        return self._request("PATCH", f"/blocks/{block_id}", data=block_data)

    # ----- サンプルコードとの互換性のための追加メソッド -----

    def get_page_markdown(self, url_or_id, recursive=True, depth=3):
        """
        NotionのURLまたはページIDからマークダウンテキストを取得します。

        util.pyのget_page_markdown関数をラッパーします。

        Args:
            url_or_id (str): NotionのURLまたはページID
            recursive (bool, optional): 再帰的にブロックを取得するかどうか
            depth (int, optional): 再帰的に取得する深さの最大値

        Returns:
            str: マークダウンテキスト
        """
        from .util import get_page_markdown

        return get_page_markdown(url_or_id, recursive, depth)

    def create_notion_page(self, database_id, title, properties=None):
        """
        Notionデータベース内に新しいページを作成します。

        example/create_page_from_markdown.pyとの互換性のために追加。

        Args:
            database_id (str): 親データベースのID
            title (str): ページのタイトル
            properties (dict, optional): その他のプロパティ

        Returns:
            dict: 作成されたページ情報
        """
        properties = properties or {}
        # タイトルプロパティを追加
        properties["title"] = {"title": [{"text": {"content": title}}]}

        # 親データベースの情報を設定
        parent = {"database_id": database_id}

        return self.create_page(parent, properties)

    def append_blocks_to_page(self, page_id, blocks):
        """
        既存のページにブロックを追加します。

        example/create_page_from_markdown.pyとの互換性のために追加。

        Args:
            page_id (str): ページのID
            blocks (list): 追加するブロックのリスト

        Returns:
            dict: 追加結果
        """
        return self.append_blocks(page_id, blocks)
