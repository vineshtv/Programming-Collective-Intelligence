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


if __name__ == "__main__":
    rownames, colnames, data = readfile('blogdata.txt')

