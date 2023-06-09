import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np



class SentenceVectorizer() :
    
    def __stop_words(self) -> set[str]:
        stop_words = set(stopwords.words('English'))
        stop_words = stop_words.union({",", ".", "'s", "(", ")", "{", "}", "[", "]"})
        return stop_words
    
        
    def sentences_to_vector(self, obj, Tfidf_vectorizer:bool = True) -> list:
        """
        Description:
        ------------
        This function will take a `string of one or many sentence` or a `list of sentences` as 'obj' arguements/parameter.
        Tfidf_vectorizer is True by default. If Tfidf_vectorizer = True, The function will Use CountVectorizer

        Returns:
        --------
        An Vector array generated by TfidfVectorizer() or CountVectorizer() ; depends on parameter.
        """
                
        if type(obj) is not list:
            text = obj
            tokenized_sent = sent_tokenize(text.lower())            
            tokenized_word = [word_tokenize(tx) for tx in tokenized_sent]
        
        else :
            tokenized_word = list(map(word_tokenize, obj))
        

        # filtering tokens from stopwords
        stop_words = self.__stop_words()
        filtered_tokenz = [[word for word in wordArray if word not in stop_words] for wordArray in tokenized_word]

        # lemmatizing all tokens
        lemmatizer = WordNetLemmatizer()
        lem_tokenz = [[lemmatizer.lemmatize(word) for word in wordArray] for wordArray in filtered_tokenz]

        # transforming each tokenized array to sentence
        lem_sentence = [(' ').join(arr) for arr in lem_tokenz]

        # converting these sentences to vector
        if Tfidf_vectorizer == True :
            self.__vectorizer = TfidfVectorizer()            
        else :
            self.__vectorizer = CountVectorizer()
            
            
        vectored_form = self.__vectorizer.fit_transform(lem_sentence)
        vectored_form = vectored_form.toarray()
        return vectored_form.tolist()
    
    
    
    def get_features_name_out(self):
        try:
            x = self.__vectorizer.get_feature_names_out()
            x = np.array(x).tolist()
            return x
        except:
            raise Exception("Vectorizer hasn't initialized yet. Couldn't get the feature names")
