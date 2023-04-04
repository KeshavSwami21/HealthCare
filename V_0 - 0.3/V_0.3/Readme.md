# HealthCare ChatBot

### Version 3 includes the Biagram Language Model:

#### Bigram Language Model:

The BigramLanguageModel is a PyTorch module that implements a simple language model that makes use of bigrams (i.e., pairs of adjacent characters) to predict the next character in a sequence.
The model consists of an embedding layer for token and positional embeddings, followed by a linear layer that outputs logits for each possible next character. Specifically, the model takes as input a tensor of shape (`batch_size`, `block_size`) that represents a batch of sequences, each of length `block_size`, and outputs a tensor of shape (`batch_size`, `block_size`, `vocab_size`) that contains the logits for each possible next character in each sequence.
During training, the model is given the input tensor and a tensor of the same shape containing the true next characters for each sequence. It then computes the cross-entropy loss between the predicted logits and the true next characters.
During inference, the model is given a starting sequence and generates new characters one by one by repeatedly applying the forward pass of the model to the current sequence and sampling the next character from the predicted distribution. The generated sequence can be of arbitrary length.

**Here is an explanation of the provided code:**

**1.** The code implements a language model based on the transformer architecture for predicting the next character in a sequence of text given a context of fixed length.

**2.** The hyperparameters for the model, such as batch size, maximum context length, number of iterations, learning rate, and device, are set at the beginning of the code.

```python
    batch_size = 256
    block_size = 256
    max_iters = 5000
    eval_interval = 500
    learning_rate = 3e-4
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    eval_iters = 200
    n_embd = 384
    n_head = 6
    n_layer = 6
    dropout = 0.2
```

---

**3.** The dataset is loaded from a text file and a mapping is created between characters and integers using `chars`, `vocab_size`, `stoi`, `itos`, `encode`, and `decode`.

```python
    chars = sorted(list(set(raw_doc)))
    vocab_size = len(chars)


    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for i, ch in enumerate(chars)}

    def encode(s): return [stoi[c] for c in s]
    def decode(l): return ''.join([itos[i] for i in l])
```

---

**4.** The data is split into training and validation sets using `train_data` and `val_data`.

```python
    data = torch.tensor(encode(raw_doc), dtype=torch.long)
    n = int(0.9*len(data))  # First 90% will be train, rest val
    train_data = data[:n]
    val_data = data[n:]
```

---

**5.** `get_batch(split)` function generates a small batch of data containing input `x` and target `y`. It randomly selects `batch_size` number of data samples from the `train_data` if `split` is "train", otherwise it selects from `val_data`. It then stacks each selected data sample in the batch into a tensor of shape (`batch_size`, `block_size`). `x` tensor contains the first `block_size` elements of each selected sample and `y` tensor contains the next `block_size` elements of each selected sample. Finally, `x` and `y` are returned as tensors on the `device`.

```python
    def get_batch(split):

        data = train_data if split == 'train' else val_data
        ix = torch.randint(len(data) - block_size, (batch_size,))
        x = torch.stack([data[i:i+block_size] for i in ix])
        y = torch.stack([data[i+1:i+block_size+1] for i in ix])
        x, y = x.to(device), y.to(device)
        return x, y
```

---

**6.** `estimate_loss()` function estimates the mean loss of the model on the `train` and `val` datasets. It sets the model to evaluation mode and loops over `eval_iters` number of iterations to get `X` and `Y` batches from `get_batch()` function. It then passes `X` and `Y` to the model and calculates the mean loss for each iteration. The average loss over all iterations is returned for both the `train` and `val` splits.

```python
    def estimate_loss():
        out = {}
        model.eval()
        for split in ['train', 'val']:
            losses = torch.zeros(eval_iters)
            for k in range(eval_iters):
                X, Y = get_batch(split)
                logits, loss = model(X, Y)
                losses[k] = loss.item()
            out[split] = losses.mean()
        model.train()
        return out
```

---

**7.** `Head` class defines one head of the self-attention. It has three linear layers (`key`, `query`, and `value`) that transform the input `x` into query, key, and value vectors. It then computes the attention weights using the dot product of query and key vectors and scales it with the square root of the embedding dimension. It applies a mask to ensure that each token only attends to previous tokens. It then applies a softmax function and a dropout layer to the attention weights and aggregates the values using the weighted sum of values. Finally, the output tensor is returned.

```python
    class Head(nn.Module):
    # one head of the self-attention

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)
        self.query = nn.Linear(n_embd, head_size, bias=False)
        self.value = nn.Linear(n_embd, head_size, bias=False)
        self.register_buffer('tril', torch.tril(
            torch.ones(batch_size, block_size)))

        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)  # B,T,C
        q = self.query(x)  # B,T,C

        # compute attention scores ("affinities")
        wei = q @ k.transpose(-2, -1) * C**-0.5  # (B,T,C) @ (B,T,C) -> (B,T,T)
        wei = wei.masked_fill(
            self.tril[:T, :T] == 0, float('-inf')) # type: ignore
        wei = F.softmax(wei, dim=-1)  # (B,T,T)
        wei = self.dropout(wei)

        # perfom the weighted aggregation of the values
        v = self.value(x)  # (B,T,C)
        out = wei  @ v  # (B,T,T) @ (B,T,C) -> (B,T,C)
        return out
```

---

**8.** `MultiHeadAttention` class defines multiple heads of self-attention in parallel. It has a list of `num_heads` `Head` instances and a linear layer (`proj`) to project the concatenated output of all heads into the embedding dimension. A dropout layer is applied after projection, and the output tensor is returned.

```python
    class MultiHeadAttention(nn.Module):
        # Multiple heads of the self-attention in parallel

        def __init__(self, num_heads, head_size):
            super().__init__()
            self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])
            self.proj = nn.Linear(n_embd, n_embd)
            self.dropout = nn.Dropout(dropout)

        def forward(self, x):
            out = torch.cat([h(x) for h in self.heads], dim=-1)
            out = self.dropout(self.proj(out))
            return out
```

---

**9.** `FeedForward` class defines a simple linear layer followed by a ReLU activation function, another linear layer, and a dropout layer.

```python
    class FeedForward(nn.Module):
        # A simple linear Layer Followed by a non-linearity

        def __init__(self, n_embd):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(n_embd,4 * n_embd),
                nn.ReLU(),
                nn.Linear(4 * n_embd, n_embd),
                nn.Dropout(dropout),
            )

        def forward(self, x):
            return self.net(x)
```

---

**10.** `Block` class defines a transformer block, which consists of a self-attention layer (`sa`), a feedforward layer (`ffwd`), and two layer normalization layers (`ln1` and `ln2`). It takes the input `x`, passes it through the self-attention layer followed by the first layer normalization layer and adds it to the input. The result is then passed through the feedforward layer, followed by the second layer normalization layer, and added to the previous result. The final output is returned.

```python
    class Block(nn.Module):
        #Transformer block: Communication followed by computation

        def __init__(self, n_embd, n_head):
            #n_embd: embedding dimension, n_head: the number of heads we'd like

            super().__init__()
            head_size = n_embd // n_head
            self.sa = MultiHeadAttention(n_head, head_size)
            self.ffwd = FeedForward(n_embd)
            self.ln1 = nn.LayerNorm(n_embd)
            self.ln2 = nn.LayerNorm(n_embd)

        def forward(self, x):
            x = x + self.sa(self.ln1(x))
            x = x + self.ffwd(self.ln2(x))
            return x
```

**11.** **Super Simple Bigram Model**:

```python
    class BigramLanguageModel(nn.Module):

        def __init__(self):
            super().__init__()
            # Each token directly reads off the logits for the next token from a lookup table
            self.token_embedding_table = nn.Embedding(vocab_size, n_embd)
            self.position_embedding_table = nn.Embedding(block_size, n_embd)
            self.blocks = nn.Sequential(*[Block(n_embd, n_head=n_head) for _ in range(n_layer)])
            self.lnf = nn.LayerNorm(n_embd) # final layer norm
            self.lm_head = nn.Linear(n_embd, vocab_size)

        def forward(self, idx, targets=None):
            B, T = idx.shape

            # idx and targets are both (B, T) tensor of integers
            tok_emb = self.token_embedding_table(idx)  # (B, T, C)
            pos_emb = self.position_embedding_table(
                torch.arange(T, device=device))  # (T, C)
            x = tok_emb + pos_emb  # (B, T, C)
            x = self.blocks(x)# (B, T, C)
            logits = self.lm_head(x)  # (B, T, vocab_size)

            if targets is not None:
                B, T, C = logits.shape
                logits = logits.view(B*T, C)
                targets = targets.view(B*T)
                loss = F.cross_entropy(logits, targets)
                return logits, loss
            else:
                return logits, None

        def generate(self, idx, max_new_tokens):

            # idx is (B, T) array of indices in the current content
            for _ in range(max_new_tokens):
                # crop idx to the block_size tokens
                idx_cond = idx[:, -block_size:]
                # get the predictions
                logits, loss = self(idx_cond)
                # focus only on the last time step
                logits = logits[:, -1, :]  # Becomes (B, C)
                # apply softmax to get probablities
                probs = F.softmax(logits, dim=-1)  # (B, C)
                # sample from the distribution
                idx_next = torch.multinomial(probs, num_samples=1)  # (B, 1)
                # append sampled index to the running sequence
                idx = torch.cat((idx, idx_next), dim=1)  # (B, T+1)

            return idx
```

- The code defines a class `BigramLanguageModel` that inherits from `nn.Module`. This class implements a simple bigram language model using the transformer architecture.
- The class has an `__init__` method that initializes the various components of the model, including the token embedding table, the position embedding table, the transformer blocks, the final layer norm, and the linear layer that maps the output of the transformer to a probability distribution over the vocabulary.
- The `forward` method of the class takes an input tensor `idx` of shape (`B`, `T`) representing a batch of sequences of tokens, where `B` is the batch size and `T` is the maximum sequence length. It also takes an optional target tensor `targets` of shape (`B`, `T`) representing the target tokens for each input sequence.
- The method first applies an embedding layer to the input tensor to obtain the token embeddings. It then adds the position embeddings to the token embeddings to obtain the final input tensor for the transformer.
- The input tensor is then passed through a sequence of transformer blocks, which transform the input tensor into a sequence of hidden states.
- The output of the transformer is then passed through a layer normalization layer and a linear layer to obtain the logits for each token in the vocabulary.
- If `targets` is not `None`, the method computes the cross-entropy loss between the logits and the targets, and returns both the logits and the loss. Otherwise, it returns only the logits.
- The `generate` method of the class takes an input tensor `idx` of shape (`B`, `T`) representing a batch of sequences of tokens, and an integer `max_new_tokens` representing the maximum number of new tokens to generate for each sequence.
- The method repeatedly generates new tokens by sampling from the probability distribution over the vocabulary predicted by the model based on the input sequence and the previously generated tokens. It appends the sampled tokens to the end of the input sequence and continues generating new tokens until `max_new_tokens` tokens have been generated for each sequence.
- The method repeatedly generates new tokens by sampling from the probability distribution over the vocabulary predicted by the model based on the input sequence and the previously generated tokens. It appends the sampled tokens to the end of the input sequence and continues generating new tokens until max_new_tokens tokens have been generated for each sequence.

**12.** `model = BigramLanguageModel()`: creates an instance of the `BigramLanguageModel` class and `m = model.to(device)`: transfers the model to a specific device, such as a GPU if available, for faster computations.

```python
    model = BigramLanguageModel()
    m = model.to(device)
```

---

**13.** `optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)`: creates an AdamW optimizer to update the model's parameters during training.

```python
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
```

---

**14.** **The Loop**:

```python
    for iter in range(max_iters):

        # every once in a while evaluate the loss on train and val sets
        if iter % eval_interval == 0:
            losses = estimate_loss()
            print(
                f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

        # sample a batch of data
        xb, yb = get_batch('train')

        # evaluate the loss
        logits, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
```

- `for iter in range(max_iters):` : iterates over the maximum number of training iterations.
- `if iter % eval_interval == 0:` : if the current iteration is a multiple of `eval_interval`, evaluate the loss on the train and validation sets.
- `losses = estimate_loss()`: calls a function estimate_loss() to calculate the average loss on the train and validation sets.
- `xb, yb = get_batch('train')`: samples a batch of training data using the function `get_batch()`.
- `logits, loss = model(xb, yb)`: calculates the model's logits and loss on the input batch `xb` and target batch `yb`.
- `optimizer.zero_grad(set_to_none=True)`: zeroes out the gradients of the optimizer before computing gradients for the current batch.
- `loss.backward()`: computes the gradients of the loss with respect to the model's parameters.
- `optimizer.step()`: updates the model's parameters using the computed gradients and the optimizer.

**15.** `context = torch.zeros((1, 1), dtype=torch.long, device=device)`: initializes the context for text generation as a single token with a value of zero.

**16.** `m.generate(context, max_new_tokens=500)`: calls the `generate()` method of the model to generate 500 new tokens given the context.

**17.** `decode(m.generate(context, max_new_tokens=500)[0].tolist())`: decodes the generated sequence of tokens into human-readable text using a decoding function.
```python
    context = torch.zeros((1, 1), dtype=torch.long, device=device)
    print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))
```