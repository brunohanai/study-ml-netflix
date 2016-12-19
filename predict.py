import cPickle as pickle
import scipy as sp
import omdb
from text_functions import split_and_adjust
from data_manager import adjust_omdb_info

genre_cvt = pickle.load(open('var/pickle/last_genre_cvt.pkl', 'r'))
actor_cvt = pickle.load(open('var/pickle/last_actor_cvt.pkl', 'r'))
country_cvt = pickle.load(open('var/pickle/last_country_cvt.pkl', 'r'))
language_cvt = pickle.load(open('var/pickle/last_language_cvt.pkl', 'r'))
clf = pickle.load(open('var/pickle/last_clf.pkl', 'r'))
tle = pickle.load(open('var/pickle/last_type_label_encoder.pkl', 'r'))
le = pickle.load(open('var/pickle/last_label_encoder.pkl', 'r'))

title = raw_input('Title: ')

omdb_info = omdb.title(title)

if len(omdb_info) == 0:
    print 'OMDB Info not Found'
    exit()

omdb_info = adjust_omdb_info(omdb_info)
print omdb_info

X_pred = sp.sparse.hstack((
    genre_cvt.transform([split_and_adjust(omdb_info['genre'])]),
    # actor_cvt.transform([split_and_adjust(omdb_info['actors'])]),
    # country_cvt.transform([split_and_adjust(omdb_info['country'])]),
    # language_cvt.transform([split_and_adjust(omdb_info['language'])]),
    # float(omdb_info['imdb_rating']),
    # int(omdb_info['runtime'].split()[0]),
    # tle.transform([omdb_info['type']])[0]
))
# print X_pred.toarray()

print "\nPrevisao ---> ", le.inverse_transform(clf.predict(X_pred))