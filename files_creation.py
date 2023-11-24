import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
from functools import reduce
import pandas as pd 
import nltk
from nltk.corpus import stopwords

#reading dataset 
msc_degrees = pd.read_csv('msc_degrees.csv')

#cleaning description column to be able to run the following code 
stopw = stopwords.words('english')
msc_degrees['description_clean'] = msc_degrees.description.apply(lambda row: nltk.word_tokenize(row)).apply(lambda row: ([nltk.PorterStemmer().stem(word) for word in row if (word.isalnum() and (not word in stopw))])) 


#VOCABULARY FILE
# creating vocabulary lists as a tool to write the vocabulary file 
vocabulary_list = sorted(list(Counter(reduce(lambda x, y: x+y, msc_degrees.description_clean.values)).keys()))
vocabulary_idx = dict(zip(vocabulary_list, list(range( len(vocabulary_list)))))
    
# save dictionary to vocabulary.pkl file
with open('vocabulary.pkl', 'wb') as v_file:
    pickle.dump(vocabulary_idx, v_file)

v_file.close()


#INVERTED INDEX FILE (WITHOUT TFIDF)
# Read dictionary pkl file
with open('vocabulary.pkl', 'rb') as v_file:
    vocabulary_dict = pickle.load(v_file)

#function to get the documents in which term appears
get_documents_list = lambda word:  list(msc_degrees.loc[msc_degrees.description_clean.apply(lambda row: word in row )].index)

#initializing inverted_index_dict
inverted_index = dict()

#updating the inverted_index dictionary
for key in vocabulary_dict:
    #saving needed values in order to call the funcion only once per term 
    doc_list =  get_documents_list(key) 

    #updating dict
    inverted_index.update({vocabulary_dict[key] : doc_list})

# save dictionary to inverted_index.pkl file
with open('inverted_index.pkl', 'wb') as invidx_file:
    pickle.dump(inverted_index, invidx_file)

invidx_file.close()


# INVERTED INDEX FILE (WITH TFIDF)
# calculating tfidf 
tfidf = TfidfVectorizer(lowercase=False, tokenizer=lambda text: text)  #input='content', lowercase=False, tokenizer=lambda text: text
tfidf_matrix = tfidf.fit_transform(msc_degrees.description_clean)

#Read inverted_index pkl file (needed to construct inverted_index with tfidf)
with open('inverted_index.pkl', 'rb') as invidx_file:
    inverted_index = pickle.load(invidx_file)

invidx_file.close()

#creating inverted index (with tfidf) dictionary
inverted_index_tfidf = dict()
for term_id in inverted_index:
    inverted_index_tfidf.update( { term_id: dict([ (doc_id, tfidf_matrix[(doc_id , term_id)] ) for doc_id in inverted_index[term_id] ]) } )

#saving the dictionary as a pickle file
with open('inverted_index_tfidf.pkl', 'wb') as tfidf_file:
    pickle.dump(inverted_index_tfidf, tfidf_file)

tfidf_file.close()


#ISO CURRENCY DICTIONARY 
ISO_currency_dict = {
    '$' : 'USD',
    '£' : 'GBP',
    '¥': 'JPY',
    '֏': 'AMD',
    '؋': 'AFN',
    '৲': 'BDT',
    '৳': 'BDT',
    '৻': 'VES',
    '૱': 'KHR',
    '௹': 'LKR',
    '฿': 'THB',
    '៛': 'KHR',
    'euro' : 'EUR',
    'euros' : 'EUR',
    'Euro' : 'EUR',
    'Euros' : 'EUR',
    'Eur' : 'EUR',
    'US$' : 'USD',
    'USD': 'USD',
    'EUR': 'EUR',
    'GBP': 'GBP',
    'JPY': 'JPY',
    'INR': 'INR',
    'AUD': 'AUD',
    'CAD': 'CAD',
    'HK': 'HKD',
    'ISK': 'ISK',
    'RMB': 'CNY',
    'SEK': 'SEK',
    'CHF': 'CHF',
    
    #'\u20a0-\u20bd': below
    '₡': 'CRC', #Costa Rican Colón
    '₤': 'ITL', # Italian Lira
    '₥': 'DEM', # German Mark
    '₦': 'NGN', # Nigerian Naira
    '₧': 'ESP', # Spanish Peseta
    '₨': 'INR', # Indian Rupee
    '₩': 'KRW', # South Korean Won
    '₪': 'ILS', # Israeli New Shekel
    '₫': 'VND', # Vietnamese Đồng
    '€': 'EUR', # Euro
    '₭': 'LAK', # Lao Kip
    '₮': 'MNT', # Mongolian Tugrik
    '₯': 'GRD', # Greek Drachma
    '₱': 'PHP', # Philippine Peso
    '₲': 'PYG', # Paraguayan Guarani
    '₴': 'UAH', # Ukrainian Hryvnia
    '₵': 'GHS', # Ghanaian Cedi    
}

    
# save dictionary to ISOcurrency.pkl file
with open('ISOcurrency.pkl', 'wb') as iso_file:
    pickle.dump(ISO_currency_dict, iso_file)

iso_file.close()