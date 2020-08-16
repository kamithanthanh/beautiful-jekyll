# http://doc.sagemath.org/html/en/reference/polynomial_rings/sage/rings/polynomial/polynomial_modn_dense_ntl.html#sage.rings.polynomial.polynomial_modn_dense_ntl.small_roots
# doan cuoi
def partial(hidden, N, qbar) : 
  set_verbose(2)
  F.<x> = PolynomialRing(Zmod(N), implementation='NTL')
  f = x - qbar
  d = f.small_roots(X=2^hidden-1, beta=0.5)[0] # time random
  return qbar - d 

def partialP(pbar, N, hidden_bits) : 
    X = 2^hidden_bits
    M = matrix([[X^2, X*pbar, 0], [0, X, pbar], [0, 0, N]])
    B = M.LLL()
    Q = B[0][0]*x^2/X^2+B[0][1]*x/X+B[0][2]
    return pbar +Q.roots(ring=ZZ)[0][0] 
