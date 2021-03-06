
# coding: utf-8

# In[74]:

#pandas for reading csv
#numpy for mathematical calculations
import pandas as pd, numpy as np
#regular expression - manipulate sentences
import re

#Hyperparameters
#MAX_NB_WORDS provides limit of words stored in vocabulary
MAX_NB_WORDS = 200000
#MAX_SEQUENCE_LENGTH sets limit of words in sequence
MAX_SEQUENCE_LENGTH = 150


# In[75]:


#Load whole yahoo TRAINING dataset from filepath
unprocessed_training_data = pd.read_csv(r'C:\Users\maximilian.weber\OneDrive - Synpulse\UserRoaming\Desktop\TextClassificationDatasets-20181112T073934Z-001\TextClassificationDatasets\yahoo_answers_csv\train.csv', header=None)
#own header titles
unprocessed_training_data.columns = ['labels','questions_1','questions_2', 'features']


# In[76]:


#Load whole yahoo TESTING dataset from filepath
unprocessed_testing_data = pd.read_csv(r'C:\Users\maximilian.weber\OneDrive - Synpulse\UserRoaming\Desktop\TextClassificationDatasets-20181112T073934Z-001\TextClassificationDatasets\yahoo_answers_csv\test.csv', header=None)
#Own header titles
unprocessed_testing_data.columns = ['labels','questions_1','questions_2', 'features']


# In[83]:


#delete unnecessary columns of TRAINING dataset
del unprocessed_training_data['questions_1']
del unprocessed_training_data['questions_2']


# In[84]:


#delete unnecessary columns of TESTING dataset
del unprocessed_testing_data['questions_1']
del unprocessed_testing_data['questions_2']


# In[87]:


#delete all rows without content of TRAINING dataset
processed_training_data = unprocessed_training_data.dropna()


# In[88]:


#delete all rows without content of TESTING dataset
processed_testing_data = unprocessed_testing_data.dropna()


# In[91]:


#Get data content of TRAINING data with label 1-3
training_data_label_1 = processed_training_data[processed_training_data["labels"] == 1]
training_data_label_2 = processed_training_data[processed_training_data["labels"] == 2]
training_data_label_3 = processed_training_data[processed_training_data["labels"] == 3]


# In[92]:


##Get data content of TESTING data with label 1-3
testing_data_label_1 = processed_testing_data[processed_testing_data['labels'] == 1]
testing_data_label_2 = processed_testing_data[processed_testing_data['labels'] == 2]
testing_data_label_3 = processed_testing_data[processed_testing_data['labels'] == 3]


# In[95]:


#cut ONLY TRAINING datasets with label 1-3 to size of 50'000
training_data_label_1 = training_data_label_1[:50000]
training_data_label_2 = training_data_label_2[:50000]
training_data_label_3 = training_data_label_3[:50000]


# In[98]:


#merge TRAINING data label 1 with 2
training_data_label_1_2 = training_data_label_1.append(training_data_label_2)
#merge training data label 1 & 2 with 3
training_data_label_1_2_3 = training_data_label_1_2.append(training_data_label_3)


# In[102]:


#merge TESTING data label 1 with 2
testing_data_label_1_2 = testing_data_label_1.append(testing_data_label_2)
#merge TESTING data label 1 & 2 with 3
testing_data_label_1_2_3 = testing_data_label_1_2.append(testing_data_label_3)


# In[105]:


#shuffle TRAINING data
from sklearn.utils import shuffle
shuffled_training_data = shuffle(training_data_label_1_2_3)
#shuffle TESTING data
shuffled_testing_data = shuffle(testing_data_label_1_2_3)


# In[107]:


#unordered because data was removed & appended --> some n/a arrays
#fill x_train_unordered with TRAINING sentences
#fill y_train_unordered with corresponding labels
x_train_unordered = shuffled_training_data['features']
y_train_unordered = shuffled_training_data['labels']


# In[109]:


#unordered because data was removed & appended --> some n/a arrays
#fill x_test_unordered with testing sentences
#fill y_test_unordered with corresponding labels (validation purpose ONLY)
x_test_unordered = shuffled_testing_data['features']
y_test_unordered = shuffled_testing_data['labels']


# In[111]:


#removes n/a arrays in x_train_unordered and y_train_unordered
x_train = []
y_train = []
for i in y_train_unordered:
    y_train.append(i)

for i in x_train_unordered:
    x_train.append(str(i))

#important for keras model (matrix format)
y_train = np.array(y_train).reshape(-1,1)


# In[112]:


#removes n/a arrays in x_test_unordered and y_test_unordered
x_test = []
y_test = []
for i in y_test_unordered:
    y_test.append(i)

for i in x_test_unordered:
    x_test.append(i)
#no need for reshaping because nothing gets trained in keras model


# In[113]:


#WordNetLemmatizer formats words back to its basis - removes noise in dataset
#example: go, went, gone, goes, going --> go
import nltk
from nltk.stem import WordNetLemmatizer
#stopwords removes any unvaluable words like this, for, in, ...
from nltk.corpus import stopwords
nltk.download('wordnet')


# In[114]:

@Pre raw sentences as Args
@Post cleaned wordlist
#convert into a list of words
#remove unnecessary split into words, no hyphens
def sentence_to_wordlist(raw):
    """
    Receives a raw sentence and cleans it using the following steps:
    1. Includes only words and numbers
    2. Transforms the review in lower case
    3. Removes all stop words
    4. Performs lemmatize
    """

    clean = re.sub("[^A-Za-z0-9]", " ", str(raw))
    clean = clean.lower()
    review = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
    clean = review.sub('', str(clean))
    clean = clean.split()

    lemmatizer = WordNetLemmatizer()
    clean = [lemmatizer.lemmatize(i, pos='v') for i in clean]
    return clean


# In[43]:


#displays loading bar
from tqdm import tqdm
#split TRAINING sentences into wordlist
split_training_sentences = []
for raw_sentence in tqdm(x_train):
    split_training_sentences.append(sentence_to_wordlist(raw_sentence))


# In[45]:


#split TESTING sententes into wordlist
split_testing_sentences = []
for raw in tqdm(x_test):
    split_testing_sentences.append(sentence_to_wordlist(raw))


# In[72]:


#text to numbers ordered by most used 1 to less used high number
from keras.preprocessing.text import Tokenizer

#allows to vectorize a text corpus, by turning each text into a sequence of integers
tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(split_training_sentences)

tokenized_training_set = tokenizer.texts_to_sequences(split_training_sentences)
tokenized_testing_set = tokenizer.texts_to_sequences(split_testing_sentences)
vocab_size = len(tokenizer.word_index) + 1  # Adding 1 because of reserved 0 index


# In[73]:


import pickle
#saves tokenizer
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)


# In[48]:


#pad every sentence to the same sentence length (necessary for matrix calculations)
from keras.preprocessing.sequence import pad_sequences
maxlen = MAX_SEQUENCE_LENGTH
padded_training_set = pad_sequences(tokenized_training_set, maxlen=maxlen)
padded_testing_set = pad_sequences(tokenized_testing_set, maxlen=maxlen)


# In[50]:

@Pre filepath of pretrained model, word_index of pretrained tokenizer, embedding_dim as Hyperparameter
@Post returns embedding_matrix which is used in keras model
#creates embedding matrix for later use with pretrained glove model
def create_embedding_matrix(filepath, word_index, embedding_dim):
    vocab_size = len(word_index) + 1  # Adding again 1 because of reserved 0 index
    embedding_matrix = np.zeros((vocab_size, embedding_dim))

    with open(filepath, encoding="utf8") as f:
        for line in f:
            word, *vector = line.split()
            if word in word_index:
                idx = word_index[word]
                embedding_matrix[idx] = np.array(
                    vector, dtype=np.float32)[:embedding_dim]

    return embedding_matrix


# In[51]:


#builds embedding_matrix with pretrained glove model
embedding_dim = 50
embedding_matrix = create_embedding_matrix(
    r'C:\Users\maximilian.weber\Downloads\glove.6B\glove.6B.50d.txt',
    tokenizer.word_index, embedding_dim)


# In[52]:


#necessary if model classifies non-binary
from keras.utils.np_utils import to_categorical
categorical_labels = to_categorical(y_train)


# In[53]:


#keras model
from keras.models import Sequential
from keras import layers
#embedding_dim = 50 --> unnecessary predefined above
model = Sequential()
model.add(layers.Embedding(input_dim=vocab_size,
                           output_dim=embedding_dim,
                           weights=[embedding_matrix],
                           input_length=maxlen,
                           trainable=True))
model.add(layers.SpatialDropout1D(0.5))
model.add(layers.LSTM(196, dropout=0.2, recurrent_dropout=0.2))
model.add(layers.Dense(4, activation='softmax'))
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary()


# In[54]:


history = model.fit(padded_training_set, categorical_labels, batch_size=64, epochs=3, validation_split=0.1)


# In[59]:


results = model.predict(padded_testing_set)


# In[69]:


# Save the weights
model.save_weights('model_weights.h5')
# Save the model architecture
with open('model_architecture.json', 'w') as f:
    f.write(model.to_json())


# In[67]:


#TESTING
number = 501

probability = max(results[number])
predicted_category = np.argmax(results[number])
true_category = y_test[number]
text_sequence = split_testing_sentences[number]

print('I\'m ' + str(round(probability * 100)) + '% sure about my prediction!')
print(100*'_')
if predicted_category == 1:
    print('predicted: Society & Culture')
elif predicted_category == 2:
    print('predicted: Science & Math')
elif predicted_category == 3:
    print('predicted: Health')
print(100*'_')
if true_category == 1:
    print('True Category: Society & Culture')
elif true_category == 2:
    print('True Category: Science & Math')
elif true_category == 3:
    print('True Category: Health')
print(100*'_')
print(text_sequence)
print(100*'_')
print(x_test[number])


# In[61]:


#model predictor
example = input('Test: ')
example = sentence_to_wordlist(example)
example = tokenizer.texts_to_sequences([example])
example = pad_sequences(example, maxlen=maxlen)

category_probability = model.predict(example)

print(max(category_probability[0]))

number = np.argmax(category_probability)
if number == 1:
    print('Society & Culture')
elif number == 2:
    print('Science & Math')
elif number == 3:
    print('Health')
