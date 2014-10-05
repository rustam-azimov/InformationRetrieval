import sys
import codecs
import pymorphy2

ind_path = sys.argv[1]
f = codecs.open(ind_path, encoding='utf-8', mode='r')
docs = f.readline().split()
words = []
indexes = []
for line in f:
    list = line.split()
    words.append(list[0])
    indexes.append(list[1::])

query = input('Enter your query or "exit": ')
while not (query == 'exit'):
    query = query.split()
    if not (len(query) % 2):
        print('incorrect query')
        query = input('Enter your query or "exit": ')
        continue
    n = (len(query) + 1) // 2
    opers = query[1::2]
    isAnds = False
    if set(opers) == {'AND'}:
        isAnds = True
    elif set(opers) != {'OR'} and n > 1:
        print('incorrect query')
        query = input('Enter your query or "exit": ')
        continue
    lines = []
    searches = query[::2]
    for search in searches:
        if search in words:
            i = words.index(search)
            lines.append(i)
    s = set()
    if isAnds:
        if len(lines) != n:
            print('no documents found')
            query = input('Enter your query or "exit": ')
            continue
        s = set(indexes[lines[0]])
        for i in range(1, n):
            s = s.intersection(set(indexes[lines[i]]))
    else:
        for i in range(len(lines)):
            s = s.union(set(indexes[lines[i]]))
    res = []
    for e in s:
        res.append(e)
    if not len(res):
        print('no documents found')
        query = input('Enter your query or "exit": ')
        continue
    print('found ')
    if len(res) == 1:
        print(docs[int(res[0])])
        query = input('Enter your query or "exit": ')
        continue
    print(docs[int(res[0])] + ', ' + docs[int(res[1])])
    if len(res) > 2:
        print('and ' + str(len(res) - 2) + ' more')   
    query = input('Enter your query or "exit": ')