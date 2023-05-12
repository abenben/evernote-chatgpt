from datetime import datetime, timezone, timedelta
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import os
from lxml import etree
import re
from bs4 import BeautifulSoup


def enml_to_text(enml_content):
    # XHTMLからプレーンテキストを取得するために、XHTMLタグを削除する
    enml_content = re.sub(r'<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">', '', enml_content)
    root = etree.fromstring(enml_content)

    # 段落の終わりに改行を追加
    for elem in root.xpath("//div"):
        elem.tail = "\n" + (elem.tail or "")

    text = etree.tostring(root, method="text", encoding="utf-8").decode("utf-8").strip()
    return text


# EvernoteClientを初期化します。環境変数からアクセストークンを取得します。
client = EvernoteClient(
    token=os.environ.get("EVERNOTE_KEY"),
    sandbox=False
)


def extract_urls_and_tabs(enml_content):
    soup = BeautifulSoup(enml_content, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))

    tabs = []
    for tab in soup.find_all('tab'):
        tabs.append(tab.text)

    return urls, tabs


# NoteStoreを取得します。
store = client.get_note_store()

# ノートブックのリストを取得します。
notebook_list = store.listNotebooks()

# 取得したいノートブックの名前を指定します。
target_notebook_name = "03.フライヤー"

# 取得するノートの最大数を指定します。
max_notes_to_fetch = 2000

# ノートブックリストをループして、目的のノートブックを見つけます。
for notebook in notebook_list:
    if notebook.name == target_notebook_name:
        print(f'ノートブック名: {notebook.name}')

        # NoteFilterを作成し、指定したノートブックのGUIDを設定します。
        filter = NoteFilter()
        filter.notebookGuid = notebook.guid  # ノートブックの GUID を指定
        filter.ascending = False  # ノートを降順（最新順）で取得する

        # 取得するノートのメタデータに含めるフィールドを設定します。
        spec = NotesMetadataResultSpec()
        spec.includeTitle = True
        spec.includeCreated = True
        spec.includeAttributes = True

        # 指定したフィルタとスペックでノートのメタデータリストを取得します。
        notes_metadata_list = store.findNotesMetadata(
            filter,
            0,
            max_notes_to_fetch,
            spec
        )

        print(f'ノートブックに含まれるノートの数: {notes_metadata_list.totalNotes}')

        # メタデータリストからノートをループして、詳細を表示します。
        for note_meta_data in notes_metadata_list.notes:
            # ノートのGUIDを使って、ノートの詳細を取得します。
            note = store.getNote(
                note_meta_data.guid,
                True,
                True,
                True,
                True
            )
            print(f'1.タイトル: {note.title}')
            print(f'2.作成日時: {datetime.fromtimestamp(note.created / 1000, timezone(timedelta(hours=9)))}')
            enml_content = note.content

            urls, tabs = extract_urls_and_tabs(enml_content)
            print(f'3.URLs:{len(urls)}')
            for url in urls:
                print(url)
            print(f'4.Tabs: {len(tabs)}')
            for tab in tabs:
                print(tab)
            # plain_text_content = enml_to_text(enml_content)
            # print('3.内容(プレーンテキスト)')
            # print(f'{plain_text_content}')

        break
