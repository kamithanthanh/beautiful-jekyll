# http://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots
# doan cuoi
length = 512
hidden = 110
length = 512
hidden = 110
p = next_prime(2^int(round(length/2)))
q = next_prime( round(pi.n()*p) )
N = p*q
set_verbose(2)
F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
f = x - qbar
d = f.small_roots(X=2^hidden-1, beta=0.5)[0] # time random
q == qbar - d
