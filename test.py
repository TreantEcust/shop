import numpy as np
import pandas as pd

a={'a':9,'b':7,'c':8}
b=pd.DataFrame([list(a.keys()),list(a.values())])
b=b.transpose()
x=1