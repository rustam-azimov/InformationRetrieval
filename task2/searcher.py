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


def split_query(query, oper):
    res = []
    curr = []
    for w in query:
        if w == oper:
            res.append(curr)
            curr = []
        else:
            curr.append(w)
    res.append(curr)
    return res


bools = {"AND", "OR"}
morph = pymorphy2.MorphAnalyzer()
ind_path = sys.argv[1]
f = open(ind_path, 'rb')
index_dict = pickle.load(f)
docs = index_dict['!files'][0]
query = input('Enter your query or "exit": ')
while not (query == 'exit'):
    query = query.split()
    if not (len(query) % 2):
        print('incorrect query1')
        query = input('Enter your query or "exit": ')
        continue
    opers = query[1::2]
    tqueries = []
    bool_oper = ""
    if ("AND" in opers) & ("OR" not in opers):
        tqueries = split_query(query, "AND")
        bool_oper = "AND"
    elif ("AND" not in opers) & ("OR" in opers):
        tqueries = split_query(query, "OR")
        bool_oper = "OR"
    elif ("AND" not in opers) & ("OR" not in opers):
        tqueries = [query]
        bool_oper = "OR"
    else:
        print('incorrect query2')
        query = input('Enter your query or "exit": ')
        continue
    is_correct = True
    res = []
    for tquery in tqueries:
        curr_res = set()
        for p in morph.parse(tquery[0]):
            for l in p.lexeme:
                curr_res = curr_res.union(index_dict[l.word].keys())
        dist_opers = tquery[1::2]
        for i in range(len(dist_opers)):
            dist_oper = dist_opers[i]
            if not dist_oper.startswith('/'):
                is_correct = False
                print(dist_oper)
                break
            dist_oper = dist_oper.lstrip('/')
            to_left = True
            to_right = True
            if dist_oper.startswith("+"):
                to_left = False
                dist_oper = dist_oper.lstrip("+")
            elif dist_oper.startswith("-"):
                to_right = False
                dist_oper = dist_oper.lstrip("-")
            if not dist_oper.isdigit():
                is_correct = False
                break
            step = int(dist_oper)
            dict1 = defaultdict(list)
            dict2 = defaultdict(list)
            word1 = tquery[2 * i]
            word2 = tquery[2 * i + 2]
            keys1 = set()
            keys2 = set()
            for p in morph.parse(word1):
                for l in p.lexeme:
                    curr = index_dict[l.word]
                    for page in curr.keys():
                        dict1[page] += curr[page]
            for p in morph.parse(word2):
                for l in p.lexeme:
                    curr = index_dict[l.word]
                    for page in curr.keys():
                        dict2[page] += curr[page]

            common = intersection(set(dict1.keys()), set(dict2.keys()),
                curr_res)
            curr_res = set()
            for need in common:
                positions1 = set(dict1[need])
                positions2 = set(dict2[need])
                for pos in positions1:
                    if to_left:
                        for pos2 in positions2:
                            if (pos2 < pos) & ((pos - pos2) <= step):
                                curr_res.add(need)
                                break
                    if to_right:
                        for pos2 in positions2:
                            if (pos2 > pos) & ((pos2 - pos) <= step):
                                curr_res.add(need)
                                break
        if not is_correct:
            break
        res.append(curr_res)
    if not is_correct:
        print('incorrect query3')
        query = input('Enter your query or "exit": ')
        continue

    answer = set()

    if bool_oper == 'AND':
        answer = intersection(*[curr_res for curr_res in res])
    else:
        answer = union(*[curr_res for curr_res in res])
    list_answer = list(answer)
    n = len(list_answer)
    if n == 0:
        print('no documents found')
        query = input('Enter your query or "exit": ')
        continue
    print('found ')
    if n == 1:
        print(docs[list_answer[0]])
        query = input('Enter your query or "exit": ')
        continue
    print(docs[list_answer[0]] + ', ' + docs[list_answer[1]])
    if n > 2:
        print('and ' + str(n - 2) + ' more')
    query = input('Enter your query or "exit": ')
