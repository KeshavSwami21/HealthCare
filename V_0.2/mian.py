from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import random
import nltk
import numpy as np
import string



f1 = open('V_0.2\data.txt', 'r', errors='ignore')
f2 = open('V_0.2\data2.txt', 'r', errors='ignore')
raw_doc = f1.read() + f2.read()
# print (raw_doc)


# Tokenization Starts --------------------------------------------------------------------------------------------------


raw_doc = raw_doc.lower() #Converting entire text to lowercase
# print(raw_doc) # converted to lowercase
    
nltk.download('punkt') #Using the Punkt tokenizer
nltk.download('wordnet') #Using the wordnet Dictionary
nltk.download('omw-1.4')
    
sentence_tokens = nltk.sent_tokenize(raw_doc)
word_tokens = nltk.word_tokenize(raw_doc)
# print(sentence_tokens[:5]) #printing the first 5 sentence
# print(word_tokens[:5]) #printing the first 5 words
    
    
lemmer = nltk.stem.WordNetLemmatizer()
    
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
    
remove_punc_dict = dict((ord(punkt), None) for punkt in string.punctuation)
    
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punc_dict)))

# Tokenization Ends --------------------------------------------------------------------------------------------------



# Greetings Starts ---------------------------------------------------------------------------------------------------

greet_inputs = ('hello', 'hi', 'whassup', 'wassup', 'how are you?')

greet_response = ('hi', 'Hey', 'Hey There!', 'There there!!')

def Greet(sentence):
    for word in sentence.split():
        if word.lower() in greet_inputs:
            return random.choice(greet_response)


# Greetings Ends ---------------------------------------------------------------------------------------------------

# Responses Starts ---------------------------------------------------------------------------------------------------

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
    
# Responses Ends ---------------------------------------------------------------------------------------------------

# ChatFlow Starts ---------------------------------------------------------------------------------------------------


flag = True

print ("Hello! I'm the Learning Bot. Start typing your text after greeting to talk to me. For ending conversation type bye!")

while (flag == True):
    user_response = input()
    user_response = user_response.lower()
    
    if (user_response != 'bye'):
        if (user_response == 'thank you' or user_response == 'thanks'):
            flag = False
            print('Bot: You are Welcome....')
    
        else:
            if(Greet(user_response) != None):
                print('Bot ' + Greet(user_response))
        
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
    

# ChatFlow Ends ---------------------------------------------------------------------------------------------------

# class RuleBot:
#     # Potential Negative Responses
#     negative_reponses = ('no', 'nope', 'nah', 'naw', 'not a chance', 'sorry')
    
#     # Exit conversation Keywords
#     exit_commands = ('quit', 'pause', 'exit', 'goodbye', 'bye', 'later')
    
#     # Random starter question
#     random_question = (
#         'Why are you here?',
#         'Are there many humans like you?\n',
#         'What do you consume for sustenance?\n',
#         'Is there intelligent life on this planet?\n',
#         'Does Earth have a leader?\n',
#         'What planets have you visited?\n',
#         'What technology do you have ont this planet?\n'
#     )
    
#     def __init__(self):
#         self.alienbabble = {'describe_planet_intent': r'.*\s*your planet.*',
#                             'answer_why_intent': r'why\sare.*'}
    
    
#     def greet(self):
#         self.name = input("What is your name?\n")
#         will_help = input(f"Hi {self.name}, \
#                           I am Rule-Bot. Will you help me learn about your planet?\n")
        
#         if will_help in self.negative_reponses:
#             print("ok, have a nice Earth day!")
#             return 
#         self.chat()
        
#     def make_exit(self, reply):
        
#         for command in self.exit_commands:
#             if reply == command:
#                 print("Okay, have a nice Earth day!")
#                 return True
    
#     def chat(self):
#         reply = input(random.choice(self.random_question)).lower()
#         while not self.make_exit(reply):
#             reply = input(self.match_reply(reply))
    
#     def match_reply(self, reply):
#         for key, value in self.alienbabble.items():
#             intent = key
#             regex_pattern = value
#             found_match = re.match(regex_pattern, reply)
            
#             if found_match and intent == 'describe_planet_intent':
#                 return self.describe_planet_intent()
#             elif found_match and intent == 'answer_why_intent':
#                 return self.answer_why_intent()
        
#         if not found_match:
#             return self.no_match_intent()
    
#     def describe_planet_intent(self):
#         responses = ("My planet is a utopia of diverse organisms and species.\n",
#                     "I am from Opidipus, the capital of the Wayward Galaxies.\n")
        
#         return random.choice(responses)
    
#     def answer_why_intent(self):
#         responses = ("I come in peace\n",
#                     "I am here to collect data on your planet and its inhabitants\n",
#                     "I heard the coffee is good.\n")
        
#         return random.choice(responses)
    
#     def no_match_intent(self):
#         responses = (
#             "Please tell me more.\n", "Tell me more!\n", "Why do you say that?\n",
#             "I see, Can you please Elaborate?\n", "Interesting. Can you tell me more about that?\n",
#             "I see. How do you think?\n", "Why?\n", "How do you think I feel when you say that?\n",
#         )
#         return random.choice(responses)
    

# AlienBot = RuleBot()
# AlienBot.greet()