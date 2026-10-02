# Private CDP resume editor

Double-click **Start Resume Editor.cmd** in the project folder. Your browser opens the editor. Keep its small launcher window running while you edit; choose **Close editor** or close that window to stop the editor.

The editor runs on this computer only. It needs Python 3; the launcher automatically uses the Python already bundled on Prabir's computer, or the Windows Python launcher on another computer. No packages or hosting account are needed.

## Everyday editing

1. Choose a section on the left and edit complete text fields.
2. Add, remove, or reorder responsibility bullets with the buttons.
3. Check the live preview. Resolve any layout warnings before publishing.
4. **Save draft** saves privately on this computer. **Restore saved draft** brings it back on a later visit.
5. **Download HTML** creates a standalone resume. Open it and use Print / Save as PDF.
6. **Export backup** and **Import backup** move a draft between computers.

## Connect and publish

Choose **Connect GitHub** and follow the instructions in the editor. Use a fine-grained personal access token from the `prabirbera23` account, restricted to the `prabir-bera-resumes` repository with Contents read/write permission. Paste it into the editor, never into chat or a source file.

The token stays in the local server's memory, is used only with `api.github.com`, and is forgotten when the server stops. The editor checks the GitHub account before allowing publishing. Reconnect after restarting the editor.

**Publish changes** shows a confirmation, then updates only `content/cdp.json`. GitHub Actions rebuilds the public resume. Allow about a minute for deployment. If another edit has been published since you loaded the resume, GitHub rejects the stale update. Export a backup, load the latest published version, and reapply your edits.

Your shared link remains https://prabirbera23.github.io/prabir-bera-resumes/cdp.html.

## Files

- `content/cdp.json`: editable CDP text, now used instead of the old numbered Markdown fields.
- `templates/cdp-editor.html`: current three-page design with stable editable areas.
- `content/cdp.draft.json`: private local draft; excluded from Git.
- `scripts/editor_server.py`: private backend, bound to `127.0.0.1` only.
- `scripts/editor_model.py`: validation and safe text rendering shared by editor and publishing build.
- `editor/public/`: editor interface.

The other resume designs still use their existing Markdown files. The older `content/cdp.md` is retained as a historical reference and no longer controls the public CDP version.

The editor retains the current three-page template. Long additions may need layout changes; the preview warns and blocks publishing when text overflows. It does not silently remove text or automatically add pages.
