import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import Tree
from nltk.corpus import stopwords
nltk.download('words')

def get_continuous_chunks(text, label):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    founded_words = []

    for subtree in chunked:
        if type(subtree) == Tree: 
            print(subtree.label())    
            if subtree.label() == label:
                founded_words.append(" ".join([token for token, pos in subtree.leaves()]))
    return founded_words

sentence="What is the weather in Chicago or Spain?"
tokens = nltk.word_tokenize(sentence)           # Separamos la frase por palabras
print (tokens)
stop_words = set(stopwords.words('english'))
clean_tokens = [w for w in tokens if not w in stop_words]   # le quitamos las palabras sin significado semántico 'a' 'the' 'is'
print(clean_tokens)
tagged = nltk.pos_tag(clean_tokens)                         # las clasificamos por verbo, sustantivo...
print(tagged)
prueba = get_continuous_chunks(sentence, 'GPE')
print (prueba)
test = nltk.ne_chunk(tagged)                                # Comprueba si hay nombres propios, de ciudades...
print(test)
#print(str(test[2]).split()[0])



