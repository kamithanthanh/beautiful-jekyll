# http://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots
# doan cuoi
def partial(hidden, N, qbar) : 
  set_verbose(2)
  F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
  f = x - qbar
  d = f.small_roots(X=2^hidden-1, beta=0.5)[0] # time random
  return qbar - d 

