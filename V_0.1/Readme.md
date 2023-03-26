# HealthCare ChatBot

### Version 1 includes the Rule based Chabot:


> 1. The code defines a class named **RuleBot** which implements a rule-based chatbot that communicates with the user in the context of an alien trying to learn about planet Earth.
>
> 2. The chatbot has several built-in rules, including exit commands, negative responses, and random starter questions.
> 
> 3. The `__init__()` function initializes the chatbot's intents as a dictionary with regular expressions that correspond to specific questions or statements the user may make.
>```python
>    def __init__(self):
>        self.alienbabble = {'describe_planet_intent': r'.*\s*your planet.*',
>                            'answer_why_intent': r'why\sare.*'}
>``` 
>***
> 4. The `greet()` function initiates the conversation with the user by asking for their name and whether they are willing to help the alien learn about Earth.
>```python
>    def greet(self):
>        self.name = input("What is your name?\n")
>        will_help = input(f"Hi {self.name}, \
>                          I am Rule-Bot. Will you help me learn about your planet?\n")
>        
>        if will_help in self.negative_reponses:
>            print("ok, have a nice Earth day!")
>            return 
>        self.chat()
>```
>***
> 5. The `make_exit(reply)` function checks if the user has entered one of the exit commands and terminates the chatbot if so.
> ```python
>    def make_exit(self, reply):
>        
>        for command in self.exit_commands:
>            if reply == command:
>                print("Okay, have a nice Earth day!")
>                return True
>```
>***
> 6. The `chat()` function implements the core of the chatbot, by randomly selecting one of the starter questions and then repeatedly responding to the user's input using the `match_reply()` function.
> ```python
>    def chat(self):
>        reply = input(random.choice(self.random_question)).lower()
>        while not self.make_exit(reply):
>            reply = input(self.match_reply(reply))
>```
>***
> 7. The `match_reply(reply)` function matches the user's input to one of the intents defined in the chatbot's dictionary and responds accordingly. If the input does not match any intent, the chatbot uses the `no_match_intent()` function to prompt the user for more information.
> ```python
>    def match_reply(self, reply):
>        found_match = None
>        for key, value in self.alienbabble.items():
>            intent = key
>            regex_pattern = value
>            found_match = re.match(regex_pattern, reply)
>            
>            if found_match and intent == 'describe_planet_intent':
>                return self.describe_planet_intent()
>            elif found_match and intent == 'answer_why_intent':
>                return self.answer_why_intent()
>        
>        if not found_match:
>            return self.no_match_intent()
>```
>***
> 8. The `describe_planet_intent()` and `answer_why_intent()` functions define specific responses to the corresponding intents in the chatbot's dictionary.
> ```python
>    #Replies for the planet question
>    def describe_planet_intent(self):
>        responses = ("My planet is a utopia of diverse organisms and species.\n",
>                    "I am from Opidipus, the capital of the Wayward Galaxies.\n")
>        
>        return random.choice(responses)
>    
>    #Replies for the Why intent question
>    def answer_why_intent(self):
>        responses = ("I come in peace\n",
>                    "I am here to collect data on your planet and its inhabitants\n",
>                    "I heard the coffee is good.\n")
>        
>        return random.choice(responses)
>```
>***
> 9. The `no_match_intent()` function provides a set of generic responses that the chatbot uses when the user's input does not match any of the defined intents.
> 
> 10. Finally, the code creates an instance of the RuleBot class and initiates the conversation by calling the `greet()` function.
***
