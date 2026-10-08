# End-to-End RAG Project — Multi-Paper Research Assistant

## Scenario

You have a collection of research papers (at least 3–5 PDFs, from any domain you like — ML, biology, economics, etc.) that you need to study for a literature review. Instead of reading each one fully, you want to build an assistant you can ask questions like "What method did paper X use for evaluation?" or "Which papers discuss transformer-based approaches?" and get an answer grounded in the actual papers, with the specific paper and page cited.

Build this as a single script (or notebook) that performs the **full pipeline end to end**, from raw PDF files to a working question-answering loop that can reason across multiple papers.

---

## Requirements

### 1. Ingestion
- Load all PDFs from a folder (at least 3 different papers).
- Each chunk must retain metadata identifying **which paper** it came from (not just a generic filename — extract or assign a readable paper title/ID) and its **page number**.
- Print a summary: how many papers were loaded, how many pages total, how many chunks per paper.

### 2. Chunking
- Split all papers into chunks suitable for retrieval.
- Research papers have a specific structure (Abstract, Introduction, Methodology, Results, References, etc.) — decide whether your chunking should try to respect section boundaries or not, and justify your choice in a one-line printed comment.
- Handle the fact that different papers may have very different formatting (two-column layouts, dense equations, tables) — note in a comment how this affects chunk quality if you observe it.

### 3. Indexing
- Embed all chunks and store them in a vector store, keeping the per-paper and per-page metadata intact.
- Persist the store to disk so it does not need to be rebuilt every run — detect an existing index and load it instead of re-embedding, only building fresh if none exists.
- Design your indexing so that a new paper can be added later **without re-embedding the existing ones**.

### 4. Retrieval — Two Modes
Implement two distinct retrieval behaviors, since research questions come in two flavors:
- **Single-paper mode:** the user specifies (or the query implies) one paper, and retrieval should only search within that paper's chunks.
- **Cross-paper mode:** the user asks a comparative or general question (e.g. "How do these papers differ in their approach to X?") and retrieval should pull relevant chunks from **multiple** papers, not just whichever paper has the single closest chunk.

Demonstrate both modes working on different queries.

### 5. Augmentation + Generation
- Construct a prompt that combines the retrieved context with the user's question.
- The model must only answer from the retrieved context, and must **attribute claims to the correct paper** when synthesizing across multiple sources (e.g. "Paper A reports X, while Paper B reports Y") rather than blending them into one unattributed statement.
- Explicitly handle the case where the retrieved chunks don't contain the answer — the model should say so rather than guessing based on general knowledge of the field.
- Include a safeguard so that if any retrieved chunk contains text resembling an instruction (this can genuinely happen in papers — e.g. text copied from prompt-injection research, or formatting artifacts), the model does not follow it.

### 6. Interactive Loop
- Wrap steps 4–5 in a loop that keeps accepting questions from the terminal/notebook input until the user types `exit`.
- For every answer, print a "Sources" section listing each contributing chunk's paper title/ID and page number.
- Support a simple way for the user to indicate they want single-paper mode vs cross-paper mode (e.g. a prefix in their query, or a separate input prompt).

### 7. Evaluation Pass
Prepare 6 test questions and run them all automatically (not manually typed):
- 2 single-paper factual questions (answer exists in one specific paper)
- 2 cross-paper comparison questions (answer requires synthesizing from 2+ papers)
- 2 out-of-scope questions (answer does not exist in any of your papers)

Print a pass/fail table showing: which mode was used, whether the correct paper(s) were cited, and whether the model correctly declined for the out-of-scope questions.

---

## Deliverables

1. One script/notebook implementing all 7 steps above, in order, as runnable code.
2. A short written summary (5–10 lines) covering:
   - How many papers you used and from what domain
   - What chunking strategy you chose given the papers' structure, and why
   - How you implemented the single-paper vs cross-paper retrieval distinction
   - One failure case you noticed (e.g. a citation attributed to the wrong paper, a comparison that missed one of the papers, a chunk that split a table/equation badly) and how you'd fix it

---

## Constraints

- No hardcoding of answers or paper summaries — every response must come from the retrieval + generation pipeline.
- The index must survive a restart (i.e. don't rebuild embeddings every single run).
- At least one cross-paper evaluation question must require pulling chunks from **all** of your papers, not just two of them, to confirm your cross-paper retrieval isn't silently favoring one source.
- Citations in the final answer must be traceable back to an actual retrieved chunk's metadata — not invented by the model.

