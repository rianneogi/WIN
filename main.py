import math
import random
import time

Table = []
TrustTable = []
alpha = 0.34
beta = 0.33

def get_rating(user, item):
    return Table[user][item]

def get_trust_table(u1,u2):
    #print(u1, u2)
    return TrustTable[u1][u2]

def get_trusted_neighbors(user):
    tn = []
    for i in range(len(TrustTable)):
        if get_trust_table(user, i)>=0.5 and user!=i:
            tn.append(i)
    return tn

def jaccard(u1, u2):
    L1 = get_trusted_neighbors(u1)
    L2 = get_trusted_neighbors(u2)

    union = []
    inter = []

    #get intersection
    for i in L1:
        if i in L2:
            inter.append(i)

    #get union
    for i in L1:
        union.append(i)
    for i in L2:
        if i not in L1:
            union.append(i)

    return len(inter)/len(union)

def get_common_ratings(u1, u2):
    sub_L1=[]
    sub_L2=[]
    for i in range(len(Table[u1])):
        if Table[u1][i] != -1 and Table[u2][i] != -1:
            sub_L1.append(Table[u1][i])
            sub_L2.append(Table[u2][i])
    return sub_L1, sub_L2

def get_ratings_from_item_subset(user, subset):
    s = []
    for i in subset:
        s.append(get_rating(user, i))
    return s

def pearson(u1, u2):
    subset = get_common_ratings(u1, u2)
    L1 = subset[0]
    L2 = subset[1]
    #L1 = get_ratings_from_item_subset(u1, subset)
    #L2 = get_ratings_from_item_subset(u2, subset)
    assert(len(L1) == len(L2))
    #print(len(L1))
    if len(L1)==1: #avoid divide by zero
        return 1

    m1=sum(L1)/len(L1)
    m2=sum(L2)/len(L2)
    numerator=0
    den1=0
    den2=0
    for i in range(len(L1)):
        numerator += (L1[i]-m1)*(L2[i]-m2)
        den1 += pow((L1[i]-m1),2)
        den2 += pow((L2[i]-m2),2)

    if numerator==0: #avoid divide by zero
        return 1

    ans=numerator/pow(den1*den2, 0.5)
    return ans

def get_trust_distance(user, neighbor):
    return 1

def calc_mole_trust(u1, u2):
    return get_trust_table(u1,u2)

def get_trust(user, neighbor):
    return calc_mole_trust(user, neighbor)/get_trust_distance(user, neighbor)

def get_weight(user, neighbor):
    return alpha*pearson(user, neighbor) + beta*get_trust(user, neighbor) + (1-alpha-beta)*jaccard(user, neighbor)

def merge_rating(user, item):
    tn = get_trusted_neighbors(user)
    num = 0
    den = 0
    for neighbor in tn:
        weight = get_weight(user, neighbor)
        num += weight * get_rating(neighbor, item)
        den += abs(weight)
    return num/den

def get_number_of_items(name):
    with open(name) as f:
        max=-1
        for line in f:
            id=line.split("|")[0]
            id=int(id)
            if max < id:
                max = id
    return max

def get_ds():
    nrows=get_number_of_items(r"ml-100k/u.user")
    ncols=get_number_of_items(r"ml-100k/u.item")
    global Table
    global TrustTable
    Table=[[-1 for j in range(ncols)] for i in range(nrows)]
    TrustTable = [[0 for j in range(nrows)] for i in range(nrows)]

def fill_ds():
    with open(r"ml-100k/u.data") as f:
        for line in f:
            user, item, rating, a=line.split("\t")
            user=int(user)
            item=int(item)
            rating=int(rating)
            Table[user-1][item-1]=rating

def generate_trust():
    cnt = 0
    while cnt<(len(Table)):
        r = random.randint(2,10)
        for i in range(cnt,cnt+r):
            if i >= len(TrustTable):
                break
            for j in range(cnt,cnt+r):
                if j >= len(TrustTable[i]):
                    break
                TrustTable[i][j] = 1
        cnt = cnt+r

def main():
    random.seed(time.time())

    get_ds()
    fill_ds()
    generate_trust()

    for i in range(10):
        for j in range(10):
            print(merge_rating(i,j),end=" ")
        print("")


main()
#print(jaccard(L1,L2))