# HealthCare ChatBot

### Version 1 includes the Rule based Chabot:


> 1. The code defines a class named **RuleBot** which implements a rule-based chatbot that communicates with the user in the context of an alien trying to learn about planet Earth.
>
> 2. The chatbot has several built-in rules, including exit commands, negative responses, and random starter questions.
> 
> 3. The `__init__()` function initializes the chatbot's intents as a dictionary with regular expressions that correspond to specific questions or statements the user may make.
>```python
>def __init__(self):
>        self.alienbabble = {'describe_planet_intent': r'.*\s*your planet.*',
>                            'answer_why_intent': r'why\sare.*'}
>``` 
>***
>
>
>
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
***
