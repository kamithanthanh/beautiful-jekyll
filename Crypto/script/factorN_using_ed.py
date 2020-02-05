def find_prime_factors(n,e,d):
    k = e * d - 1
    s = 0 
    t = k

    while t % 2 == 0:
        t = t // 2
        s += 1

    i = s
    a = 2

    while True:
        b = pow(a,t,n)

        if b == 1:
            a = nextprime(a)
            continue

        while i != 1:
            c = pow(b,2,n)
            if c == 1:
                break
            else:
                b = c
                i -= 1

        if b == n - 1:
            a = nextprime(a)
            continue

        p = math.gcd(b-1, n)
        q = n // p
        return p, q
