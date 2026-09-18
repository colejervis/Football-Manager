import math
import random

def bell_curve(mean, standard_deviation):

    """
    https://en.wikipedia.org/wiki/Box–Muller_transform

    Uses the box-muller equation to model a bell curve - bell curves are useful as they describe how random, independent variables average
    into a predictable shape - such as player ability generation or player potentials

    Standard computer random number generators are uniform (e.g numbers have the same chance of appearing). A normal / Gaussian distribution
    is used to model how average scores appear frequently and extreme scores are less likely.
    """

    n1 = random.random()
    n2 = random.random()
    while n1 == 0:
        n1 = random.randint(0, 1)

    return mean + standard_deviation * (math.sqrt(-2 * math.log(n1)) * math.cos(2 * math.pi * n2))


def poisson_distribution(base_events):

    """
    https://www.johndcook.com/blog/2010/06/14/generating-poisson-random-values/

    Used for counts of rare, independent events, e.g. chances / fouls / shots in a football match, from a baseline number - uses Knuth's Algorithm
    """

    l = math.exp(-base_events)
    k = 0
    p = 1

    while p > l:
        k = k + 1
        u = random.random()
        p *= u

    return k-1


def softmax(weights, temperature):
    """
    Takes a list of raw, ungrounded numbers (logits), and converts them into a probability distribution where each value is between 0 and 1.
    It exponentiates each number (subtracting the max weight to keep the numbers manageable but probabilities the same), dividing each one by temperature,
    allowing the user to control the gaps / steepness between each value. These are converted in 0-1 probabilities by normalizing them.

    Useful for controlling probabilities in systems such as the media prediction, youth intake nationalities, AI team selection, using the temp.
    """

    max_weight = max(weights)

    new_weights = []
    for weight in weights:
        new_weights.append(math.exp((weight - max_weight) / temperature))

    sum_exp = sum(new_weights)

    probabilities = []
    for weight in new_weights:
        probabilities.append(weight/sum_exp)

    return probabilities

def sigmoid(input, scale):
    """
    https://en.wikipedia.org/wiki/Sigmoid_function

    A mathematical curve shaped like the letter 'S' that can convert any real-valued number into a decimal between 0 and 1. Can be used to generate probabilities
    for goals, penalty goals, etc
    """

    return 1 / (1 + math.exp((-input / scale)))

def rounddp(number, dp):
    """
    https://en.wikipedia.org/wiki/Rounding

    Both techniques use a technique known as 'round half away from zero'
    """

    if number == 0:
        return 0

    x = number
    n = dp

    return sgn(x) * (math.floor(abs(x)*10**n + 0.5)) / 10**n

def roundsf(number, sf):

    if number == 0:
        return 0

    m = math.floor(math.log10(abs(number)))
    x = number
    n = sf

    return sgn(x) * (math.floor(abs(x)*10**(n-1-m) + 0.5)) / 10**(n-1-m)

def sgn(number):
    """
    Helper function for rounding
    """

    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0


def random_choices(list, indexOfWeight = 1):

    total = 0
    for item in list:
        total += item[indexOfWeight]

    number = random.uniform(0, total)
    cumulative = 0
    for item in list:

        weight = item[indexOfWeight]

        cumulative += weight
        if number <= cumulative:
            selectedItem = item
            break

    return selectedItem