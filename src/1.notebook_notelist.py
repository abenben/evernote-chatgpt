from datetime import datetime, timezone, timedelta
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import os

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
        filter.notebookGuid = notebook.guid

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
            print(f'  ノートのタイトル: {note_meta_data.title}')

            # ノートのGUIDを使って、ノートの詳細を取得します。
            note = store.getNote(
                note_meta_data.guid,
                True,
                True,
                True,
                True
            )
            print(f'    タイトル: {note.title}')
            print(f'    作成日時: {datetime.fromtimestamp(note.created / 1000, timezone(timedelta(hours=9)))}')
            print(f'    内容(XHTML): {note.content[0:64]}')

            # ノートに添付されたリソースがあれば、それらを表示します。
            if note.resources is not None:
                for resource in note.resources:
                    print(f'    添付データファイル名: {resource.attributes.fileName}')
                    print(f'      データタイプ: {resource.mime}')

        break
