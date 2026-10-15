"""MCP server exposing the mini-Wikipedia RAG index (lesson 09.04).

Run by an MCP client over stdio, e.g. Claude Code:
    claude mcp add mini-wiki -- uv run --directory /path/to/ai-eng python chapters/09-agents/mcp_server.py
"""
from mcp.server.mcpserver import MCPServer  # mcp>=2 (was FastMCP in mcp 1.x)

from aieng import rag

mcp = MCPServer("mini-wiki", instructions="Search a small encyclopedia corpus (3,200 Wikipedia passages).")


@mcp.tool()
def search_docs(query: str, k: int = 4) -> str:
    """Search the encyclopedia. Returns the k most relevant passages, each prefixed with its id like [12]."""
    return "\n\n".join(f"[{pid}] {text}" for pid, _, text in rag.search(query, k=min(k, 10)))


@mcp.tool()
def get_passage(passage_id: int) -> str:
    """Return the full text of one passage by id."""
    docs = rag.corpus()
    if not 0 <= passage_id < len(docs):
        raise ValueError(f"passage_id must be between 0 and {len(docs) - 1}")
    return docs[passage_id]


@mcp.resource("wiki://stats")
def stats() -> str:
    """Corpus statistics."""
    return f"{len(rag.corpus())} passages, embedded with {rag.EMBED_MODEL}"


@mcp.prompt()
def cite_answer(question: str) -> str:
    """A prompt template that asks for a cited answer."""
    return f"Use search_docs to answer, citing passage ids like [12]. Question: {question}"


if __name__ == "__main__":
    mcp.run()  # stdio transport by default
