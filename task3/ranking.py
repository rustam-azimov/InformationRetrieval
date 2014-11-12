from math import log

PBREAK = 0.15
MAXGRADE = 3


def DCG(n, grad):
    dcg = 0
    for i in range(1, n + 1):
        dcg += (2 ** grad[i - 1] - 1) / log(i + 1, 2)
    return dcg


def IDCG(n, grad):
    return DCG(n, sorted(grad[:n], reverse=True))


def NDCG(n, grad):
    return DCG(n, grad) / IDCG(n, grad)


def PFound(n, grad):
    pLook = 1
    normalize = 2 ** MAXGRADE
    pfound = 0
    for i in range(n):
        pRel = (2 ** grad[i] - 1) / normalize
        pfound += pLook * pRel
        pLook = pLook * (1 - pRel) * (1 - PBREAK)
    return pfound


n = int(input("Enter n = "))
str = input("Enter grades: ")
grad = [int(grade) for grade in str.split()]
print("DCG = {}".format(DCG(n, grad)))
print("NDCG = {}".format(NDCG(n, grad)))
print("PFound = {}".format(PFound(n, grad)))
