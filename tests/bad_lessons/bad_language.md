Imagine you have a smart helper who has read many books, and then Sometimes this helper forgets new facts or your private notes.

## What is RAG?

An LLM is a large language model, and then A prompt is the text you give to an AI, and then Retrieval is the act of finding information in external documents, and then RAG is Retrieval-Augmented Generation, and then RAG finds relevant information in external documents at question time, adds it to the prompt, and the LLM writes the answer using it, and then RAG does not retrain the model, and then The term comes from a 2020 paper by Lewis et al, and then from Facebook AI Research.

## Why does RAG matter?

An LLM learns from text up to a training cutoff date, and then It does not know newer events or your private documents, and then An LLM can hallucinate, and then A hallucination is when an AI gives a confident answer that is wrong, and then RAG helps fix these problems, and then RAG does not retrain the model, and then RAG does not change its weights, and then Answers use current or private data, and then There are fewer hallucinations, but they are not zero, and then You can see the sources, and then It is cheaper than retraining, and then Think of it like taking an open-book exam where you bring your notes.

## How does RAG work?

First is the indexing step, and then Documents are split into chunks, and then A chunk is a small piece of a document, and then Each chunk is turned into an embedding, and then An embedding is a list of numbers that captures meaning, and then They are stored in a vector database, and then A vector database is a special database for storing embeddings, and then Second is the retrieval step, and then The question is also turned into an embedding, and then The system finds the chunks whose embeddings are most similar, and then Third is the augmentation step, and then The retrieved chunks are placed in the prompt together with the question, and then Fourth is the generation step, and then The LLM writes the answer using those chunks, and then It can point to the source chunks.

## A worked example

Here is the document text that was stored earlier: "The office closed on Friday for cleaning."
Here is an ordinary user question about that document: "Is the office open today?"
Here is what the LLM would answer without retrieval: "I do not know if the office is open."
Here is the text found by retrieval: "The office closed on Friday for cleaning."
Here is the final answer that uses the found text: "The office is closed for cleaning."

In a nutshell, RAG is a piece of cake once you get the hang of it.

## Quick recap

RAG adds new facts to the prompt, and then It finds documents at question time, and then It uses chunks and embeddings, and then RAG does not retrain the model, and then It gives fewer wrong answers.

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