# Update `process_wonjunim_words.py` to use Context and Titles

## User Review Required
> [!IMPORTANT]
> The user specified `gpt-5` as the model. This model might not be publicly available via the standard OpenAI API yet. If the script fails with a model error, we will need to revert to `gpt-4o` or similar. I will proceed with `gpt-5` as requested.

## Proposed Changes

### `process_wonjunim_words.py`

#### [MODIFY] `process_wonjunim_words.py`
- **Context Loading**: Add functionality to read `d:\AntiGravity\scriptproject\원주님소개.txt` and inject it into the system prompt.
- **Refine Text Function**: 
    - Update prompt to include the "Context Document".
    - Request a "Summary Title" to be generated as the first line (e.g., `# TITLE: ...`).
- **DOCX Creation**:
    - Add the original filename at the top of the document.
    - Parse the content to extract the `# TITLE: ...` line and use it as the main document title.
    - Organize the rest of the content (Headings, Bullets) as before.

## Verification Plan

### Automated Tests
- Run the script `python process_wonjunim_words.py`.
- Check if it runs without "Invalid Model" error.
- Check `원주님말씀.doc\2013` for generated files.
- Open one generated DOCX (or check file size/log output) to verify:
    - Filename is at the top.
    - A summary title exists.
    - Content is in "Written Style" (文語體).
