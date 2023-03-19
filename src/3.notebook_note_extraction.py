from datetime import datetime, timezone, timedelta
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import os
from lxml import etree
import re


def enml_to_text(enml_content):
    enml_content = re.sub(r'<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">', '', enml_content)
    root = etree.fromstring(enml_content)

    summary_text = ""
    start_extracting = False

    # 要約の部分だけプレーンテキストとして抽出する
    for elem in root.iter("h1", "div"):
        if elem.tag == "h1" and elem.text == "要約":
            start_extracting = True
            continue

        if start_extracting and elem.tag == "h1":
            break

        if start_extracting:
            summary_text += etree.tostring(elem, method="text", encoding="utf-8").decode("utf-8").strip()

        if start_extracting and elem.tag == "div":
            # 段落の終わりに改行を追加
            summary_text += "\n"

    return summary_text


# EvernoteClientを初期化します。環境変数からアクセストークンを取得します。
client = EvernoteClient(
    token=os.environ.get("EVERNOTE_KEY"),
    sandbox=False
)

# NoteStoreを取得します。
store = client.get_note_store()

# ノートブックのリストを取得します。
notebook_list = store.listNotebooks()

# 取得したいノートブックの名前を指定します。
target_notebook_name = "03.フライヤー"

# 取得するノートの最大数を指定します。
max_notes_to_fetch = 3

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
            print("#" * 60)
            print("#" * 60)
            print("#" * 60)
            print(f'1.タイトル: {note.title}')
            print(f'2.作成日時: {datetime.fromtimestamp(note.created / 1000, timezone(timedelta(hours=9)))}')
            enml_content = note.content
            plain_text_content = enml_to_text(enml_content)
            print('3.内容(プレーンテキスト)')
            print(f'{plain_text_content}')

        break
