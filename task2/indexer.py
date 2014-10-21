import sys
import string
from os import listdir
from os.path import isfile, join
import codecs
import pickle
from collections import defaultdict

exclude = set(string.punctuation)

def parser(ch):
    if (ch in exclude):
        return ' '
    return ch

doc_path = sys.argv[1]
ind_path = sys.argv[2]
only_files = [f for f in listdir(doc_path) if isfile(join(doc_path,f))]
index_dict = defaultdict(defaultdict)
for i in range(len(only_files)):
    print('indexing... ' + only_files[i])
    f = codecs.open(doc_path + '/' + only_files[i], encoding='utf-8', mode='r')
    words = ''.join(parser(ch) for ch in f.read()).replace(u'\ufeff', '').lower().split()
    for j in range(len(words)):
        curr = index_dict[words[j]].get(i, [])
        if not curr:
            curr = [j]
        else:
            curr.append(j)
        index_dict[words[j]][i] = curr
    f.close()
index_dict['!files'][0] = only_files
index_inv = open(ind_path, 'wb')
pickle.dump(index_dict, index_inv)
index_inv.close()