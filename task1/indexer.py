import sys
import string
from os import listdir
from os.path import isfile, join
import pymorphy2
import codecs

doc_path = sys.argv[1]
ind_path = sys.argv[2]
only_files = [f for f in listdir(doc_path) if isfile(join(doc_path,f))]
morph = pymorphy2.MorphAnalyzer()
intab = string.punctuation
outtab = ' ' * len(string.punctuation)
index_dict = dict()
for i in range(len(only_files)):
    f = codecs.open(doc_path + '/' + only_files[i], encoding='utf-8', mode='r')
    words = f.read().translate({ord(x): y for (x, y) in zip(intab, outtab)}).lower().split()
    for word in words:
        normal = morph.parse(word)[0].normal_form
        value = index_dict.get(normal, [])
        if str(i) not in value:
            index_dict[normal] = value + [str(i)]
    f.close()   

index_inv = codecs.open(ind_path, 'w', 'utf-8')
index_inv.write(" ".join(only_files))  
for word in index_dict.keys():
    values = " ".join(index_dict[word])
    index_inv.write('\n' + word + " " + values)
index_inv.close()