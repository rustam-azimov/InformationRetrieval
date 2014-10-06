import sys
import pymorphy2
import pickle

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
docs = index_dict['!files']
query = input('Enter your query or "exit": ')
while not (query == 'exit'):
    query = query.split()
    if not (len(query) % 2):
        print('incorrect query')
        query = input('Enter your query or "exit": ')
        continue
    opers = query[1::2]
    searches = set()
    for w in query[::2]:
        for p in morph.parse(w):
            for l in p.lexeme:
                searches.add(l.word)
    res = set()
    if set(opers) == {'AND'}:
        res = intersection(*[index_dict[search] for search in searches])
    elif set(opers) != {'OR'} and (len(query) + 1) // 2 > 1:
        print('incorrect query')
        query = input('Enter your query or "exit": ')
        continue
    else:
        res = union(*[index_dict[search] for search in searches])
    list_res = list(res)
    n = len(list_res)
    if not n:
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