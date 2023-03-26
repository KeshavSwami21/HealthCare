# HealthCare ChatBot

### Version 2 includes the preprocessing based Chabot:

1. Importing necessary libraries:

   - `TfidfVectorizer` and `cosine_similarity` from
   - `sklearn.feature_extraction.text` and `sklearn.metrics.pairwise`, respectively.
   - `re`, `random`, `nltk`, `numpy`, and `string` are also imported.

2. Reading the data from two files and storing it in a variable named `raw_doc`.

3. Tokenizing the data using `nltk.sent_tokenize()` and `nltk.word_tokenize()`. Tokenization is a process of splitting text into smaller parts, such as sentences or words.

```python
    sentence_tokens = nltk.sent_tokenize(raw_doc)
    word_tokens = nltk.word_tokenize(raw_doc)
```

---

4. Defining a function `LemTokens()` to lemmatize the tokens. Lemmatization is a process of reducing words to their base or root form.

5. Removing the punctuation from the text and normalizing it by applying lemmatization using the function `LemNormalize()`.

```python
    def LemTokens(tokens):
        return [lemmer.lemmatize(token) for token in tokens]

    remove_punc_dict = dict((ord(punkt), None) for punkt in string.punctuation)

    def LemNormalize(text):
        return LemTokens(nltk.word_tokenize(text.lower().translate  (remove_punc_dict)))
```

---

6. Defining a set of greetings that the bot will respond to and their corresponding responses.

7. Defining a function `Greet()` that takes a sentence as input and returns a greeting response if the sentence contains any of the predefined greetings.

```python
    def Greet(sentence):
        for word in sentence.split():
            if word.lower() in greet_inputs:
                return random.choice(greet_response)
```

---

8. Defining a function `response()` that takes the user's input as input and returns a response using cosine similarity. Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them.

```python
    def response(user_response):
        robo1_response = ''

        TfidfVec = TfidfVectorizer(tokenizer = LemNormalize, stop_words = 'english')
        tfidf = TfidfVec.fit_transform(sentence_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx = vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if (req_tfidf == 0):
            robo1_response = robo1_response + 'I am sorry. Unable to understand that'
            return robo1_response

        else:
            robo1_response = robo1_response + sentence_tokens[idx]
            return robo1_response
```

---

9. Implementing the chat flow using a `while` loop.

   - The loop runs until the user enters "bye".
   - The bot responds with a greeting if the user's input contains a greeting.
   - If not, the bot lemmatizes the user's input, appends it to `sentence_tokens`, and calculates the cosine similarity between the user's input and the saved data.
   - If the cosine similarity is zero, the bot responds with "I am sorry. Unable to understand that."
   - If not, the bot responds with the most similar sentence from the saved data.

```python
    while (flag == True):
        user_response = input()
        user_response = user_response.lower()

        if (user_response != 'bye'):
            if (user_response == 'thank you' or user_response == 'thanks'):
                flag = False
                print('Bot: You are Welcome....')

            else:
                if(Greet(user_response) != None):
                    print('Bot ', Greet(user_response))

                else:
                    sentence_tokens.append(user_response)
                    word_tokens = word_tokens + nltk.word_tokenize(user_response)
                    final_words = list(set(word_tokens))
                    print('Bot: ', end = '')
                    print(response(user_response))
                    sentence_tokens.remove(user_response)

        else:
            flag = False
            print('Bot: GoodBye!')
```

---

10. The user can end the conversation by typing "bye". The bot responds with "Goodbye!".
