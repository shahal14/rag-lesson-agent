Imagine you have a smart helper who has read many books. Sometimes this helper forgets new facts or your private notes.

## What is RAG?

An LLM is a large language model. A prompt is the text you give to an AI. Retrieval is the act of finding information in external documents. RAG is Retrieval-Augmented Generation. RAG finds relevant information in external documents at question time, adds it to the prompt, and the LLM writes the answer using it. RAG does not retrain the model. The term comes from a 2020 paper by Lewis et al. from Facebook AI Research.

## How does RAG work?

First is the indexing step. Documents are split into chunks. A chunk is a small piece of a document. Each chunk is turned into an embedding. An embedding is a list of numbers that captures meaning. They are stored in a vector database. A vector database is a special database for storing embeddings. Second is the retrieval step. The question is also turned into an embedding. The system finds the chunks whose embeddings are most similar. Third is the augmentation step. The retrieved chunks are placed in the prompt together with the question. Fourth is the generation step. The LLM writes the answer using those chunks. It can point to the source chunks.

## A worked example

Here is the document text that was stored earlier: "The office closed on Friday for cleaning."
Here is an ordinary user question about that document: "Is the office open today?"
Here is what the LLM would answer without retrieval: "I do not know if the office is open."
Here is the text found by retrieval: "The office closed on Friday for cleaning."
Here is the final answer that uses the found text: "The office is closed for cleaning."

## Quick recap

RAG adds new facts to the prompt. It finds documents at question time. It uses chunks and embeddings. RAG does not retrain the model. It gives fewer wrong answers.

## Glossary

- **LLM**: A large language model that learns from text.
- **Prompt**: The text you give to an AI.
- **Retrieval**: The act of finding information in external documents.
- **Hallucination**: A confident answer from an AI that is wrong.
- **Chunk**: A small piece of a document.
- **Embedding**: A list of numbers that captures meaning.
- **Vector database**: A special database for storing embeddings.

## Check yourself

1. What does RAG stand for?
2. Does RAG retrain the model?
3. What is an embedding?