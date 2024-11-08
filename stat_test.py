import pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
import os
import seaborn as sns
import matplotlib.pyplot as plt

model_name_list = ["svmPoly", "C5.0", "nb", "nnet", "pls", "fda", "pcaNNet"]
wd_list = ["all", "no_Dst", "no_TEC", "coord", "xyap", "xzap", "yzap"]
if not os.path.isfile("mcnemar.csv"):
    values_compare = dict()
    for model_name in model_name_list:
        for wd in wd_list:
            values_compare[model_name + "_" + wd] = dict()
            file_open = pd.read_csv(wd + "/" + model_name + ".csv")
            actual = list(file_open["true_classes"])
            preds = list(file_open["model_predictions"])
            values_compare[model_name + "_" + wd][0] = preds
            if "actual" not in values_compare:
                values_compare["actual"] = dict()
                values_compare["actual"][0] = actual
            for class_one in range(1, 6):
                values_compare[model_name + "_" + wd][class_one] = [p == class_one for p in preds]
                values_compare["actual"][class_one] = [p == class_one for p in actual]
    new_data_frame = {"model1": [], "model2": [], "class": [], "test_type": [], "correction": [], "pvalue": [], "statistic": []}
    list_of_keys = list(values_compare.keys())
    for model_ix1 in range(len(list_of_keys)):
        for model_ix2 in range(model_ix1 + 1, len(list_of_keys)):
            m1 = list_of_keys[model_ix1]
            m2 = list_of_keys[model_ix2]
            a1 = values_compare[m1][0]
            a2 = values_compare[m2][0]
            matr = []
            corr_use = False
            for class_one in range(1, 6):
                matr.append([])
                for class_two in range(1, 6):
                    val_add = len([ix for ix in range(len(a1)) if a1[ix] == class_one and a2[ix] == class_two])
                    matr[-1].append(val_add)
                    if val_add <= 4:
                        corr_use = True
            mnc = mcnemar(matr, exact=False, correction=True)
            new_data_frame["model1"].append(m1)
            new_data_frame["model2"].append(m2)
            new_data_frame["class"].append(0)
            new_data_frame["test_type"].append("correction")
            new_data_frame["correction"].append(corr_use)
            new_data_frame["pvalue"].append(mnc.pvalue)
            new_data_frame["statistic"].append(mnc.statistic)
            mn = mcnemar(matr, exact=False, correction=False)
            new_data_frame["model1"].append(m1)
            new_data_frame["model2"].append(m2)
            new_data_frame["class"].append(0)
            new_data_frame["test_type"].append("no")
            new_data_frame["correction"].append(corr_use)
            new_data_frame["pvalue"].append(mn.pvalue)
            new_data_frame["statistic"].append(mn.statistic)
            mnbc = mcnemar(matr, exact=True, correction=True)
            new_data_frame["model1"].append(m1)
            new_data_frame["model2"].append(m2)
            new_data_frame["class"].append(0)
            new_data_frame["test_type"].append("exactcorrection")
            new_data_frame["correction"].append(corr_use)
            new_data_frame["pvalue"].append(mnbc.pvalue)
            new_data_frame["statistic"].append(mnbc.statistic)
            mnb = mcnemar(matr, exact=True, correction=False)
            new_data_frame["model1"].append(m1)
            new_data_frame["model2"].append(m2)
            new_data_frame["class"].append(0)
            new_data_frame["test_type"].append("exact")
            new_data_frame["correction"].append(corr_use)
            new_data_frame["pvalue"].append(mnb.pvalue)
            new_data_frame["statistic"].append(mnb.statistic)
            for class_one in range(1, 6):
                a1 = values_compare[m1][class_one]
                a2 = values_compare[m2][class_one]
                pp = [ix for ix in range(len(a1)) if a1[ix] == 1 and a2[ix] == 1]
                nn = [ix for ix in range(len(a1)) if a1[ix] == 0 and a2[ix] == 0]
                pn = [ix for ix in range(len(a1)) if a1[ix] == 1 and a2[ix] == 0]
                np = [ix for ix in range(len(a1)) if a1[ix] == 0 and a2[ix] == 1]
                matr = [[len(pp), len(pn)], [len(np),  len(nn)]]
                corr_use = len(pp) <= 4 or len(pn) <= 4 or len(np) <= 4 or len(nn) <= 4
                mnc = mcnemar(matr, exact=False, correction=True)
                new_data_frame["model1"].append(m1)
                new_data_frame["model2"].append(m2)
                new_data_frame["class"].append(class_one)
                new_data_frame["test_type"].append("correction")
                new_data_frame["correction"].append(corr_use)
                new_data_frame["pvalue"].append(mnc.pvalue)
                new_data_frame["statistic"].append(mnc.statistic)
                mn = mcnemar(matr, exact=False, correction=False)
                new_data_frame["model1"].append(m1)
                new_data_frame["model2"].append(m2)
                new_data_frame["class"].append(class_one)
                new_data_frame["test_type"].append("no")
                new_data_frame["correction"].append(corr_use)
                new_data_frame["pvalue"].append(mn.pvalue)
                new_data_frame["statistic"].append(mn.statistic)
                mnbc = mcnemar(matr, exact=True, correction=True)
                new_data_frame["model1"].append(m1)
                new_data_frame["model2"].append(m2)
                new_data_frame["class"].append(class_one)
                new_data_frame["test_type"].append("exactcorrection")
                new_data_frame["correction"].append(corr_use)
                new_data_frame["pvalue"].append(mnbc.pvalue)
                new_data_frame["statistic"].append(mnbc.statistic)
                mnb = mcnemar(matr, exact=True, correction=False)
                new_data_frame["model1"].append(m1)
                new_data_frame["model2"].append(m2)
                new_data_frame["class"].append(class_one)
                new_data_frame["test_type"].append("exact")
                new_data_frame["correction"].append(corr_use)
                new_data_frame["pvalue"].append(mnb.pvalue)
                new_data_frame["statistic"].append(mnb.statistic)
    dfnew = pd.DataFrame(new_data_frame)
    dfnew.to_csv("mcnemar.csv", index = False)
else:
    dfnew = pd.read_csv("mcnemar.csv", index_col = False)
ix_dfnew = []
ix_dfnew_unfiltered = []
dicti_model = {m: [] for m in model_name_list}
dict_wd = {wd: [] for wd in wd_list}
dict_class = {c: [] for c in range(0, 6)}
pvcls = dict()
allpv = dict()
allpvno = dict()
allpok = dict()
allpsignificant = dict()
for ix in range(len(dfnew["model1"])):
    m1 = dfnew["model1"][ix]
    m2 = dfnew["model2"][ix]
    cls = dfnew["class"][ix]
    t = dfnew["test_type"][ix]
    c = dfnew["correction"][ix]
    p = dfnew["pvalue"][ix]
    if m1 not in allpv:
        allpv[m1] = dict()
    if m2 not in allpv[m1]:
        allpv[m1][m2] = set()
    allpv[m1][m2].add((cls, t, c, p))
    if m2 not in allpv:
        allpv[m2] = dict()
    if m1 not in allpv[m2]:
        allpv[m2][m1] = set()
    allpv[m2][m1].add((cls, t, c, p))
    if "all" in m1:
        continue
    if "all" in m2:
        continue
    if m1 not in allpvno:
        allpvno[m1] = dict()
    if m2 not in allpvno[m1]:
        allpvno[m1][m2] = set()
    allpvno[m1][m2].add((cls, t, c, p))
    if m2 not in allpvno:
        allpvno[m2] = dict()
    if m1 not in allpvno[m2]:
        allpvno[m2][m1] = set()
    allpvno[m2][m1].add((cls, t, c, p))
    if cls != 0:
        continue
    if "exact" in t:
        continue
    if "correction" in t and not c:
        continue
    if "correction" not in t and c:
        continue
    if m1 not in allpok:
        allpok[m1] = dict()
    if m2 not in allpok[m1]:
        allpok[m1][m2] = set()
    allpok[m1][m2].add((cls, t, c, p))
    if m2 not in allpok:
        allpok[m2] = dict()
    if m1 not in allpok[m2]:
        allpok[m2][m1] = set()
    allpok[m2][m1].add((cls, t, c, p))
    ix_dfnew_unfiltered.append(ix)
    if p < 0.05 / (21 * 43):
        continue
    if m1 not in allpsignificant:
        allpsignificant[m1] = dict()
    if m2 not in allpsignificant[m1]:
        allpsignificant[m1][m2] = set()
    allpsignificant[m1][m2].add((cls, t, c, p))
    if m2 not in allpsignificant:
        allpsignificant[m2] = dict()
    if m1 not in allpsignificant[m2]:
        allpsignificant[m2][m1] = set()
    allpsignificant[m2][m1].add((cls, t, c, p))
    ix_dfnew.append(ix)
    if m1 not in pvcls:
        pvcls[m1] = dict()
    if m2 not in pvcls[m1]:
        pvcls[m1][m2] = []
    pvcls[m1][m2].append((cls, t, c, p))
    dict_class[cls].append(ix)
    for m in model_name_list:
        if m in m1 and m in m2:
            dicti_model[m].append(ix)
    for wd in wd_list:
        if wd in m1 and wd in m2:
            dict_wd[wd].append(ix)
    s = dfnew["statistic"][ix]
print(len(ix_dfnew))
print(len(ix_dfnew_unfiltered))
for m in model_name_list:
    if m != "nb":
        continue
    pvs = set()
    for ix in dicti_model[m]:
        m1 = dfnew["model1"][ix]
        m2 = dfnew["model2"][ix]
        cls = dfnew["class"][ix]
        #print(m1, m2, cls)
        pvs.add((m1, m2))
    for p in pvs:
        print(p[0], p[1], pvcls[p[0]][p[1]])
for wd in wd_list:
    if wd != "no_Dst":
        continue
    pvs = set()
    for ix in dict_wd[wd]:
        m1 = dfnew["model1"][ix]
        m2 = dfnew["model2"][ix]
        cls = dfnew["class"][ix]
        #print(m1, m2, cls)
        pvs.add((m1, m2))
    for p in pvs:
        print(p[0], p[1], pvcls[p[0]][p[1]])
    
for wd in wd_list:
    if "all" in wd:
        continue

    df_new_unfiltered = {"best": []}
    for t in set(dfnew["test_type"]):
        df_new_unfiltered[t] = []

    tick_labels = []
    for m1 in allpvno:
        if wd not in m1:
            continue
        tick_labels.append(m1.split("_")[0])
        for t in set(df_new_unfiltered):
            df_new_unfiltered[t].append([])
        for m2 in allpvno:
            if wd not in m2:
                continue
            if m1 != m2:
                for val in allpvno[m1][m2]:
                    cls, t, c, p = val
                    if cls:
                        continue
                    if val in allpok[m1][m2]:
                        df_new_unfiltered["best"][-1].append(p)
                    df_new_unfiltered[t][-1].append(p)
            else:
                for t in df_new_unfiltered:
                    df_new_unfiltered[t][-1].append(1.0)
    
    for t in df_new_unfiltered:
        print(len(df_new_unfiltered[t]), len(df_new_unfiltered[t][0]))
    plt.title(wd)        
    sns.heatmap(df_new_unfiltered["best"], annot = True)
    plt.xticks([i + 0.5 for i in range(len(tick_labels))], tick_labels)
    plt.yticks([i + 0.5 for i in range(len(tick_labels))], tick_labels)
    plt.show()

for m in model_name_list:
    df_new_unfiltered = {"best": []}
    for t in set(dfnew["test_type"]):
        df_new_unfiltered[t] = []
        
    tick_labels = []
    for m1 in allpvno:
        if m not in m1:
            continue
        tick_labels.append(m1.replace(m1.split("_")[0] + "_", ""))
        for t in set(df_new_unfiltered):
            df_new_unfiltered[t].append([])
        for m2 in allpvno:
            if m not in m2:
                continue
            if m1 != m2:
                for val in allpvno[m1][m2]:
                    cls, t, c, p = val
                    if cls:
                        continue
                    if val in allpok[m1][m2]:
                        df_new_unfiltered["best"][-1].append(p)
                    df_new_unfiltered[t][-1].append(p)
            else:
                for t in df_new_unfiltered:
                    df_new_unfiltered[t][-1].append(1.0)
    
    for t in df_new_unfiltered:
        print(len(df_new_unfiltered[t]), len(df_new_unfiltered[t][0]))
    plt.title(m)        
    sns.heatmap(df_new_unfiltered["best"], annot = True)
    plt.xticks([i + 0.5 for i in range(len(tick_labels))], tick_labels)
    plt.yticks([i + 0.5 for i in range(len(tick_labels))], tick_labels)
    plt.show()