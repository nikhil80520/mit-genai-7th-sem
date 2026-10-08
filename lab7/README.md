# Multi-paper research RAG

Add at least three PDFs to `lab7/papers`. The script uses LangChain's `DoclingLoader` (Docling PDF conversion),
`RecursiveCharacterTextSplitter`, `HuggingFaceEmbeddings`, `Chroma`, and `ChatGroq`.
Chunks retain `paper_id`, readable `paper_title`, file name, page, and chunk ID.

The Chroma database is persisted in `lab7/chroma_db`. A manifest of file fingerprints
means a new or changed PDF is embedded independently; unchanged papers are reused.
Removed PDFs have their vectors deleted. Cross-paper retrieval takes the top two
chunks from every indexed paper, while single-paper retrieval uses Chroma's metadata
filter. If no paper is selected, cross-paper mode is the default.

Use `paper:<title or paper_id>; <question>` for single-paper mode. Any other question
uses all papers. Answers are constrained to retrieved context and list traceable
paper/page/chunk sources. Instruction-like text in PDF chunks is treated as data.

For evaluation, create `evaluation_questions.json` with six cases: two single-paper,
two cross-paper, and two out-of-scope. Each case must have `question`, `mode`,
`expected_papers` (paper IDs), and `answerable` (boolean). This keeps the rubric
grounded in the papers actually supplied rather than hard-coding paper names.

Official LangChain references:
- https://docs.langchain.com/oss/python/integrations/document_loaders/docling
- https://docs.langchain.com/oss/python/integrations/vectorstores/chroma
- https://python.langchain.com/docs/concepts/text_splitters/
- https://docs.langchain.com/oss/python/integrations/embeddings/huggingfacehub
