import nltk
nltk.download('punkt')
import time
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

class Train(object):
    words = []
    labels = []
    docs_x = []
    docs_y = []
    MODEL_DIR = os.environ.get('MODEL_DIR')
    MODEL_DIR = MODEL_DIR if MODEL_DIR else '.'
    def training(self):
        with open("intents.json") as file:
            self.data = json.load(file)

        for intent in self.data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                self.words.extend(wrds)
                self.docs_x.append(wrds)
                self.docs_y.append(intent["tag"])

            if intent["tag"] not in self.labels:
                self.labels.append(intent["tag"])

        self.words = [stemmer.stem(w.lower()) for w in self.words if w != "?"]
        self.words = sorted(list(set(self.words)))

        self.labels = sorted(self.labels)

        self.training = []
        self.output = []

        out_empty = [0 for _ in range(len(self.labels))]

        for x, doc in enumerate(self.docs_x):
            bag = []

            wrds = [stemmer.stem(w.lower()) for w in doc]

            for w in self.words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[self.labels.index(self.docs_y[x])] = 1

            self.training.append(bag)
            self.output.append(output_row)


        self.training = numpy.array(self.training)
        self.output = numpy.array(self.output)

        with open("{}/data.pickle".format(self.MODEL_DIR), "wb") as f:
            pickle.dump((self.words, self.labels, self.training, self.output), f)

        tensorflow.reset_default_graph()
        tflearn.init_graph(num_cores=1, gpu_memory_fraction=0.5)

        net = tflearn.input_data(shape=[None, len(self.training[0])])
        # two hidden layers with 8 neurons of each layer. This is where you can do more tuning.
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        # turn result to probability rather than a number for classification: softmax, relu, sigmoid
        net = tflearn.fully_connected(net, len(self.output[0]), activation="softmax")

        net = tflearn.regression(net)
        # net = tflearn.regression(net, optimizer='sgd', learning_rate=0.01, loss='mean_square')

        self.model = tflearn.DNN(net)
        self.model.fit(self.training, self.output, n_epoch=200, batch_size=2, show_metric=True)
        self.model.save("{}/model.tflearn".format(self.MODEL_DIR))

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

    def start(self):
        if hasattr(self, 'data'):
            return

        with open("intents.json") as file:
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

    def answer(self, inp):
        t = time.process_time()
        results = self.model.predict([self.bag_of_words(inp)])
        results_index = numpy.argmax(results)
        print('results_index {} of {}'.format(results, results_index))
        tag = self.labels[results_index]
        
        responses = ['Sorry']
        for tg in self.data["intents"]:
            print('label {} in {}'.format(tag, tg['tag']))
            if tg['tag'] == tag:
                responses = tg['responses']
        elapsed_time = time.process_time() - t
        print('Time To answer is {}'.format(elapsed_time))
        return random.choice(responses)
