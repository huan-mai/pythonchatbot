import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import nltk
from nltk.stem.lancaster import LancasterStemmer

nltk.download('punkt')
stemmer = LancasterStemmer()

ERROR_THRESHOLD = 0.25
class Prediction(object):
    words = []
    labels = []
    docs_x = []
    docs_y = []
    context =  {}
    def __init__(self, input_file, model_dir = '.'):
        self.MODEL_DIR = model_dir if model_dir else '.'
        self.input_file = input_file

    def load_model(self):
        if hasattr(self, 'data'):
            return

        with open(self.input_file) as file:
            self.data = json.load(file)

        with open("{}/data.pickle".format(self.MODEL_DIR), "rb") as f:
            self.words, self.labels, self.training, self.output = pickle.load(f)
        
        tensorflow.reset_default_graph()
        tflearn.init_graph(num_cores=1)

        net = tflearn.input_data(shape=[None, len(self.training[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")
        net = tflearn.regression(net)
        self.model = tflearn.DNN(net)
        self.model.load("{}/model.tflearn".format(self.MODEL_DIR))
    
    def bag_of_words(self, s):
        bag = [0 for _ in range(len(self.words))]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words]

        print('questions: {}'.format(s_words));
        for se in s_words:
            for i, w in enumerate(self.words):
                if w == se:
                    bag[i] = 1
                
        return numpy.array(bag)

    def classify(self, sentence):
        # generate probabilities from the model
        results = self.model.predict([self.bag_of_words(sentence)])[0]
        # filter out predictions below a threshold
        results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((self.labels[r[0]], r[1]))
        # return tuple of intent and probability
        return return_list

    def response(self, sentence, userID='123', show_details=False):
        results = self.classify(sentence)
        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in self.data["intents"]:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:
                        # set context for this intent if necessary
                        if 'context_set' in i:
                            if show_details: print ('context:', i['context_set'])
                            self.context[userID] = i['context_set']
                        print (self.context)
                        # check if this intent is contextual and applies to this user's conversation
                        if not 'context_filter' in i or \
                            (userID in self.context and 'context_filter' in i and i['context_filter'] == self.context[userID]):
                            if show_details: print ('tag:', i['tag'])
                            # a random response from the intent
                            return random.choice(i['responses'])

                results.pop(0)
