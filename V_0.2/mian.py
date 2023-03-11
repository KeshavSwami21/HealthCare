# Imports Starts ---------------------------------------------------------------------------------------------------------
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import random
import nltk
import numpy as np
import string

# Imports Ends ---------------------------------------------------------------------------------------------------------

#Here the concept is:
#User will input the string, understand the question root and then try to find the
#appropriate answer in the saved data file and then print it
#If the data is not found then it'll return "Unable to understand that"
#This uses machine Learning module called "NLTK: Nartural Language Tool Kit")
#and try To the any type of un-preprogramed string


#Opening the files the reading the data saved in them
f1 = open('V_0.2\data.txt', 'r', errors='ignore')
f2 = open('V_0.2\data2.txt', 'r', errors='ignore')
raw_doc = f1.read() + f2.read() #Storing the read data inside a variable
# print (raw_doc)


# Tokenization Starts --------------------------------------------------------------------------------------------------


raw_doc = raw_doc.lower() #Converting entire text to lowercase
# print(raw_doc) # converted to lowercase
    
nltk.download('punkt') #Using the Punkt tokenizer
nltk.download('wordnet') #Using the wordnet Dictionary
nltk.download('omw-1.4')

sentence_tokens = nltk.sent_tokenize(raw_doc) #This will tokenize the sentence
word_tokens = nltk.word_tokenize(raw_doc) #This will tokenize the word
# print(sentence_tokens[:5]) #printing the first 5 sentence
# print(word_tokens[:5]) #printing the first 5 words    

#This will Lemmertize the data
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