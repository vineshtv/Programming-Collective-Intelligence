from math import sqrt

def readfile(filename):
    lines=[line for line in file(filename)]
    #first name is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        #first col in each row is the row name
        rownames.append(p[0])
        #the data for this row is the remained of the row.
        data.append([float(x) for x in p[1:]])
    return rownames,colnames,data

def pearson(v1, v2):
    #simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    #sum of squares
    sum1Sq = sum([pow(v,2) for v in v1])
    sum2Sq = sum([pow(v,2) for v in v2])

    #sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    #Calculate r (pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2)/len(v1)) * (sum2Sq - pow(sum2, 2)/len(v1)))

    if den == 0:
        return 0

    return 1.0 - num / den


class bicluster:
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance

def hcluster(rows, distance = pearson):
    distances = {}
    currentClustId = -1

    #clusters are initially just the rows
    clust = [bicluster(rows[i], id = i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestPair = (0,1)
        closest = distance(clust[0].vec, clust[1].vec)

        #loop through every pair looking for the smallest distance
        for i in range(len(clust)):
            for j in range(i+1, len(clust)):
                #distance is the cache of distance calculation
                if(clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestPair = (i, j)

        #calculate the average of the two clusters
        mergeVec = [(clust[lowestPair[0]].vec[i] + clust[lowestPair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]

        #create the new cluster
        newCluster = bicluster(mergeVec, 
                               left = clust[lowestPair[0]], 
                               right = clust[lowestPair[1]],
                               distance = closest, 
                               id = currentClustId)

        #cluster ids that werent in the original set are negative
        currentClustId -= 1
        del clust[lowestPair[1]]
        del clust[lowestPair[0]]

        clust.append(newCluster)

    return clust[0]

def printclust(clust, labels=None, n = 0):
    #indent to make a hierarchy layout
    for i in range(n): print ' ',
    if clust.id < 0:
        #negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels == None: 
            print clust.id
        else:
            print labels[clust.id]

    #now print the right and left branches
    if clust.left != None:
        printclust(clust.left, labels = labels, n = n + 1)

    if clust.right != None:
        printclust(clust.right, labels = labels, n = n + 1)

if __name__ == "__main__":
    rownames, colnames, data = readfile('blogdata.txt')
    clust = hcluster(data)
    printclust(clust, labels = rownames)

