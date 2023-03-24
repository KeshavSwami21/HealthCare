# HealthCare Chat

### Version 1 includes the Rule based Chabot:

> 1. The code defines a class named **RuleBot** which implements a rule-based chatbot that communicates with the user in the context of an alien trying to learn about planet Earth.
>
> 2. The chatbot has several built-in rules, including exit commands, negative responses, and random starter questions.
> 
> 3. The `__init__()` function initializes the chatbot's intents as a dictionary with regular expressions that correspond to specific questions or statements the user may make.
> 
> 4. The `greet()` function initiates the conversation with the user by asking for their name and whether they are willing to help the alien learn about Earth.
> 
> 5. The `make_exit(reply)` function checks if the user has entered one of the exit commands and terminates the chatbot if so.
> 
> 6. The `chat()` function implements the core of the chatbot, by randomly selecting one of the starter questions and then repeatedly responding to the user's input using the `match_reply()` function.
> 
> 7. The `match_reply(reply)` function matches the user's input to one of the intents defined in the chatbot's dictionary and responds accordingly. If the input does not match any intent, the chatbot uses the `no_match_intent()` function to prompt the user for more information.
> 
> 8. The `describe_planet_intent()` and `answer_why_intent()` functions define specific responses to the corresponding intents in the chatbot's dictionary.
> 
> 9. The `no_match_intent()` function provides a set of generic responses that the chatbot uses when the user's input does not match any of the defined intents.
> 
> 10. Finally, the code creates an instance of the RuleBot class and initiates the conversation by calling the `greet()` function.



### Version 2 includes the preprocessing based Chabot:

>1. Importing necessary libraries:
>
>   * `TfidfVectorizer` and `cosine_similarity` from
>   * `sklearn.feature_extraction.text` and `sklearn.metrics.pairwise`, respectively.
>   * `re`, `random`, `nltk`, `numpy`, and `string` are also imported.
>
>2. Reading the data from two files and storing it in a variable named `raw_doc`.
>
>3. Tokenizing the data using `nltk.sent_tokenize()` and `nltk.word_tokenize()`. 
>   Tokenization is a process of splitting text into smaller parts, such as sentences or words.
>
>4. Defining a function `LemTokens()` to lemmatize the tokens. Lemmatization is a process of reducing words to their base or root form.
>
>5. Removing the punctuation from the text and normalizing it by applying lemmatization using the function `LemNormalize()`.
>
>6. Defining a set of greetings that the bot will respond to and their corresponding responses.
>
>7. Defining a function `Greet()` that takes a sentence as input and returns a greeting response if the sentence contains any of the predefined greetings.
>
>8. Defining a function `response()` that takes the user's input as input and returns a response using cosine similarity. Cosine similarity is a measure of similarity between two non-zero vectors of an inner product space that measures the cosine of the angle between them.
>
>9. Implementing the chat flow using a `while` loop.
>
>   * The loop runs until the user enters "bye".
>   * The bot responds with a greeting if the user's input contains a greeting.
>   * If not, the bot lemmatizes the user's input, appends it to `sentence_tokens`, and calculates the cosine similarity between the user's input and the saved data.
>   * If the cosine similarity is zero, the bot responds with "I am sorry. Unable to understand that."
>   * If not, the bot responds with the most similar sentence from the saved data.
>
>10. The user can end the conversation by typing "bye". The bot responds with "Goodbye!".

### Version 3 includes the Biagram Language Model:

> **Bigram Language Model:**
>>The BigramLanguageModel is a PyTorch module that implements a simple language model that makes use of bigrams (i.e., pairs of adjacent characters) to predict the next character in a sequence.
>>
>>The model consists of an embedding layer for token and positional embeddings, followed by a linear layer that outputs logits for each possible next character. Specifically, the model takes as input a tensor of shape (`batch_size`, `block_size`) that represents a batch of sequences, each of length `block_size`, and outputs a tensor of shape (`batch_size`, `block_size`, `vocab_size`) that contains the logits for each possible next character in each sequence.
>> 
>>During training, the model is given the input tensor and a tensor of the same shape containing the true next characters for each sequence. It then computes the cross-entropy loss between the predicted logits and the true next characters.
>> 
>>During inference, the model is given a starting sequence and generates new characters one by one by repeatedly applying the forward pass of the model to the current sequence and sampling the next character from the predicted distribution. The generated sequence can be of arbitrary length.
>
>Here is an explanation of the provided code:
>
>1. Import necessary libraries:
>
>   * `torch` - main library used for building and training deep learning models.
>   * `torch.nn` - a sub-library within PyTorch containing all the necessary functions to create neural networks.
>   * `torch.nn.functional` - another sub-library within PyTorch containing various activation functions and loss functions.
>
>2. Define Hyperparameters:
>
>   * `batch_size`: the number of independent sequences processed in parallel.
>   * `block_size`: the maximum context length for predictions.
>   * `max_iters`: the maximum number of iterations to train the model.
>   * `eval_interval`: the interval at which the loss is evaluated on the training and validation sets.
>   * `learning_rate`: the learning rate of the optimizer used to train the model.
>   * `device`: the device on which to train the model (CPU or GPU).
>   * `eval_iters`: the number of iterations to use when evaluating the loss on the training and validation sets.
>   * `n_embd`: the size of the embedding dimension used for each token in the input sequence.
>
>3. Set random seed to 1337 using `torch.manual_seed(1337)` to ensure reproducibility of the training process.
>
>4. Load the dataset from a text file and get all unique characters in the dataset.
>
>   * `raw_doc`: read the content of a text file.
>   * `chars`: get all unique characters in the dataset using `set()` and sort them in ascending order using `sorted()`.
>   * `vocab_size`: get the total number of unique characters in the dataset.
>
>5. Create mappings from characters to integers and vice versa.
>
>   * `stoi`: create a dictionary that maps each character to a unique integer index.
>   * `itos`: create a dictionary that maps each integer index to a unique character.
>   * `encode`: create a lambda function that takes a string and outputs a list of integers, where each integer represents the index of a character in the vocabulary.
>   * `decode`: create a lambda function that takes a list of integers and outputs a string, where each integer represents the index of a character in the vocabulary.
>
>6. Split the dataset into training and validation sets.
> 
>   * `data`: encode the content of the text file into a list of integers using the `encode()` function.
>   * `n`: get the index at which to split the dataset.
>   * `train_data`: the first 90% of the dataset will be used for training.
>   * `val_data`: the remaining 10% of the dataset will be used for validation.
>
>7. Define a function to generate a small batch of data for the training process.
>
>   * `get_batch()`: generate a small batch of data of inputs x and targets y.
>   * `split`: a string indicating whether to get data from the training or validation set.
>   * `data`: the dataset to use (either the training or validation set).
>   * `ix`: a random index from which to start the batch.
>   * `x`: a tensor of shape (`batch_size`, `block_size`) containing the input sequences.
>   * `y`: a tensor of shape (`batch_size`, `block_size`) containing the target sequences.
>   * `x`, `y`: convert the input and target sequences to the appropriate device (CPU or GPU).
>
>8. Define a function to estimate the loss on the training and validation sets.
>
>   * `estimate_loss()`: estimate the loss on the training and validation sets.
>   * `out`: a dictionary to store the loss values.
>   * `model.eval()`: set the model to evaluation mode.
>   * `split`: a string indicating whether to estimate the loss