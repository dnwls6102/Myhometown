import random

country = {'한국':100,'미국':1000,'중국':900,'일본':150}
x = []

def pickone():
    return random.sample(list(country.keys()),2)

