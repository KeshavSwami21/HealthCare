# HealthCare Chat

### Version 1 include the Rule based Chabot:

> 1. The code defines a class named RuleBot which implements a rule-based chatbot that communicates with the user in the context of an alien trying to learn about planet Earth.
>
> 2. The chatbot has several built-in rules, including exit commands, negative responses, and random starter questions.
> 
> 3. The __init__() function initializes the chatbot's intents as a dictionary with regular expressions that correspond to specific questions or statements the user may make.
> 
> 4. The greet() function initiates the conversation with the user by asking for their name and whether they are willing to help the alien learn about Earth.
> 
> 5. The make_exit(reply) function checks if the user has entered one of the exit commands and terminates the chatbot if so.
> 
> 6. The chat() function implements the core of the chatbot, by randomly selecting one of the starter questions and then repeatedly responding to the user's input using the match_reply() function.
> 
> 7. The match_reply(reply) function matches the user's input to one of the intents defined in the chatbot's dictionary and responds accordingly. If the input does not match any intent, the chatbot uses the no_match_intent() function to prompt the user for more information.
> 
> 8. The describe_planet_intent() and answer_why_intent() functions define specific responses to the corresponding intents in the chatbot's dictionary.
> 
> 9. The no_match_intent() function provides a set of generic responses that the chatbot uses when the user's input does not match any of the defined intents.
> 
> 10. Finally, the code creates an instance of the RuleBot class and initiates the conversation by calling the greet() function.


### Version 3 includes the Biagram Language Model:

>The BigramLanguageModel is a PyTorch module that implements a simple language model that makes use of bigrams (i.e., pairs of adjacent characters) to predict the next character in a sequence.
> 
>The model consists of an embedding layer for token and positional embeddings, followed by a linear layer that outputs logits for each possible next character. Specifically, the model takes as input a tensor of shape (batch_size, block_size) that represents a batch of sequences, each of length block_size, and outputs a tensor of shape (batch_size, block_size, vocab_size) that contains the logits for each possible next character in each sequence.
> 
>During training, the model is given the input tensor and a tensor of the same shape containing the true next characters for each sequence. It then computes the cross-entropy loss between the predicted logits and the true next characters.
> 
>During inference, the model is given a starting sequence and generates new characters one by one by repeatedly applying the forward pass of the model to the current sequence and sampling the next character from the predicted distribution. The generated sequence can be of arbitrary length.