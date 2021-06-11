from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

import pymongo

# Creating ChatBot Instance
# related documentation: https://chatterbot.readthedocs.io/en/stable/storage/
#chatbot = ChatBot('CoronaBot')
chatbot = ChatBot(
    # we create a ChatBot object called Breast Cancer ImedBot
    'Breast Cancer ImedBot',
    #Storage Adapters allows you to connect to a particular storage unit or network
    #Conceptually, the wal-index file is a shared memory to store log as the backup of real database,it will not cause
    # any problems with sqlite database
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter="chatterbot.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.output.OutputAdapter",
    #storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    #You can also position the logical adapter with a chatbot object.
    # As the name implies, Logical Adapter regulates the logic behind the chatterbot, i.e.,
    # it picks responses for any input provided to it. This parameter contains a list of logical operators.
    # Chatterbot allows us to use a number of logical Adapters. When more than one logical adapter is put to use,
    # the chatbot will calculate the confidence level, and the response with the highest calculated confidence will be returned as output.
    # Here we have used two logical adapters: BestMatch and TimeLogicAdapter
    logic_adapters=[
        # 'chatterbot.logic.MathematicalEvaluation',#the robot can answer 4+6 ?
        # 'chatterbot.logic.TimeLogicAdapter',#the robot can answer current time
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'threshold': 0.97,
            'default_response': 'I am sorry, but I do not understand. I am still learning.',
            'maximum_similarity_threshold': 0.97
        }
    ],
    database_uri='sqlite:///database.sqlite3'
    # database_uri='mongodb://localhost:27017/chatterbot-database'
)
# print("count")
# print(chatbot.storage.count())
# print(chatbot.storage.get_random())

 # Training with Personal Ques & Ans
# conversation = [
#     "Hello",
#     "Hi there!",
#     "How are you doing?",
#     "I'm doing great.",
#     "That is good to hear",
#     "Thank you.",
#     "You're welcome."
# ]
#
# trainer = ListTrainer(chatbot)
# trainer.train(conversation)

training_data_quesans = open('training_data/ques_ans.txt').read().splitlines()
training_data_personal = open('training_data/personal_ques.txt').read().splitlines()

training_data = training_data_quesans + training_data_personal

trainer = ListTrainer(chatbot)
trainer.train(training_data)

# Training with English Corpus Data
#Allows the chat bot to be trained using data from the ChatterBot dialog corpus.
trainer_corpus = ChatterBotCorpusTrainer(chatbot)
trainer_corpus.train(
    'chatterbot.corpus.english'
)