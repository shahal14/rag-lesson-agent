1. An LLM learns from text up to a training cutoff date. It does not know newer events or your private documents.
2. An LLM can hallucinate: it can give a confident answer that is wrong.
3. RAG (Retrieval-Augmented Generation) finds relevant information in external documents at question time, adds it to the prompt, and the LLM writes the answer using it.
4. RAG does NOT retrain the model or change its weights.
5. Indexing step: documents are split into chunks; each chunk is turned into an embedding (a list of numbers that captures meaning) and stored in a vector database.
6. Retrieval step: the question is also turned into an embedding; the system finds the chunks whose embeddings are most similar.
7. Augmentation step: the retrieved chunks are placed in the prompt together with the question.
8. Generation step: the LLM writes the answer using those chunks. It can point to the source chunks.
9. Benefits: answers use current or private data, fewer hallucinations (not zero), sources can be shown, and it is cheaper than retraining.
10. Limits: bad retrieval gives bad answers; it adds extra steps and delay; chunking choices matter; the model can still make mistakes.
11. The term comes from a 2020 paper by Lewis et al. (Facebook AI Research).
12. Common uses: company help-desk chatbots, question answering over documents, customer support.