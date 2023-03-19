from datetime import datetime, timezone, timedelta
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NoteFilter, NotesMetadataResultSpec
import os

client = EvernoteClient(
    token=os.environ.get("EVERNOTE_KEY"),
    sandbox=False
)

store = client.get_note_store()
notebook_list = store.listNotebooks()

target_notebook_name = "03.フライヤー"
max_notes_to_fetch = 3

for notebook in notebook_list:
    if notebook.name == target_notebook_name:
        print(f'ノートブック名: {notebook.name}')

        filter = NoteFilter()
        filter.notebookGuid = notebook.guid

        spec = NotesMetadataResultSpec()
        spec.includeTitle = True
        spec.includeCreated = True
        spec.includeAttributes = True

        notes_metadata_list = store.findNotesMetadata(
            filter,
            0,
            max_notes_to_fetch,
            spec
        )

        print(f'ノートブックに含まれるノートの数: {notes_metadata_list.totalNotes}')

        for note_meta_data in notes_metadata_list.notes:
            print(f'  ノートのタイトル: {note_meta_data.title}')

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

            if note.resources is not None:
                for resource in note.resources:
                    print(f'    添付データファイル名: {resource.attributes.fileName}')
                    print(f'      データタイプ: {resource.mime}')

        break
