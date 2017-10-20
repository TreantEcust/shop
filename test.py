import numpy as np

a={'a':9,'b':7,'c':8}
a=sorted(a.items(),key=lambda x:x[1],reverse=True)
print(a)