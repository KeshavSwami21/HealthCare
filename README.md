# HealthCare Chat

### Version 1 include the Rule based Chabot:



### Version 3 includes the Biagram Language Model:

> The BigramLanguageModel is a PyTorch module that implements a simple language model that makes use of bigrams (i.e., pairs of adjacent characters) to predict the next character in a sequence.
> 
> The model consists of an embedding layer for token and positional embeddings, followed by a linear layer that outputs logits for each possible next character. Specifically, the model takes as input a tensor of shape (batch_size, block_size) that represents a batch of sequences, each of length block_size, and outputs a tensor of shape (batch_size, block_size, vocab_size) that contains the logits for each possible next character in each sequence.
> 
>During training, the model is given the input tensor and a tensor of the same shape containing the true next characters for each sequence. It then computes the cross-entropy loss between the predicted logits and the true next characters.
> 
>During inference, the model is given a starting sequence and generates new characters one by one by repeatedly applying the forward pass of the model to the current sequence and sampling the next character from the predicted distribution. The generated sequence can be of arbitrary length.