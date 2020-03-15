def modular_sqrt_composite(c, p, q):
    """
    Calculates modular square root of composite value for given 2 factors
    For a = b^2 mod p*q calculates b
    :param a: residue
    :param p: modulus prime factor
    :param q: modulus prime factor
    :return: 4 potential root values
    """
    n = p * q
    gcd_value, yp, yq = extended_gcd(p, q)
    mp = modular_sqrt(c, p)
    mq = modular_sqrt(c, q)
    assert yp * p + yq * q == 1
    assert (mp * mp) % p == c % p
    assert (mq * mq) % q == c % q
    r1 = (yp * p * mq + yq * q * mp) % n
    s1 = (yp * p * mq - yq * q * mp) % n
    r2 = n - r1
    s2 = n - s1
    return r1, s1, r2, s2


def modular_sqrt(a, p):
    """
    Calculates modular square root with prime modulus.
    For a = b^2 mod p calculates b
    :param a: residue
    :param p: modulus
    :return: root value
    """
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while True:
        t = b
        m = 0
        for m in xrange(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

 def legendre_symbol(a, p):
    """ Compute the Legendre symbol a|p using
        Euler's criterion. p is a prime, a is
        relatively prime to p (if p divides
        a, then a|p = 0)
        Returns 1 if a has a square root modulo
        p, -1 otherwise.
    """
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls
