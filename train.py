import scipy as sp
import pandas
import cPickle as pickle
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from text_functions import split_and_adjust
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from utils import plot_feature_importances

dataset = pandas.read_csv('var/data/data.csv')


# label
available_types = ['Ana', 'Bruno', 'Dois']
label_encoder = LabelEncoder()
label_encoder.fit(available_types)
# y = dataset['label']
y = label_encoder.transform(dataset['label'])
pickle.dump(label_encoder, open('var/pickle/last_label_encoder.pkl', 'w'))


# label_encoder da feature TYPE
available_types = ['series', 'movie', 'game']
type_label_encoder = LabelEncoder()
type_label_encoder.fit(available_types)
pickle.dump(type_label_encoder, open('var/pickle/last_type_label_encoder.pkl', 'w'))


# tratar as features
feature_genres = map(lambda text: split_and_adjust(text), dataset['genre'])
feature_actors = map(lambda text: split_and_adjust(text), dataset['actors'])
feature_countries = map(lambda text: split_and_adjust(text), dataset['country'])
feature_languages = map(lambda text: split_and_adjust(text), dataset['language'])
feature_imdb_rating = map(lambda rating: [float(rating)], dataset['imdb_rating'].values)
feature_runtime = map(lambda runtime: [int(runtime)], dataset['runtime'].values)
feature_type = map(lambda type: [type_label_encoder.transform([type])[0]], dataset['type'].values)
# feature_year = map(lambda year: [int(year)/100], dataset['year'].values)


# count_vectorizer
genre_cvt = CountVectorizer()
actor_cvt = CountVectorizer()
country_cvt = CountVectorizer()
language_cvt = CountVectorizer()


# agrupar as features
X = sp.sparse.hstack((
    genre_cvt.fit_transform(feature_genres),
    # actor_cvt.fit_transform(feature_actors),
    # country_cvt.fit_transform(feature_countries),
    # language_cvt.fit_transform(feature_languages),
    feature_imdb_rating,
    # feature_runtime,
    # feature_type,
    # feature_year
), format='csr')

from sklearn.utils import shuffle
X, y = shuffle(X, y, random_state=7)

# salvar ultima versao do CountVectorizer
pickle.dump(genre_cvt, open('var/pickle/last_genre_cvt.pkl', 'w'))
pickle.dump(actor_cvt, open('var/pickle/last_actor_cvt.pkl', 'w'))
pickle.dump(country_cvt, open('var/pickle/last_country_cvt.pkl', 'w'))
pickle.dump(language_cvt, open('var/pickle/last_language_cvt.pkl', 'w'))


# separar data de treino e test (20 porcento)
kf = StratifiedKFold(int(1. / 0.20))
train_indices, test_indices = next(kf.split(X, y))
features_train, labels_train = X[train_indices], y[train_indices]
features_test, labels_test = X[test_indices], y[test_indices]


# treinar classifier
clf = RandomForestClassifier(random_state=7)
clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
print "Accuracy:", accuracy_score(pred, labels_test)
# plot_feature_importances(clf.feature_importances_, 'Decision Tree', np.array(feature_actors))  # exibir features com maior importancia


# salvar classifier
pickle.dump(clf, open('var/pickle/last_clf.pkl', 'w'))


# graficos
# available_labels = ['Ana', 'Bruno', 'Dois']
# label_encoder = LabelEncoder()
# label_encoder.fit(available_labels)
# y = map(lambda label: label_encoder.transform([label])[0], dataset['label'])
# import matplotlib.pyplot as plt
# plt.figure()
# plt.scatter(feature_imdb_rating, y, color='blue')
# plt.scatter(feature_runtime, y, color='red')
# plt.scatter(feature_type, y, color='red')
# plt.show()

# confusion matrix
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
confusion_mat = confusion_matrix(labels_test, pred)
plt.imshow(confusion_mat, interpolation='nearest', cmap=plt.cm.gray)
plt.title('Confusion matrix')
plt.colorbar()
tick_marks = np.arange(3)
plt.xticks(tick_marks, tick_marks)
plt.yticks(tick_marks, tick_marks)
plt.ylabel('True label')
plt.xlabel('Predicted label')
# plt.show()