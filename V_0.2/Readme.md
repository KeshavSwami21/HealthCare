# HealthCare ChatBot

### Version 2 includes the preprocessing based Chabot:

1. Importing necessary libraries:

    - `TfidfVectorizer` and `cosine_similarity` from
    - `sklearn.feature_extraction.text` and `sklearn.metrics.pairwise`, respectively.
    - `re`, `random`, `nltk`, `numpy`, and `string` are also imported.

2. Reading the data from two files and storing it in a variable named `raw_doc`.

3. Tokenizing the data using `nltk.sent_tokenize()` and `nltk.word_tokenize()`.
   Tokenization is a process of splitting text into smaller parts, such as sentences or words.

4. Defining a function `LemTokens()` to lemmatize the tokens. Lemmatization is a process of reducing words to their base or root form.

5. Removing the punctuation from the text and normalizing it by applying lemmatization using the function `LemNormalize()`.
   >
6. Defining a set of greetings that the bot will respond to and their corresponding responses.

7. Defining a function `Greet()` that takes a sentence as input and returns a greeting response if the sentence contains any of the predefined greetings.

8. Defining a function `response()` that takes the user's input as input and returns a response using cosine similarity. Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them.

9. Implementing the chat flow using a `while` loop.

    - The loop runs until the user enters "bye".
    - The bot responds with a greeting if the user's input contains a greeting.
    - If not, the bot lemmatizes the user's input, appends it to `sentence_tokens`, and calculates the cosine similarity between the user's input and the saved data.
    - If the cosine similarity is zero, the bot responds with "I am sorry. Unable to understand that."
    - If not, the bot responds with the most similar sentence from the saved data.

10. The user can end the conversation by typing "bye". The bot responds with "Goodbye!".