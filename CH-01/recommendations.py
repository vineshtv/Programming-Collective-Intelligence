from math import sqrt

#A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0
    },
    'Michael Phillips': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 4.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'You, Me and Dupree': 2.0,
        'The Night Listener': 3.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 1.0
    }
}

#returns a distance-based similarity score for person 1 and person2
def sim_distance(prefs, person1, person2):
    #Get the list of shared_items
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    #if they have no ratings in common return 0
    if len(si) == 0:
        return 0


    # add up the squares of all the differences
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                            for item in prefs[person1] if item in prefs[person2]])

    return 1/(1 + sqrt(sum_of_squares))


#returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, person1, person2):
    #Get the list of mutually rated items
    si = {}

    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    #find the number if matching items
    n = len(si)

    #if they have no ratings in common return 0
    if n == 0:
        return 0

    #Add up all the preferences
    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])

    #Sum up the squares
    sum1Sq = sum([pow(prefs[person1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[person2][it],2) for it in si])

    #sum up the products
    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    #Calulate the Pearson score
    num = pSum - (sum1 * sum2 /n)
    den = sqrt((sum1Sq - pow(sum1, 2)/n) * (sum2Sq - pow(sum2, 2)/n))

    if den == 0:
        return 0

    r = num/den

    return r

#Returns the best matches for person from prefs dictionary
# number of results and similarity function are optional params.
def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other) 
                        for other in prefs if other != person]

    #sort the list so the highest score appears at the top
    scores.sort()
    scores.reverse()
    return scores[0:n]



if __name__ == "__main__":
    distance = sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
    print "Euclidean distance score between Lisa Rose and Gene Seymour = ", distance

    pearsonScore = sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
    print "Pearson score for Lisa Rose and Gene Seymour = ", pearsonScore

    Knearest = topMatches(critics, 'Toby', n = 3)
    print "nearest matches for Toby = ", Knearest
