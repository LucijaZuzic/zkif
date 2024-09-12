import pandas as pd
import numpy as np

model_name_list = ["svmPoly", "C5.0", "nb", "nnet", "pls", "fda", "pcaNNet"]
metric_alias = {
    "Sensitivity": "Sen",
    "Specificity": "Spec",
    "Pos Pred Value": "PPV",
    "Neg Pred Value": "NPV",
    "Prevalence": "P",
    "Detection Rate": "DR",
    "Detection Prevalence": "DP",
    "Balanced Accuracy": "BA"
}
metric_alias_second = {
    "Accuracy": "Acc",
    "95% CI": "$95\%$ CI",
    "No Information Rate": "NIR",
    "P-Value [Acc > NIR]": "P-Value",
    "Kappa": "Kappa",
    "Mcnemar's Test P-Value": "McNemar"
}
wd = ""
dict_co_total = dict()
for model_name in model_name_list:
    dict_co_total[model_name] = dict()
    file_open = open(wd + model_name + ".txt")
    all_lines = file_open.readlines()
    line_ref = 0
    while line_ref < len(all_lines) and "Reference" not in all_lines[line_ref]:
        line_ref += 1
    if line_ref != len(all_lines):
        print(model_name)
        line_sen = line_ref
        while line_sen < len(all_lines) and "Sensitivity" not in all_lines[line_sen]:
            line_sen += 1
        line_over = line_ref
        while line_over < len(all_lines) and "Overall" not in all_lines[line_over]:
            line_over += 1
        co = all_lines[line_over + 2:line_over + 10]
        co = [x.strip().split(" : ") for x in co]
        dict_co = dict()
        for line_ix in range(len(co)):
            if len(co[line_ix]) > 1:
                #print(co[line_ix])
                dict_co[co[line_ix][0]] = co[line_ix][1]
        #print(dict_co)
        for val in dict_co:
            #print(val, dict_co[val])
            dict_co_total[model_name][val] = dict_co[val]
        cm = all_lines[line_ref + 1:line_ref + 7]
        for line_ix in range(len(cm)):
            while "  " in cm[line_ix]:
                cm[line_ix] = cm[line_ix].replace("  ", " ")
            cm[line_ix] = cm[line_ix].strip().split(" ")
            for val_ix in range(len(cm[line_ix])):
                if str(cm[line_ix][val_ix]).isdigit():
                    cm[line_ix][val_ix] = int(cm[line_ix][val_ix])
            #print(cm[line_ix])
        dict_cm = dict()
        for col_ix in range(len(cm[0])):
            colname = cm[0][col_ix]
            dict_cm[colname] = []
            for row_ix in range(1, len(cm[0])):
                dict_cm[colname].append(cm[row_ix][col_ix])
        line_one = "\\cline{3-7}\n\\multicolumn{2}{c|}{} & \\multicolumn{5}{|c|}{Reference} \\\\ \\cline{3-7}\n"
        for row_ix in range(len(cm)):
            line_one += " & "
            flag_end = False
            for col_ix in range(len(cm[row_ix])):
                if str(cm[row_ix][col_ix]).isdigit():
                    line_one += "$" + str(cm[row_ix][col_ix]) + "$ & "
                else:
                    line_one += str(cm[row_ix][col_ix]) + " & "
                if "T" in str(cm[row_ix][col_ix]):
                    flag_end = True
            line_one = line_one[:-2]
            if flag_end:
                line_one += "\\\\ \\hline\n"
            else:
                line_one += "\\\\ \\cline{2-7}\n"
        line_one = line_one.replace(" & Prediction ", "\\multicolumn{2}{c|}{} ")
        line_one = line_one.replace(" & E", "\\multirow{5}{*}{\\rotatebox{90}{Prediction}} & E")
        line_one = line_one.replace("}\\multirow{5}{*}{\\rotatebox{90}{Prediction}} & E", "} & E")
        print(line_one)
        #print(dict_cm)
        df_cm = pd.DataFrame(dict_cm)
        df_cm.to_csv(wd + model_name + "_cm.csv", index = False)
        cs = all_lines[line_sen - 1:line_sen + 8]
        for line_ix in range(len(cs)):
            while "  " in cs[line_ix]:
                cs[line_ix] = cs[line_ix].replace("  ", " ")
            cs[line_ix] = cs[line_ix].replace("Class: ", "")
            cs[line_ix] = cs[line_ix].replace("NaN", "100000")
            if line_ix > 0:
                uppers = []
                for val_ix in range(len(cs[line_ix])):
                    if str(cs[line_ix][val_ix]).isupper():
                        uppers.append(cs[line_ix][val_ix])
                for upper in uppers:
                    cs[line_ix] = cs[line_ix].replace(" " + upper, "_" + upper)
            cs[line_ix] = cs[line_ix].strip().split(" ")
            if line_ix == 0:
                cs[line_ix].insert(0, "Statistics")
            for val_ix in range(len(cs[line_ix])):
                if str(cs[line_ix][val_ix]).isdigit():
                    cs[line_ix][val_ix] = int(cs[line_ix][val_ix])
                else:
                    cs[line_ix][val_ix] = cs[line_ix][val_ix].replace("_", " ")
            #print(cs[line_ix])
        dict_cs = dict()
        for col_ix in range(len(cs[0])):
            colname = cs[0][col_ix]
            dict_cs[colname] = []
            for row_ix in range(1, len(all_lines[line_sen:line_sen + 9])):
                val_use = cs[row_ix][col_ix]
                if str(val_use).isdigit() and val_use > 100:
                    dict_cs[colname].append("NaN")
                else:
                    dict_cs[colname].append(cs[row_ix][col_ix])
        line_one = "\\cline{3-10}\n\\multicolumn{2}{c|}{} & \\multicolumn{8}{c|}{Statistics} \\\\ \\cline{3-10}\n"
        for colname in dict_cs:
            if "E" not in colname and "Statistics" not in colname:
                line_one += " & "
            line_one += colname.replace("Statistics", "\\multicolumn{2}{c|}{}").replace("E", "\\multirow{5}{*}{\\rotatebox{90}{Class}} & E") + " & "
            for col_ix in range(len(dict_cs[colname])):
                if str(dict_cs[colname][col_ix]).isdigit() or "." in str(dict_cs[colname][col_ix]):
                    if float(dict_cs[colname][col_ix]) > 100:
                        line_one += "NaN & "
                    else:
                        line_one += "$" + str(np.round(float(dict_cs[colname][col_ix]) * 100, 4)) + "\%$ & "
                else:
                    if str(dict_cs[colname][col_ix]) in metric_alias:
                        line_one += metric_alias[str(dict_cs[colname][col_ix])] + " & "
                    else:
                        line_one += str(dict_cs[colname][col_ix]) + " & "
            line_one = line_one[:-2]
            if "Statistics" in colname or "T" in colname:
                line_one += "\\\\ \\hline\n"
            else:
                line_one += "\\\\ \\cline{2-10}\n"
        print(line_one.replace(".0\%", "\%"))
        line_one = "\\cline{3-7}\n\\multicolumn{2}{c|}{} & \\multicolumn{5}{c|}{Class} \\\\ \\cline{3-7}\n"
        for row_ix in range(len(cs)):
            for col_ix in range(len(cs[row_ix])):
                if str(cs[row_ix][col_ix]).isdigit() or "." in str(cs[row_ix][col_ix]):
                    if float(cs[row_ix][col_ix]) > 100:
                        line_one += "NaN & "
                    else:
                        line_one += "$" + str(np.round(float(cs[row_ix][col_ix]) * 100, 4)) + "\%$ & "
                else:
                    if str(cs[row_ix][col_ix]) in metric_alias:
                        if "Sensitivity" not in str(cs[row_ix][col_ix]):
                            line_one += " & " + metric_alias[str(cs[row_ix][col_ix])] + " & "
                        else:
                            line_one += "\\multirow{8}{*}{\\rotatebox{90}{Statistics}} & " + metric_alias[str(cs[row_ix][col_ix])] + " & "
                    else:
                        line_one += str(cs[row_ix][col_ix]).replace("Statistics", "\\multicolumn{2}{c|}{}") + " & "
            line_one = line_one[:-2]
            if row_ix == 0 or row_ix == len(cs) - 1:
                line_one += "\\\\ \\hline\n"
            else:
                line_one += "\\\\ \\cline{2-7}\n"
        print(line_one.replace(".0\%", "\%"))
        #print(dict_cs)
        df_cs = pd.DataFrame(dict_cs)
        df_cs.to_csv(wd + model_name + "_cs.csv", index = False)
#print(dict_co_total)
models_list = list(dict_co_total.keys())
metrics_list = list(dict_co_total[models_list[0]].keys())
new_dict_co = {"Metric": metrics_list}
for model_name in models_list:
    new_dict_co[model_name] = []
    for metric in metrics_list:
        new_dict_co[model_name].append(dict_co_total[model_name][metric])
#print(new_dict_co)
line_print = "\\hline\n"
for colname in new_dict_co.keys():
    line_print += colname + " & "
line_print = line_print[:-2] + "\\\\ \\hline\n"
for metric in metrics_list:
    line_print += metric_alias_second[metric] + " & "
    for model_name in models_list:
        if "NA" not in dict_co_total[model_name][metric]:
            line_print += "$" + dict_co_total[model_name][metric] + "$ & "
        else:
            line_print += "NA & "
    line_print = line_print[:-2] + "\\\\ \\hline\n"
print(line_print)
line_print = "\\hline\nModel & "
for metric in metrics_list:
    line_print += metric_alias_second[metric] + " & "
line_print = line_print[:-2] + "\\\\ \\hline\n"
for model_name in models_list:
    line_print += model_name + " & "
    for metric in metrics_list:
        if "NA" not in dict_co_total[model_name][metric]:
            line_print += "$" + dict_co_total[model_name][metric] + "$ & "
        else:
            line_print += "NA & "
    line_print = line_print[:-2] + "\\\\ \\hline\n"
print(line_print)
df_new_dict_co = pd.DataFrame(new_dict_co)
df_new_dict_co.to_csv(wd + "stats.csv", index = False)