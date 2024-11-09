from statsmodels.stats.contingency_tables import mcnemar

v11 = [2704, 4397, 4431, 6115, 6017, 5360]
v00 = [18384, 20077, 13223, 11659, 5569, 10960]
v10 = [5136, 3443, 10297, 11861, 17951, 12560]
v01 = [5136, 3443, 3409, 1725, 1823, 2480]

for ix in range(len(v11)):
    matr = [[v11[ix], v10[ix]], [v01[ix], v00[ix]]]
    for isexact in [True, False]:
        for iscorr in [True, False]:
            print(ix, isexact, iscorr, mcnemar(matr, exact=isexact, correction=iscorr).pvalue)