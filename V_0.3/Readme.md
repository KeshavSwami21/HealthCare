# HealthCare ChatBot

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
>   >* `torch` - main library used for building and training deep learning models.
>   >* `torch.nn` - a sub-library within PyTorch containing all the necessary functions to create neural networks.
>   >* `torch.nn.functional` - another sub-library within PyTorch containing various activation functions and loss functions.
>
>2. Define Hyperparameters:
>
>   >* `batch_size`: the number of independent sequences processed in parallel.
>   >* `block_size`: the maximum context length for predictions.
>   >* `max_iters`: the maximum number of iterations to train the model.
>   >* `eval_interval`: the interval at which the loss is evaluated on the training and validation sets.
>   >* `learning_rate`: the learning rate of the optimizer used to train the model.
>   >* `device`: the device on which to train the model (CPU or GPU).
>   >* `eval_iters`: the number of iterations to use when evaluating the loss on the training and validation sets.
>   >* `n_embd`: the size of the embedding dimension used for each token in the input sequence.
>
>3. Set random seed to 1337 using `torch.manual_seed(1337)` to ensure reproducibility of the training process.
>
>4. Load the dataset from a text file and get all unique characters in the dataset.
>
>   >* `raw_doc`: read the content of a text file.
>   >* `chars`: get all unique characters in the dataset using `set()` and sort them in ascending order using `sorted()`.
>   >* `vocab_size`: get the total number of unique characters in the dataset.
>
>5. Create mappings from characters to integers and vice versa.
>
>   >* `stoi`: create a dictionary that maps each character to a unique integer index.
>   >* `itos`: create a dictionary that maps each integer index to a unique character.
>   >* `encode`: create a lambda function that takes a string and outputs a list of integers, where each integer represents the index of a character in the vocabulary.
>   >* `decode`: create a lambda function that takes a list of integers and outputs a string, where each integer represents the index of a character in the vocabulary.
>
>6. Split the dataset into training and validation sets.
> 
>   >* `data`: encode the content of the text file into a list of integers using the `encode()` function.
>   >* `n`: get the index at which to split the dataset.
>   >* `train_data`: the first 90% of the dataset will be used for training.
>   >* `val_data`: the remaining 10% of the dataset will be used for validation.
>
>7. Define a function to generate a small batch of data for the training process.
>
>   >* `get_batch()`: generate a small batch of data of inputs x and targets y.
>   >* `split`: a string indicating whether to get data from the training or validation set.
>   >* `data`: the dataset to use (either the training or validation set).
>   >* `ix`: a random index from which to start the batch.
>   >* `x`: a tensor of shape (`batch_size`, `block_size`) containing the input sequences.
>   >* `y`: a tensor of shape (`batch_size`, `block_size`) containing the target sequences.
>   >* `x`, `y`: convert the input and target sequences to the appropriate device (CPU or GPU).
>
>8. Define a function to estimate the loss on the training and validation sets.
>
>   >* `estimate_loss()`: estimate the loss on the training and validation sets.
>   >* `out`: a dictionary to store the loss values.
>   >* `model.eval()`: set the model to evaluation mode.
>   >* `split`: a string indicating whether to estimate the loss