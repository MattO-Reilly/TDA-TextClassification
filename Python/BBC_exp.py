from packages import *
from functions import *


data = pd.read_csv("./data/bbc-text.csv")
print(f"Shape : {data.shape}, \n\nColumns: {data.columns}, \n\nCategories: {data.category.unique()}")
data.head().append(data.tail())


class DataPreparation:
    def __init__(self, data, column='text'):
        self.df = data
        self.column = column

    def preprocess(self):
        self.tokenize()
        self.remove_stopwords()
        self.remove_non_words()
        self.lemmatize_words()

        return self.df

    def tokenize(self):
        self.df['clean_text'] = self.df[self.column].apply(nltk.word_tokenize)
        print("Tokenization is done.")

    def remove_stopwords(self):
        stopword_set = set(nltk.corpus.stopwords.words('english'))

        def rem_stopword(words): return [
            item for item in words if item not in stopword_set]

        self.df['clean_text'] = self.df['clean_text'].apply(rem_stopword)
        print("Remove stopwords done.")

    def remove_non_words(self):
        """
            Remove all non alpha characters from the text data
            :numbers: 0-9
            :punctuation: All english punctuations
            :special characters: All english special characters
        """
        regpatrn = '[a-z]+'
        def rem_special_chars(x): return [
            item for item in x if re.match(regpatrn, item)]
        self.df['clean_text'] = self.df['clean_text'].apply(rem_special_chars)
        print("Removed non english characters is done.")

    def lemmatize_words(self):
        lemma = nltk.stem.wordnet.WordNetLemmatizer()

        def on_word_lemma(x): return [lemma.lemmatize(w, pos='v') for w in x]

        self.df['clean_text'] = self.df['clean_text'].apply(on_word_lemma)
        print("Lemmatization on the words.")


vectorizer = CountVectorizer()

data_prep = DataPreparation(data)
cleanse_df_freq = data_prep.preprocess()

wordfreq_df = []
for i in cleanse_df_freq['text']:
    vector1 = standardize_text_sentence(str(i))
    CountVecf = TfidfVectorizer()
    appended_data = pd.DataFrame()
    Count_data = CountVecf.fit_transform(vector1)
    cv_dataframe = pd.DataFrame(
        Count_data.toarray(), columns=CountVecf.get_feature_names())
    matrix = (np.array(cv_dataframe, dtype=object))
    wordfreq_df.append(list(matrix))

#cleanse_df_freq['wordfreqvec'] = wordfreq_df
pd.set_option('display.max_colwidth', None)
cleanse_df_freq.to_excel(r'./data/freq_vectors.xlsx', index=False)