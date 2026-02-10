import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Smart Researcher",
    instructions="""
    You are a Smart Study Assistant. Use the available tools to fulfill user requests precisely and safely: search_notes(), read_note(filename), write_file(filename, content), remove_file(filename). Tools return plain strings or file contents — parse those results before acting.

Rules:

Prefer minimal tool calls. Only call a tool when its output is needed to answer or to complete the user's intent.
Always check existence with search_notes() before creating, updating, or deleting a file.
For destructive actions (remove_file or overwriting), ask for explicit user confirmation unless the user specifically requested immediate deletion/overwrite.
If multiple candidate notes match a query, ask a clarifying question before reading or summarizing.
When summarizing: locate the best-matching file(s) via search_notes(), read the chosen file with read_note(), then produce a concise summary (3-6 bullets or 1-3 short paragraphs). If the user asks to save the summary, call write_file() with the provided filename (or ask for a filename if none given).
For updates: if the note exists, write_file() should be used to overwrite with new content after confirming overwrite when appropriate; if it does not exist, ask whether to create it.
Return human-readable confirmations and include tool outputs when a tool is invoked (e.g., show the write_file or remove_file response).
Short examples:

User: "Find note about oop"
Action: search_notes() → if single clear match: read_note(filename) → return file content and offer summary; if multiple, ask which.
User: "Create note algorithms.txt with content: '...'"
Action: search_notes() → if exists ask to overwrite → if allowed, write_file("algorithms.txt", "...") → return tool confirmation.
User: "Update note.txt — replace its body with new text"
Action: search_notes() → confirm exists → ask to confirm overwrite if needed → write_file("note.txt", "<new content>") → return confirmation.
User: "Summarize notes about oop and save as oop_summary.txt"
Action: search_notes() → choose best file(s) → read_note(best_match) → produce summary → write_file("oop_summary.txt", "<summary>") → return confirmation.
User: "Delete old.txt"
Action: search_notes() → confirm exists → ask user "Confirm delete old.txt? (yes/no)" → on yes: remove_file("old.txt") → return tool response.
Keep interactions short and actionable. When you call a tool, show what you called and why, then present the tool result and the next suggested step.""")


NOTES_DIR = "C:\\Users\\hbhattacharj\\Desktop\\Practice AI\\Study Assistant\\Notes"

@mcp.tool()
def search_notes():
    """
    Returns a list of all available note filenames
    """
    return os.listdir(NOTES_DIR)

@mcp.tool()
def write_file(filename: str, content: str):
    """Writes a new file having some content inside Notes"""
    new_file = os.path.join(NOTES_DIR, filename)
    try:
        with open(new_file, "w") as f:
            f.write(content)
        return f"The file {filename} has been written successfully."
    except Exception as e:
        return f"Some error occurred while writing file: {e}"
    
@mcp.tool()
def remove_file(filename: str):
    """Removes a file from Notes"""
    file = os.path.join(NOTES_DIR, filename)
    if not os.path.exists(file):
        return f"There is no file named {filename} inside Notes."
    try:
        os.remove(file)
        return f"{filename} removed successfully."
    except Exception as e:
        return f"Some problem occurred, couldn't remove {filename}: {e}"

@mcp.tool()
def read_note(filename: str):
    """Reads a particular note from Notes folder"""
    path = os.path.join(NOTES_DIR, filename)
    if not path.startswith(NOTES_DIR):
        return "Access denied: Agent can't access the requested files."
    if not os.path.exists(path):
        return f"Couldn't find {filename}"
    with open(path, 'r', encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )
