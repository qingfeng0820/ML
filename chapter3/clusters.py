# -*- coding: utf-8 -*-

# from PIL import Image, ImageDraw
import random
from math import sqrt


def readfile(filename):
    lines = [line for line in file(filename)]

    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the row name
        rownames.append(p[0])
        # The data for this row is the remainder of the row
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    # 返回值是以1.0减去pearson相关度之后的结果，这样做的目的是为了让相似度越大的两个元素之间的距离变得更小
    return 1.0 - num / den


def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0

    for i in range(len(v1)):
        if v1[i] != 0: c1 += 1  # in v1
        if v2[i] != 0: c2 += 1  # in v2
        if v1[i] != 0 and v2[i] != 0: shr += 1  # in both

    return 1.0 - (float(shr) / (c1 + c2 - shr))


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # Clusters are initially just the rows
    cluster = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(cluster) > 1:
        lowestpair = (0, 1)
        closest = distance(cluster[0].vec, cluster[1].vec)

        # loop through every pair looking for the smallest distance
        for i in range(len(cluster)):
            for j in range(i + 1, len(cluster)):
                # distances is the cache of distance calculations
                if (cluster[i].id, cluster[j].id) not in distances:
                    distances[(cluster[i].id, cluster[j].id)] = distance(cluster[i].vec, cluster[j].vec)

                d = distances[(cluster[i].id, cluster[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # calculate the average of the two clusters
        mergevec = [
            (cluster[lowestpair[0]].vec[i] + cluster[lowestpair[1]].vec[i]) / 2.0
            for i in range(len(cluster[0].vec))]

        # create the new cluster
        newcluster = bicluster(mergevec, left=cluster[lowestpair[0]],
                               right=cluster[lowestpair[1]],
                               distance=closest, id=currentclustid)

        # cluster ids that weren't in the original set are negative
        currentclustid -= 1
        del cluster[lowestpair[1]]
        del cluster[lowestpair[0]]
        cluster.append(newcluster)

    return cluster[0]


def printhcluster(cluster, labels=None, indent=0):
    # indent to make a hierarchy layout
    for i in range(indent): print ' ',
    if cluster.id < 0:
        # negative id means that this is branch
        print '-'
    else:
        # positive id means that this is an endpoint
        if labels == None:
            print cluster.id
        else:
            print labels[cluster.id]

    # now print the right and left branches
    if cluster.left != None: printhcluster(cluster.left, labels=labels, indent=indent + 1)
    if cluster.right != None: printhcluster(cluster.right, labels=labels, indent=indent + 1)


def getheight(cluster):
    # Is this an endpoint? Then the height is just 1
    if cluster.left == None and cluster.right == None: return 1

    # Otherwise the height is the same of the heights of
    # each branch
    return getheight(cluster.left) + getheight(cluster.right)


def getdepth(cluster):
    # The distance of an endpoint is 0.0
    if cluster.left == None and cluster.right == None: return 0

    # The distance of a branch is the greater of its two sides
    # plus its own distance
    return max(getdepth(cluster.left), getdepth(cluster.right)) + cluster.distance


def rotatematrix(data):
  newdata=[]
  for i in range(len(data[0])):
    newrow=[data[j][i] for j in range(len(data))]
    newdata.append(newrow)
  return newdata


def kcluster(rows, distance=pearson, k=4, max_iterate_count=100):
    # Determine the minimum and maximum values for each point
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows]))
              for i in range(len(rows[0]))]

    # Create k randomly placed centroids
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0]
                 for i in range(len(rows[0]))] for j in range(k)]

    lastmatches = None
    for t in range(max_iterate_count):
        print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)]

        # Find which centroid is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            bestmatch = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatch], row): bestmatch = i
            bestmatches[bestmatch].append(j)

        # If the results are the same as last time, this is complete
        if bestmatches == lastmatches:
            print "Iteration End"
            break
        lastmatches = bestmatches

        # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(bestmatches[i]) > 0:
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                clusters[i] = avgs

    return bestmatches


def printkcluster(cluster, labels=None):
    for i in range(len(cluster)):
        print "cluster %s: " % i,
        item = cluster[i]
        for it in item:
            print "%s, " % labels[it] if labels else it,
        print "\n",


def scaledown(rows, distance=pearson, rate=0.01, dimension=2):
    n = len(rows)
    if n < 1:
        raise ValueError("no data in samples")
    columns = len(rows[0])
    if columns <= dimension:
        raise ValueError("Cannot scale down %d dimentions to %d dimensions" % (columns, dimension))

    # The real distances between every pair of items
    realdist = [[distance(rows[i], rows[j]) for j in range(n)]
                for i in range(0, n)]

    # Randomly initialize the starting points of the locations in 2D
    # loc = [[random.random(), random.random()] for i in range(n)]
    loc = [[random.random() for x in range(dimension)] for i in range(n)]

    fakedist = [[0.0 for j in range(n)] for i in range(n)]

    lasterror = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                # use Euclidean distance to calculate distances on given dimensions based on loc
                fakedist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2)
                                           for x in range(len(loc[i]))]))

        # Move points
        # grad = [[0.0, 0.0] for i in range(n)]
        grad = [[0.0 for x in range(dimension)] for i in range(n)]

        totalerror = 0
        for k in range(n):
            for j in range(n):
                if j == k: continue
                # The error is percent difference between the distances
                errorterm = (fakedist[j][k] - realdist[j][k]) / realdist[j][k]

                # Each point needs to be moved away from
                # or towards the other point in proportion to how much error it has
                # grad[k][0] += ((loc[k][0] - loc[j][0]) / fakedist[j][k]) * errorterm
                # grad[k][1] += ((loc[k][1] - loc[j][1]) / fakedist[j][k]) * errorterm
                for x in range(len(loc[k])):
                    grad[k][x] += ((loc[k][x] - loc[j][x]) / fakedist[j][k]) * errorterm

                # Keep track of the total error
                totalerror += abs(errorterm)
        print totalerror

        # If the answer got worse by moving the points, we are done
        if lasterror and lasterror < totalerror: break
        lasterror = totalerror

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            # loc[k][0] -= rate * grad[k][0]
            # loc[k][1] -= rate * grad[k][1]
            for x in range(len(loc[k])):
                loc[k][x] -= rate * grad[k][x]

    return loc
