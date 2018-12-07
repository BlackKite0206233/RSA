import math
import random

def KeyGenerator(bit = 512):
    p = generatePrime(bit)
    q = generatePrime(bit)
    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 0
    d = 0
    while True:
        e = random.randrange(1, math.pow(2, 17))
        if math.gcd(phi_n, e) == 1:
            gcd, x, y = EEA(phi_n, e)
            if gcd == y * phi_n + x * e:
                d = x % phi_n
                break
    return (n, p, q, e, d)
    
def Encryption(n, key, message):
    return SQandMU(message, key, n)

def DecryptionCRT(n, p, q, key, message):
    xp = message % p
    xq = message % q
    dp = key % (p - 1)
    dq = key % (q - 1)
    yp = SQandMU(xp, dp, p)
    yq = SQandMU(xq, dq, q)

    _, x, _ = EEA(p, q)
    cp = x % p
    _, x, _ = EEA(q, p)
    cq = x % q
    
    return (round(q * cp) * yp + round(p * cq) * yq) % n
    
def SQandMU(x, h, n):
    b = bin(h).lstrip('0b')
    r = 1
    for i in b:
        r = r ** 2
        if i == '1':
            r *= x
        r %= n
    return r

def MillerRabinTest(p, k):
    if p == 2:
        return True
    if not(p & 1):
        return False
    
    u = p - 1
    t = 0

    while u & 1 == 0:
        u >>= 1
        t += 1

    def test(a):
        x = SQandMU(a, u, p)
        if x == 1 or x == p - 1:
            return False
        for i in range(t - 1):
            x = SQandMU(a, 2 ** i * u, p)
            if x == p - 1:
                return False
        return True
    while k:
        a = random.randrange(2, p - 2)
        if test(a):
            return False
        k -= 1
        
    return True


def generatePrime(n):
    step = math.floor(math.log2(n) / 2)
    while True:
        x = random.getrandbits(n - 2) << 1
        x += 1 + (1 << 510)
        if MillerRabinTest(x, step):
            return x

def EEA(a, b):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return b, x0, y0