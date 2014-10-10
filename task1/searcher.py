import sys
import pymorphy2
import pickle
from collections import defaultdict

def union(*sets):
    prev_set = set()
    for s in sets:
        prev_set = set(s).union(prev_set)
    return prev_set

def intersection(first, *sets):
    prev_set = first
    for s in sets:
        prev_set = s.intersection(prev_set)
    return prev_set

morph = pymorphy2.MorphAnalyzer()
ind_path = sys.argv[1]
f = open(ind_path, 'rb')
index_dict = pickle.load(f)
docs_set = index_dict['!files']
docs = []
for strs in docs_set:
    docs = strs.split()
query = input('Enter your query or "exit": ')
while not (query == 'exit'):
    query = query.split()
    if not (len(query) % 2):
        print('incorrect query')
        query = input('Enter your query or "exit": ')
        continue
    opers = query[1::2]
    searches = defaultdict(set)
    for w in query[::2]:
        for p in morph.parse(w):
            for l in p.lexeme:
                searches[w] = searches[w].union(index_dict[l.word])
    res = set()
    if set(opers) == {'AND'}:
        res = intersection(*[searches[key] for key in searches])
    elif set(opers) != {'OR'} and (len(query) + 1) // 2 > 1:
        print('incorrect query')
        query = input('Enter your query or "exit": ')
        continue
    else:
        res = union(*[searches[key] for key in searches])
    list_res = list(res)
    n = len(list_res)
    if n == 0:
        print('no documents found')
        query = input('Enter your query or "exit": ')
        continue
    print('found ')
    if n == 1:
        print(docs[list_res[0]])
        query = input('Enter your query or "exit": ')
        continue
    print(docs[list_res[0]] + ', ' + docs[list_res[1]])
    if n > 2:
        print('and ' + str(n - 2) + ' more')   
    query = input('Enter your query or "exit": ')