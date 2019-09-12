import json
import pickle
import nltk
import numpy
import tflearn
import tensorflow
from nltk.stem.lancaster import LancasterStemmer
nltk.download('punkt')
_stemmer = LancasterStemmer()

class Train:
    def __init__(self, input_file, model_dir):
        self.model_dir = model_dir if model_dir else '.'
        self.input_file = input_file
        self.docs_x = []
        self.docs_y = []

    def to_binary_array(self, words, labels):
        training = []
        output = []
        out_empty = [0 for _ in range(len(labels))]
        for x, doc in enumerate(self.docs_x):
            bag = []

            wrds = [_stemmer.stem(w.lower()) for w in doc]

            for w in words:
                    bag.append(1 if w in wrds else 0)

            output_row = out_empty[:]
            output_row[labels.index(self.docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)
        return numpy.array(training), numpy.array(output)

    def parse_intents_file(self):
        words = []
        labels = []
        with open(self.input_file) as file:
            data = json.load(file)

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                self.docs_x.append(wrds)
                self.docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])
        return labels, words

    def training(self):
        labels, words = self.parse_intents_file()
        
        words = [_stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))

        labels = sorted(labels)

        training, output = self.to_binary_array(words, labels)

        with open("{}/data.pickle".format(self.model_dir), "wb") as f:
            pickle.dump((words, labels, training, output), f)

        tensorflow.reset_default_graph()
        tflearn.init_graph(num_cores=1, gpu_memory_fraction=0.5)

        net = tflearn.input_data(shape=[None, len(training[0])])
        # two hidden layers with 8 neurons of each layer. This is where you can do more tuning.
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        # turn result to probability rather than a number for classification: softmax, relu, sigmoid
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")

        net = tflearn.regression(net)
        # net = tflearn.regression(net, optimizer='sgd', learning_rate=0.01, loss='mean_square')

        model = tflearn.DNN(net)
        model.fit(training, output, n_epoch=200, batch_size=2, show_metric=True)
        model.save("{}/model.tflearn".format(self.model_dir))
