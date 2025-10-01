from llama_index.core.tools import ToolMetadata  # Ensure this import is correct

class NoteEngine:
    def __init__(self):
        self.metadata = ToolMetadata(
            name="note_engine",
            description="Processes notes and queries."
        )

    def __call__(self, query):
        return f"Note engine processed your query: {query}"

note_engine = NoteEngine()
