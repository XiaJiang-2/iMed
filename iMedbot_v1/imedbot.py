import random
import json
import pickle
import numpy as np

import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.keras.models import load_model

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('coversationPattern.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('imedbot_model.h5')


def clean_up_sentence(sentence):#I am going to say hello
    """
process input sentence
    @param sentence: input sentence
    @return: a list include all stemmed word from input sentence
    """
    sentence_words = nltk.word_tokenize(sentence)
    #print(sentence_words)#['I', 'am', 'going', 'to', 'say', 'hello']

    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    #print(sentence_words)
    return sentence_words

# bag for word
def bag_of_words(sentence):
    """
transfer sentence_words into bag data structure as the input of deep learning model to predict class tag
    @param sentence: sentence word after tokenize and lemmatize
    @return:related bag structure of input_sentence
    """

    sentence_words = clean_up_sentence(sentence)
    # print("after clean up")
    # print(sentence_words)#['I', 'am', 'going', 'to', 'say', 'hello']
    bag = [0] * len(words)
    for input_word in sentence_words:
        for i, word in enumerate(words):
            if word == input_word:
                bag[i] = 1
    # print("after bag")
    # there are four words in the input that also appeared in the word list
    #print(np.array(bag))#[0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0]
    return np.array(bag)

def predict_class(sentence):
    """
predict the tag of input sentence
    @param sentence: input sentence
    @return: tag
    """
    bow = bag_of_words(sentence)
    # print("bow")
    # print(bow)
    res = model.predict(np.array([bow]))[0]#[2.1516404e-05 9.9997103e-01 5.7227639e-06 1.7859028e-06]
    print("hello")
    print(np.array([bow]))#[[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 1]]
    # print(model.predict(np.array([bow])))#[[2.1516404e-05 9.9997103e-01 5.7227639e-06 1.7859028e-06]]
    ERROR_THRESHOLD = 0.5
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # print(results)#[[1, 0.99997103]] select tag that probability > 0.25
    return_list = []
    if not results:
        return_list.append({'tag':'confuse','probability':str(0)})
    else:
        results.sort(key = lambda x:x[1], reverse = True)
    # print(results)
        for r in results:
            return_list.append({'tag':classes[r[0]],'probability':str(r[1])})
    # print(return_list)
    return return_list#[{'intent': 'greetings', 'probability': '0.9995371'}]

def get_response(intents_list,intents_json):
    # print(intents_list)
    # print(intents_json)
    tag = intents_list[0]['tag']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

print("Go! Bot is running")
# print(words)
# print(classes)
goodbye = ["Talk to you later", "Goodbye"]
while True:
    message = input("")
    ints = predict_class(message)
    res = get_response(ints,intents)
    print(res)
    if res in goodbye:
        break





