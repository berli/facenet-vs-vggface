#!/usr/bin/python 
# -*- coding: utf-8 -*-)

import pandas as pd
df = pd.DataFrame(  [   [  ['1','2','3'] , '2' ] ,  [['4','5','6'] , '3' ] ]  ) 
cat_df = df.apply(lambda s:[x + '_' + s[1] for x in s[0]], axis = 1)
print cat_df

