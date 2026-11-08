Computers can now talk and write like smart humans. You can learn how to make these smart computer tools work with private documents.

## What is RAG?
An LLM is a large language model that reads and writes human text. A prompt is the text you give to an AI. Retrieval is the action of finding needed facts from stored files. RAG is Retrieval-Augmented Generation. RAG finds relevant information in external documents at question time. It adds this information to the prompt. Then the LLM writes the answer using it. RAG does not retrain the model or change its weights. The term comes from a 2020 paper by Lewis et al. from Facebook AI Research.

## Why does RAG matter?
An LLM learns from text up to a training cutoff date. It does not know newer events or your private documents. An LLM can hallucinate, which means it can give a confident answer that is wrong. RAG helps fix these big problems. RAG answers use current or private data. RAG has fewer hallucinations, but the number is not zero. You can see the sources of the answers. RAG is also cheaper than retraining an LLM.

## How does RAG work?
RAG works like taking an open-book exam where you look up facts in a real book during the test. Indexing is the first step. Documents are split into pieces called chunks. Each chunk is turned into an embedding, which is a list of numbers that captures meaning. The embeddings are stored in a vector database, which is a special database for meaning numbers. Retrieval is the second step. The user question is also turned into an embedding. The system finds the chunks whose embeddings are most similar to the question. Augmentation is the third step. The retrieved chunks are placed in the prompt together with the question. Generation is the fourth step. The LLM writes the answer using those chunks. It can point to the source chunks.

## A worked example
Here is how RAG works with a real example. 
First, the document text that was stored earlier: "Office parking opens at eight in the morning." 
Second, an ordinary user question about that document: "When does the office parking open?" 
Third, what the LLM would answer without retrieval: The LLM has never seen the document, so it guesses or says it does not know. 
Fourth, the text found by retrieval: "Office parking opens at eight in the morning." 
Fifth, the final answer that uses the found text: "The office parking opens at eight in the morning."

## Quick recap
RAG connects external documents to your AI prompts. It finds matching text and gives it to the LLM. The LLM writes correct answers using that text. RAG does not retrain the model. It stops the model from making up false facts.

## Glossary
- **LLM**: A large language model that reads and writes human text.
- **prompt**: The text you give to an AI.
- **retrieval**: The action of finding needed facts from stored files.
- **hallucination**: A false answer given with high confidence by the model.
- **chunk**: A small piece of a split document.
- **embedding**: A list of numbers that captures meaning.
- **vector database**: A special database for storing embeddings.

## Check yourself
1. What does RAG stand for?
2. Does RAG retrain the LLM?
3. What is placed into the prompt during augmentation?