import requests
def factor(n) : 
  rd = requests.get("http://factordb.com/api", params={"query": str(n)}).json() 
  return rd['factors'] 
# {u'status': u'C', u'id': u'1100000001115460681', u'factors': [[u'72532046707394527184361122364055313434377630022988043070962959961740902025113107530697959132646327596976526693065378307', 1]]}
