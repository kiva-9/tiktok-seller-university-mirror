#!/usr/bin/env python3
"""debug_gdocs.py — 调试 Google Docs API 文档结构"""
import json
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/documents"]

def main():
    doc_id = os.environ.get("GOOGLE_DOCS_DOCUMENT_ID", "")
    if not doc_id:
        print("设置 GOOGLE_DOCS_DOCUMENT_ID 环境变量")
        sys.exit(1)

    sa_json = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
    info = json.loads(sa_json)
    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    service = build("docs", "v1", credentials=creds)

    doc = service.documents().get(documentId=doc_id).execute()
    body = doc.get("body", {}).get("content", [])

    print(f"文档标题: {doc.get('title')}")
    print(f"body.content 元素数: {len(body)}")
    print(f"最后一个元素的 endIndex: {body[-1]['endIndex']}")
    print()
    print("body.content 结构:")
    for i, el in enumerate(body):
        print(f"  [{i}] {json.dumps(el, ensure_ascii=False)[:200]}")

if __name__ == "__main__":
    main()
