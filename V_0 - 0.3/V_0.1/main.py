import re
import random

#This version only include the code for the basic chatbot that only works with the pregrammed responses
# or in ohter words this is Rule based ChatBot
# The concept here is that the chabot is an alien who visited the plant earth and communicate with the humans
#to understand the planet earth.

class RuleBot:
    # Potential Negative Responses
    negative_reponses = ('no', 'nope', 'nah', 'naw', 'not a chance', 'sorry')
    
    # Exit conversation Keywords
    exit_commands = ('quit', 'pause', 'exit', 'goodbye', 'bye', 'later')
    
    # Random starter question
    random_question = (
        'Why are you here?',
        'Are there many humans like you?\n',
        'What do you consume for sustenance?\n',
        'Is there intelligent life on this planet?\n',
        'Does Earth have a leader?\n',
        'What planets have you visited?\n',
        'What technology do you have ont this planet?\n'
    )
    
    #Creating the Question intents
    def __init__(self):
        self.alienbabble = {'describe_planet_intent': r'.*\s*your planet.*',
                            'answer_why_intent': r'why\sare.*'}
    
    
    #Functoins for greetings
    def greet(self):
        self.name = input("What is your name?\n")
        will_help = input(f"Hi {self.name}, \
                          I am Rule-Bot. Will you help me learn about your planet?\n")
        
        if will_help in self.negative_reponses:
            print("ok, have a nice Earth day!")
            return 
        self.chat()
        
    #This function will terminate the chatbot
    def make_exit(self, reply):
        
        for command in self.exit_commands:
            if reply == command:
                print("Okay, have a nice Earth day!")
                return True
    
    #This fuction willl loop the chatbot for repeated conversations
    def chat(self):
        reply = input(random.choice(self.random_question)).lower()
        while not self.make_exit(reply):
            reply = input(self.match_reply(reply))
    
    #This function will match the question intent and try to answer the question accordingly
    def match_reply(self, reply):
        found_match = None
        for key, value in self.alienbabble.items():
            intent = key
            regex_pattern = value
            found_match = re.match(regex_pattern, reply)
            
            if found_match and intent == 'describe_planet_intent':
                return self.describe_planet_intent()
            elif found_match and intent == 'answer_why_intent':
                return self.answer_why_intent()
        
        if not found_match:
            return self.no_match_intent()
    
    
    #Replies for the planet question
    def describe_planet_intent(self):
        responses = ("My planet is a utopia of diverse organisms and species.\n",
                    "I am from Opidipus, the capital of the Wayward Galaxies.\n")
        
        return random.choice(responses)
    
    #Replies for the Why intent question
    def answer_why_intent(self):
        responses = ("I come in peace\n",
                    "I am here to collect data on your planet and its inhabitants\n",
                    "I heard the coffee is good.\n")
        
        return random.choice(responses)
    
    #If question is not matched in the question library then it'll just ask question and take answer 
    #Note: answer are stored in any library
    def no_match_intent(self):
        responses = (
            "Please tell me more.\n", "Tell me more!\n", "Why do you say that?\n",
            "I see, Can you please Elaborate?\n", "Interesting. Can you tell me more about that?\n",
            "I see. How do you think?\n", "Why?\n", "How do you think I feel when you say that?\n",
        )
        return random.choice(responses)
    

AlienBot = RuleBot() #Creating the object for the class RuleBot
AlienBot.greet() #Calling the greet function