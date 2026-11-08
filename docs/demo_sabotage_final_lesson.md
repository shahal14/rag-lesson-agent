Computers can now talk to us like real humans do. You can learn how to build these smart computer systems today.

## What is RAG?

An LLM is a large language model that reads text and writes answers. A prompt is the text you give to an AI. Retrieval is the act of finding facts stored in an outside place. RAG is Retrieval-Augmented Generation. RAG finds relevant information in external documents at question time. It adds this information to the prompt. Then the LLM writes the answer using it. RAG does not retrain the model.

## Why does RAG matter?

An LLM learns from text up to a training cutoff date. It does not know newer events or your private documents. An LLM can hallucinate. A hallucination is a confident answer that is wrong. RAG helps fix these problems. 

Think of an open-book exam. A student cannot remember every book in the library. During the test, the student looks up the right page in a book and writes the correct answer. RAG works the same way for an AI.

## How does RAG work?

First, we do the indexing step. Documents are split into pieces called chunks. A chunk is a small part of a larger document. Each chunk is turned into an embedding. An embedding is a list of numbers that captures meaning. These numbers are stored in a vector database. A vector database is a special database that stores numbers for meaning.

Next, we do the retrieval step. The question is also turned into an embedding. The system finds the chunks whose embeddings are most similar to the question.

Then, we do the augmentation step. The retrieved chunks are placed in the prompt together with the question.

Finally, we do the generation step. The LLM writes the answer using those chunks. It can point to the source chunks. RAG does not retrain the model or change its weights.

## A worked example

Here is how RAG works with real data. 

(1) The document text that was stored earlier: "The office coffee machine will be replaced on Friday."

(2) An ordinary user question about that document: "When are we getting a new coffee machine?"

(3) What the LLM would answer WITHOUT retrieval: The model has never seen the document before. It guesses or says it does not know the answer.

(4) The text found by retrieval: "The office coffee machine will be replaced on Friday."

(5) The final answer that uses the found text: "You are getting a new coffee machine on Friday."

## Quick recap

An LLM has a training cutoff date and cannot see your private files. RAG finds outside facts and adds them to the prompt so the LLM can read them. RAG does not retrain the model. RAG helps reduce hallucinations and lets the AI use new data.

## Glossary

- **LLM**: A large language model that reads and writes text.
- **prompt**: The text you give to an AI.
- **retrieval**: The act of finding facts stored in an outside place.
- **hallucination**: A confident answer that is wrong.
- **chunk**: A small part of a larger document.
- **embedding**: A list of numbers that captures meaning.
- **vector database**: A special database that stores numbers for meaning.

## Check yourself

1. Does RAG retrain the model?
2. What is a hallucination?
3. What is an embedding?