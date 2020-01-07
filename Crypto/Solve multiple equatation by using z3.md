# Solve multiple equatation by using z3

s = Solver()
    
    input = [BitVec("input%s" % i, 8) for i in range(10)]
    
    for i in range(10):
      s.add(input[i] >= 0x20)
      s.add(input[i] <= 0x7E)
    if s.check() == sat : 
    	s.model()

![Solve%20multiple%20equatation%20by%20using%20z3/Untitled.png](Solve%20multiple%20equatation%20by%20using%20z3/Untitled.png)