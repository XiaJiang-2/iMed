import random
import json
import pickle
import numpy as np

import nltk
#nltk.download()
from nltk.stem import WordNetLemmatizer# reduce the word to its stem
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Activation,Dropout
from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('coversationPattern.json').read())

input_words = []
classes = []
documents = []
ignore_letters = ['?','!','.',',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern) #split setence up to the individual word
        input_words.extend(word_list)
        documents.append((word_list,intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent["tag"].lower())
# print(input_words)
input_words = [lemmatizer.lemmatize(word.lower()) for word in input_words if word not in ignore_letters]
# print(input_words)
input_words= sorted(set(input_words))#set to delete the duplicates and sort to make sure it return a list
#print(documents)
# [(['hello'], 'greetings'), (['hey'], 'greetings'), (['hi'], 'greetings')]
classes = sorted(set(classes))

pickle.dump(input_words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# used bag to represent setence, every combination in the document is a bag
training = [] # store bag and related output_row for deep learning
output_empty = [0] * len(classes)# it used to store the related tags of input_word

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize((word.lower()))for word in word_patterns]
    for word in input_words:
        bag.append(1) if word in word_patterns else bag.append(0)
    output_row = list(output_empty) # you need to empty output_row every time after for loop
    output_row[classes.index(document[1])] = 1
    training.append([bag,output_row])
random.shuffle(training)
training = np.array(training)

train_x = list(training[:,0])
train_y = list(training[:,1])

# deep learning,predict tag according to user input
model = Sequential()
model.add(Dense(128,input_shape = (len(train_x[0]),),activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation = 'relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation= 'softmax'))

sgd = SGD(lr = 0.01, decay = 1e-6, momentum = 0.9, nesterov=True)
model.compile(loss = 'categorical_crossentropy', optimizer = sgd, metrics = ['accuracy'])

hist = model.fit(np.array(train_x),np.array(train_y), epochs = 200, batch_size = 5, verbose = True)
model.save('imedbot_model.h5',hist)
print("Done")