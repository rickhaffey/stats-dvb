import numpy as np
import pandas as pd

def contingencyTable(df, var1, var2):
  # isolate to just our 2 variables for the crosstab
  df = df.loc[:, [var1, var2]]

  # build a crosstab with marginal totals
  ct = pd.crosstab(df[var1], df[var2], margins=True)

  # grab totals for the rows and columns
  rowTotals = ct.loc[:, 'All']
  colTotals = ct.loc['All', :]

  # generate col, row, and overall pcts
  colPcts = ct / colTotals
  rowPcts = (ct.transpose() / rowTotals).transpose()
  grandTotal = ct.loc['All', 'All']
  allPcts = ct / grandTotal

  new_index = [ct.index.values, ['count'] * len(ct.index.values)]
  ct.index = new_index
  ct.index.names = [var1, 'metric']

  new_index = [colPcts.index.values, ['pctOfColumn'] * len(colPcts.index.values)]
  colPcts.index = new_index
  colPcts.index.names = [var1, 'metric']

  new_index = [rowPcts.index.values, ['pctOfRow'] * len(rowPcts.index.values)]
  rowPcts.index = new_index
  rowPcts.index.names = [var1, 'metric']

  new_index = [allPcts.index.values, ['pctOfTotal'] * len(allPcts.index.values)]
  allPcts.index = new_index
  allPcts.index.names = [var1, 'metric']

  metrics = ['count', 'pctOfColumn', 'pctOfRow', 'pctOfTotal']

  var1Vals = np.append(df[var1].unique(), 'All')
  var2Vals = np.append(df[var2].unique(), 'All')

  l = [[x] * 4 for x in var1Vals]
  k = [x for xs in l for x in xs]

  arrays = [k, metrics * len(var1Vals)]

  tuples = list(zip(*arrays))
  index = pd.MultiIndex.from_tuples(tuples, names=[var1, 'metric'])
  df2 = pd.DataFrame(index=index, columns=var2Vals, data=0)

  return df2.add(rowPcts, fill_value=0).add(colPcts, fill_value=0).add(allPcts, fill_value=0).add(ct, fill_value=0)
