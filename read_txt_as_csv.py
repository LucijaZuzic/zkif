import pandas as pd
import numpy as np
import os

mod_val = 8
keywords_time = ["Train", "Predict", "Importance", "Total"]
translate_time = {"Train": "train",
                   "Predict": "prediction",
                   "Importance": "variable importance calculation",
                   "Total": "execution"
                   }
position_start = "!ht"
model_name_list = ["svmPoly", "C5.0", "nb", "nnet", "pls", "fda", "pcaNNet"]
model_print_list = ["svmPoly", "C5.0", "nb", "nnet", "pls", "fda", "pcaNNet"]
translate_model = {"svmPoly": "polynomial SVM",
                   "C5.0": "decision tree",
                   "nb": "naive Bayes",
                   "nnet": "neural network",
                   "pls": "PLS",
                   "fda": "FDA",
                   "pcaNNet": "PCA neural network"
                   }
by_pred = True
by_class = True
by_statistics = True
use_alias = True
by_time_type = True
by_time_model = True
by_time_type_ansamble = True
by_time_model_ansamble = True
skip_time = ["user", "system"]
skip_time_tmp = ["user", "system"]
for skip_time_first in skip_time_tmp:
    for key_time in keywords_time:
        skip_time.append(skip_time_first + "_" + key_time.lower())
by_model = True
by_metric = True
use_alias_second = True
by_ansamble = True
skip_first = ["Prevalence"]
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
skip_second = ["Mcnemar's Test P-Value"]
metric_alias_second = {
    "Accuracy": "Acc",
    "95% CI": "$95\%$ CI",
    "No Information Rate": "NIR",
    "P-Value [Acc > NIR]": "$p$-value",
    "Kappa": "Kappa",
    "Mcnemar's Test P-Value": "McNemar"
    }
metric_alias_fix = {
    "Accuracy": "Accuracy",
    "95% CI": "$95\%$ CI",
    "No Information Rate": "No Information Rate",
    "P-Value [Acc > NIR]": "$p$-value $[$Acc $>$ NIR$]$",
    "Kappa": "Kappa",
    "Mcnemar's Test P-Value": "McNemar's test $p$-value"
    }
wd_list = ["all", "no_Dst", "no_TEC", "coord", "xyap", "xzap", "yzap"]
translate_data = {"all": "all variables",
                   "no_Dst": "all variables except Dst",
                   "no_TEC": "all variables except Dst, TEC, and dTEC",
                   "coord": "only $B_{x}$, $B_{y}$, and $B_{z}$",
                   "xyap": "only $B_{x}$, $B_{y}$, and $a_{p}$",
                   "xzap": "only $B_{x}$, $B_{z}$, and $a_{p}$",
                   "yzap": "only $B_{y}$, $B_{z}$, and $a_{p}$"
                   }
ansamble_list = [4, 7]
ansamble_print = [4, 7]
all_model_total_dict = dict()
reference_total_dict = dict()
stats_total_dict = dict()
stats_reverse_total_dict = dict()
all_model_dict = dict()
reference_dict = dict()
stats_dict = dict()
stats_reverse_dict = dict()
all_str_dict = dict()
for model_name in model_name_list:
    all_model_dict[model_name] = dict()
    reference_dict[model_name] = dict()
    stats_dict[model_name] = dict()
    stats_reverse_dict[model_name] = dict()
for x1 in [True, False]:
    all_model_total_dict[x1] = dict()
    reference_total_dict[x1] = dict()
    stats_total_dict[x1] = dict()
    stats_reverse_total_dict[x1] = dict()
    all_model_dict[x1] = dict()
    reference_dict[x1] = dict()
    stats_dict[x1] = dict()
    stats_reverse_dict[x1] = dict()
    all_str_dict[x1] = dict()
    for model_name in model_name_list:
        all_model_dict[model_name][x1] = dict()
        reference_dict[model_name][x1] = dict()
        stats_dict[model_name][x1] = dict()
        stats_reverse_dict[model_name][x1] = dict()
    for x2 in [True, False]:
        all_model_total_dict[x1][x2] = dict()
        reference_total_dict[x1][x2] = dict()
        stats_total_dict[x1][x2] = dict()
        stats_reverse_total_dict[x1][x2] = dict()
        all_model_dict[x1][x2] = dict()
        reference_dict[x1][x2] = dict()
        stats_dict[x1][x2] = dict()
        stats_reverse_dict[x1][x2] = dict()
        all_str_dict[x1][x2] = dict()
        for model_name in model_name_list:
            all_model_dict[model_name][x1][x2] = dict()
            reference_dict[model_name][x1][x2] = dict()
            stats_dict[model_name][x1][x2] = dict()
            stats_reverse_dict[model_name][x1][x2] = dict()
        for x3 in [True, False]:
            if ((x1 or x2) or x3) == False:
                continue
            all_model_total_dict[x1][x2][x3] = ""
            reference_total_dict[x1][x2][x3] = ""
            stats_total_dict[x1][x2][x3] = ""
            stats_reverse_total_dict[x1][x2][x3] = ""
            all_model_dict[x1][x2][x3] = dict()
            reference_dict[x1][x2][x3] = dict()
            stats_dict[x1][x2][x3] = dict()
            stats_reverse_dict[x1][x2][x3] = dict()
            all_str_dict[x1][x2][x3] = ""
            for model_name in model_name_list:
                all_model_dict[model_name][x1][x2][x3] = ""
                reference_dict[model_name][x1][x2][x3] = ""
                stats_dict[model_name][x1][x2][x3] = ""
                stats_reverse_dict[model_name][x1][x2][x3] = ""
time_dict = dict()
time_total_dict = ""
time_reverse_dict = dict()
time_reverse_total_dict = ""
all_stats_dict = ""
all_stats_reverse_dict = ""
ansamble_dict_total = ""
ansamble_dict = dict()
time_ansamble_dict = dict()
time_ansamble_total_dict = ""
time_ansamble_reverse_dict = dict()
time_ansamble_reverse_total_dict = ""
for an in ansamble_list:
    ansamble_dict[an] = ""
    time_ansamble_dict[an] = ""
    time_ansamble_reverse_dict[an] = ""
for kt in keywords_time:
    time_dict[kt] = ""
    time_reverse_dict[kt] = ""
for wd in wd_list:
    all_str = dict()
    reference_str = dict()
    stats_str= dict()
    stats_str_reverse = dict()
    for x1 in [True, False]:
        all_str[x1] = dict()
        reference_str[x1] = dict()
        stats_str[x1] = dict()
        stats_str_reverse[x1] = dict()
        for x2 in [True, False]:
            all_str[x1][x2] = dict()
            reference_str[x1][x2] = dict()
            stats_str[x1][x2] = dict()
            stats_str_reverse[x1][x2] = dict()
            for x3 in [True, False]:
                if ((x1 or x2) or x3) == False:
                    continue
                all_str[x1][x2][x3] = ""
                reference_str[x1][x2][x3] = ""
                stats_str[x1][x2][x3] = ""
                stats_str_reverse[x1][x2][x3] = ""
    dict_co_total = dict()
    dict_time_total_total = {"Model": []}
    dict_time_total = dict()
    for time_name in keywords_time:
        dict_time_total[time_name] = {"Model": []}
    for model_name in model_name_list:
        all_model = dict()
        for x1 in [True, False]:
            all_model[x1] = dict()
            for x2 in [True, False]:
                all_model[x1][x2] = dict()
                for x3 in [True, False]:
                    if ((x1 or x2) or x3) == False:
                        continue
                    all_model[x1][x2][x3] = ""
        dict_co_total[model_name] = dict()
        file_open = open(wd + "/" + model_name + ".txt")
        all_lines = file_open.readlines()
        file_open.close()
        line_ref = 0
        while line_ref < len(all_lines) and "Reference" not in all_lines[line_ref]:
            line_ref += 1
        if line_ref != len(all_lines):
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
            line_one = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c|c|c|c|c|c|}\n\t\t\\hline\n\t\t & \\multicolumn{5}{|c|}{Reference} \\\\ \\hline\n"
            for row_ix in range(len(cm)):
                line_one += "\t\t "
                for col_ix in range(len(cm[row_ix])):
                    if str(cm[row_ix][col_ix]).isdigit():
                        line_one += "$" + str(cm[row_ix][col_ix]) + "$ & "
                    else:
                        line_one += str(cm[row_ix][col_ix]) + " & "
                line_one = line_one[:-2]
                line_one += "\\\\ \\hline\n"
            caption_txt = "The confusion matrix for the " + translate_model[model_name] + " model when using " + translate_data[wd] + " as input."
            label_txt = "tab:cm:" + wd.replace("_", "") + ":" +  model_name
            line_one += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
            if model_name in model_print_list and by_pred:
                #print(line_one)
                if not os.path.isdir(wd + "/latex_table/" + model_name):
                    os.makedirs(wd + "/latex_table/" + model_name)
                file_label = open(wd + "/latex_table/" + model_name + "/cm_" + model_name + ".tex", "w")
                file_label.write(line_one)
                file_label.close()
                x1 = True
                for x2 in [True, False]:
                    for x3 in [True, False]:
                        all_model[x1][x2][x3] += line_one + "\n"
                        reference_str[x1][x2][x3] += line_one + "\n"
                        all_str[x1][x2][x3] += line_one + "\n"
                        all_model_total_dict[x1][x2][x3] += line_one + "\n"
                        reference_total_dict[x1][x2][x3] += line_one + "\n"
                        all_model_dict[model_name][x1][x2][x3] += line_one + "\n"
                        reference_dict[model_name][x1][x2][x3] += line_one + "\n"
                        all_str_dict[x1][x2][x3] += line_one + "\n"
            #print(dict_cm)
            df_cm = pd.DataFrame(dict_cm)
            df_cm.to_csv(wd + "/" + model_name + "_cm.csv", index = False)
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
            line_one = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{"
            for i in range(len(metric_alias) - len(skip_first) + 2):
                line_one += "|c"
            line_one += "|}"
            line_one += "\n\t\t\\hline\n\t\t & \\multicolumn{" + str(len(metric_alias) - len(skip_first)) + "}{c|}{Statistics} \\\\ \\hline\n"
            for colname in dict_cs:
                line_one += "\t\t"
                for col_ix in range(len(dict_cs[colname])):
                    if dict_cs["Statistics"][col_ix] in skip_first:
                        continue
                    if str(dict_cs[colname][col_ix]).isdigit() or "." in str(dict_cs[colname][col_ix]):
                        if float(dict_cs[colname][col_ix]) > 100:
                            line_one += "NaN & "
                        else:
                            line_one += "$" + str(np.round(float(dict_cs[colname][col_ix]) * 100, 4)) + "\%$ & "
                    else:
                        if str(dict_cs[colname][col_ix]) in metric_alias:
                            if use_alias:
                                line_one += metric_alias[str(dict_cs[colname][col_ix])] + " & "
                            else:
                                line_one += str(dict_cs[colname][col_ix]) + " & "
                        else:
                            line_one += str(dict_cs[colname][col_ix]) + " & "
                line_one = line_one[:-2]
                line_one += "\\\\ \\hline\n"
            caption_txt = "The performance indicators derived from the confusion matrix for the " + translate_model[model_name] + " model when using " + translate_data[wd] + " as input."
            label_txt = "tab:cs:" + wd.replace("_", "") + ":" +  model_name
            line_one += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
            if model_name in model_print_list and by_class:
                line_one = line_one.replace(".0\%", "\%")
                #print(line_one)
                if not os.path.isdir(wd + "/latex_table/" + model_name):
                    os.makedirs(wd + "/latex_table/" + model_name)
                file_label = open(wd + "/latex_table/" + model_name + "/cs_" + model_name + ".tex", "w")
                file_label.write(line_one)
                file_label.close()
                x2 = True
                for x1 in [True, False]:
                    for x3 in [True, False]:
                        all_model[x1][x2][x3] += line_one + "\n"
                        reference_str[x1][x2][x3] += line_one + "\n"
                        all_str[x1][x2][x3] += line_one + "\n"
                        all_model_total_dict[x1][x2][x3] += line_one + "\n"
                        reference_total_dict[x1][x2][x3] += line_one + "\n"
                        all_model_dict[model_name][x1][x2][x3] += line_one + "\n"
                        reference_dict[model_name][x1][x2][x3] += line_one + "\n"
                        all_str_dict[x1][x2][x3] += line_one + "\n"
            line_one = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c|c|c|c|c|c|}\n\t\t\\hline\n\t\t & \\multicolumn{5}{c|}{Class} \\\\ \\hline\n"
            for row_ix in range(len(cs)):
                if cs[row_ix][0] in skip_first:
                    continue
                line_one += "\t\t"
                for col_ix in range(len(cs[row_ix])):
                    if str(cs[row_ix][col_ix]).isdigit() or "." in str(cs[row_ix][col_ix]):
                        if float(cs[row_ix][col_ix]) > 100:
                            line_one += "NaN & "
                        else:
                            line_one += "$" + str(np.round(float(cs[row_ix][col_ix]) * 100, 4)) + "\%$ & "
                    else:
                        if str(cs[row_ix][col_ix]) in metric_alias:
                            if use_alias:
                                line_one += metric_alias[str(cs[row_ix][col_ix])] + " & "
                            else:
                                line_one += str(cs[row_ix][col_ix]) + " & "
                        else:
                            line_one += str(cs[row_ix][col_ix]) + " & "
                line_one = line_one[:-2]
                line_one += "\\\\ \\hline\n"
            caption_txt = "The performance indicators derived from the confusion matrix for the " + translate_model[model_name] + " model when using " + translate_data[wd] + " as input."
            label_txt = "tab:cs:reverse:" + wd.replace("_", "") + ":" +  model_name
            line_one += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
            if model_name in model_print_list and by_statistics:
                line_one = line_one.replace(".0\%", "\%")
                #print(line_one)
                if not os.path.isdir(wd + "/latex_table/" + model_name):
                    os.makedirs(wd + "/latex_table/" + model_name)
                file_label = open(wd + "/latex_table/" + model_name + "/cs_reverse_" + model_name + ".tex", "w")
                file_label.write(line_one)
                file_label.close()
                x3 = True
                for x1 in [True, False]:
                    for x2 in [True, False]:
                        all_model[x1][x2][x3] += line_one + "\n"
                        reference_str[x1][x2][x3] += line_one + "\n"
                        all_str[x1][x2][x3] += line_one + "\n"
                        all_model_total_dict[x1][x2][x3] += line_one + "\n"
                        reference_total_dict[x1][x2][x3] += line_one + "\n"
                        all_model_dict[model_name][x1][x2][x3] += line_one + "\n"
                        reference_dict[model_name][x1][x2][x3] += line_one + "\n"
                        all_str_dict[x1][x2][x3] += line_one + "\n"
            #print(dict_cs)
            df_cs = pd.DataFrame(dict_cs)
            df_cs.to_csv(wd + "/" + model_name + "_cs.csv", index = False)
            for time_name in keywords_time:
                line_tm = 0
                while line_tm < len(all_lines) and time_name + " time" not in all_lines[line_tm]:
                    line_tm += 1
                marker_found = True
                if line_tm == len(all_lines):
                    line_tm = len(all_lines) - 3
                    marker_found = False
                lines_time = all_lines[line_tm + 1:line_tm + 3]
                for lix in range(len(lines_time)):
                    while "  " in lines_time[lix]:
                        lines_time[lix] = lines_time[lix].replace("  ", " ")
                    lines_time[lix] = lines_time[lix].strip().split(" ")
                for tix in range(len(lines_time[0])):
                    valt = lines_time[1][tix]
                    if not marker_found:
                        valt = "NA"
                    if lines_time[0][tix] not in dict_time_total[time_name]:
                        dict_time_total[time_name][lines_time[0][tix]] = []
                    dict_time_total[time_name][lines_time[0][tix]].append(valt)
                    if lines_time[0][tix] + "_"  + time_name.lower() not in dict_time_total_total:
                        dict_time_total_total[lines_time[0][tix] + "_"  + time_name.lower()] = []
                    dict_time_total_total[lines_time[0][tix] + "_"  + time_name.lower()].append(valt)
                dict_time_total[time_name]["Model"].append(model_name)
                if model_name not in dict_time_total_total["Model"]:
                    dict_time_total_total["Model"].append(model_name)
            for x1 in [True, False]:
                for x2 in [True, False]:
                    for x3 in [True, False]:
                        if ((x1 or x2) or x3) == False:
                            continue
                        one_name = wd + "/latex_table/all_model_" + model_name
                        if not x1:
                            one_name += "_no_cm"
                        if not x2:
                            one_name += "_no_cs"
                        if not x3:
                            one_name += "_no_cs_reverse"
                        file_label = open(one_name + ".tex", "w")
                        file_label.write(all_model[x1][x2][x3][:-1])
                        file_label.close()
    for x1 in [True, False]:
        for x2 in [True, False]:
            for x3 in [True, False]:
                if ((x1 or x2) or x3) == False:
                    continue
                one_name = ""
                if not x1:
                    one_name += "_no_cm"
                if not x2:
                    one_name += "_no_cs"
                if not x3:
                    one_name += "_no_cs_reverse"
                file_label = open(wd + "/latex_table/all_reference" + one_name + ".tex", "w")
                file_label.write(reference_str[x1][x2][x3][:-1])
                file_label.close()
                file_label = open(wd + "/latex_table/all_stats" + one_name + ".tex", "w")
                file_label.write(stats_str[x1][x2][x3][:-1])
                file_label.close()
                file_label = open(wd + "/latex_table/all_stats" + one_name + ".tex", "w")
                file_label.write(stats_str_reverse[x1][x2][x3][:-1])
                file_label.close()
    for time_name in keywords_time:
        df_dict_time_total = pd.DataFrame(dict_time_total[time_name])
        df_dict_time_total.to_csv(wd + "/time_" + time_name.lower() + "_models.csv", index = False)
        lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{"
        for key_time in dict_time_total[time_name]:
            if key_time in skip_time:
                continue
            lines_time += "|c"
        lines_time += "|}"
        lines_time += "\n\t\t\\hline\n\t\t"
        for key_time in dict_time_total[time_name]:
            if key_time in skip_time:
                continue
            lines_time += key_time + " & "
        lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        for key_val_ix in range(len(dict_time_total[time_name]["Model"])):
            lines_time += "\t\t"
            for key_name in dict_time_total[time_name]:
                if key_name in skip_time:
                    continue
                if (str(dict_time_total[time_name][key_name][key_val_ix]).isdigit() or "." in str(dict_time_total[time_name][key_name][key_val_ix])) and "C" not in str(dict_time_total[time_name][key_name][key_val_ix]):
                    lines_time += "$" + dict_time_total[time_name][key_name][key_val_ix] + "$ & "
                else:
                    lines_time += dict_time_total[time_name][key_name][key_val_ix] + " & "
            lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        caption_txt = "The " + translate_time[time_name] + " time in seconds for each model when using " + translate_data[wd] + " as input."
        label_txt = "tab:time:" + wd.replace("_", "") + ":" + time_name.lower()
        lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
        if by_time_type:
            #print(lines_time)
            if not os.path.isdir(wd + "/latex_table"):
                os.makedirs(wd + "/latex_table")
            file_label = open(wd + "/latex_table/time_" + time_name.lower() + ".tex", "w")
            file_label.write(lines_time)
            file_label.close()
            for x1 in [True, False]:
                for x2 in [True, False]:
                    for x3 in [True, False]:
                        if ((x1 or x2) or x3) == False:
                            continue
                        all_str[x1][x2][x3] += lines_time + "\n"
                        all_str_dict[x1][x2][x3] += lines_time + "\n"
            time_dict[time_name] += lines_time + "\n"
        lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c"
        for key_name in dict_time_total[time_name]:
            if key_name in skip_time:
                continue
            for key_val in dict_time_total[time_name][key_name]:
                lines_time += "|c"
            break
        lines_time += "|}"
        lines_time += "\n\t\t\\hline\n"
        for key_name in dict_time_total[time_name]:
            if key_name in skip_time:
                continue
            lines_time += "\t\t"
            lines_time += key_name + " & "
            for key_val in dict_time_total[time_name][key_name]:
                if (str(key_val).isdigit() or "." in str(key_val)) and "C" not in str(key_val):
                    lines_time += "$" + key_val + "$ & "
                else:
                    lines_time += key_val + " & "
            lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        caption_txt = "The " + translate_time[time_name] + " time in seconds for each model when using " + translate_data[wd] + " as input."
        label_txt = "tab:time:reverse:" + wd.replace("_", "") + ":" + time_name.lower()
        lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
        if by_time_model:
            #print(lines_time)
            if not os.path.isdir(wd + "/latex_table"):
                os.makedirs(wd + "/latex_table")
            file_label = open(wd + "/latex_table/time_reverse_" + time_name.lower() + ".tex", "w")
            file_label.write(lines_time)
            file_label.close()
            for x1 in [True, False]:
                for x2 in [True, False]:
                    for x3 in [True, False]:
                        if ((x1 or x2) or x3) == False:
                            continue
                        all_str[x1][x2][x3] += lines_time + "\n"
                        all_str_dict[x1][x2][x3] += lines_time + "\n"
            time_reverse_dict[time_name] += lines_time + "\n"
    df_dict_time_total_total = pd.DataFrame(dict_time_total_total)
    df_dict_time_total_total.to_csv(wd + "/time_models.csv", index = False)
    lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{"
    for key_time in dict_time_total_total:
        if key_time in skip_time:
            continue
        lines_time += "|c"
    lines_time += "|}"
    lines_time += "\n\t\t\\hline\n\t\t"
    for key_time in dict_time_total_total:
        if key_time in skip_time:
            continue
        lines_time += key_time + " & "
    lines_time = lines_time[:-2] + "\\\\ \\hline\n"
    for key_val_ix in range(len(dict_time_total_total["Model"])):
        lines_time += "\t\t"
        for key_name in dict_time_total_total:
            if key_name in skip_time:
                continue
            if (str(dict_time_total_total[key_name][key_val_ix]).isdigit() or "." in str(dict_time_total_total[key_name][key_val_ix])) and "C" not in str(dict_time_total_total[key_name][key_val_ix]):
                lines_time += "$" + dict_time_total_total[key_name][key_val_ix] + "$ & "
            else:
                lines_time += dict_time_total_total[key_name][key_val_ix] + " & "
        lines_time = lines_time[:-2] + "\\\\ \\hline\n"
    caption_txt = "The time taken for all algorithm stages in seconds for each model when using " + translate_data[wd] + " as input."
    label_txt = "tab:time:" + wd.replace("_", "")
    lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
    if by_time_type:
        #print(lines_time)
        if not os.path.isdir(wd + "/latex_table"):
            os.makedirs(wd + "/latex_table")
        file_label = open(wd + "/latex_table/time.tex", "w")
        file_label.write(lines_time)
        file_label.close()
        for x1 in [True, False]:
            for x2 in [True, False]:
                for x3 in [True, False]:
                    if ((x1 or x2) or x3) == False:
                        continue
                    all_str[x1][x2][x3] += lines_time + "\n"
                    all_str_dict[x1][x2][x3] += lines_time + "\n"
        time_total_dict += lines_time + "\n"
    lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c"
    for key_name in dict_time_total_total:
        if key_name in skip_time:
            continue
        for key_val in dict_time_total_total[key_name]:
            lines_time += "|c"
        break
    lines_time += "|}"
    lines_time += "\n\t\t\\hline\n"
    for key_name in dict_time_total_total:
        if key_name in skip_time:
            continue
        lines_time += "\t\t"
        lines_time += key_name + " & "
        for key_val in dict_time_total_total[key_name]:
            if (str(key_val).isdigit() or "." in str(key_val)) and "C" not in str(key_val):
                lines_time += "$" + key_val + "$ & "
            else:
                lines_time += key_val + " & "
        lines_time = lines_time[:-2] + "\\\\ \\hline\n"
    caption_txt = "The time taken for all algorithm stages in seconds for each model when using " + translate_data[wd] + " as input."
    label_txt = "tab:time:reverse:" + wd.replace("_", "")
    lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
    if by_time_model:
        #print(lines_time)
        if not os.path.isdir(wd + "/latex_table"):
            os.makedirs(wd + "/latex_table")
        file_label = open(wd + "/latex_table/time_reverse.tex", "w")
        file_label.write(lines_time)
        file_label.close()
        for x1 in [True, False]:
            for x2 in [True, False]:
                for x3 in [True, False]:
                    if ((x1 or x2) or x3) == False:
                        continue
                    all_str[x1][x2][x3] += lines_time + "\n"
                    all_str_dict[x1][x2][x3] += lines_time + "\n"
        time_reverse_total_dict += lines_time + "\n"
    #print(dict_co_total)
    models_list = list(dict_co_total.keys())
    metrics_list = list(dict_co_total[models_list[0]].keys())
    new_dict_co = {"Metric": metrics_list}
    for model_name in models_list:
        new_dict_co[model_name] = []
        for metric in metrics_list:
            new_dict_co[model_name].append(dict_co_total[model_name][metric])
    #print(new_dict_co)
    line_print = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{"
    for colname in new_dict_co.keys():
        line_print += "|c"
    line_print += "|}"
    line_print += "\n\t\t\\hline\n\t\t"
    for colname in new_dict_co.keys():
        line_print += colname + " & "
    line_print = line_print[:-2] + "\\\\ \\hline\n"
    for metric in metrics_list:
        if metric in skip_second:
            continue
        line_print += "\t\t"
        if use_alias_second:
            line_print += metric_alias_second[metric] + " & "
        else:
            line_print += metric_alias_fix[metric] + " & "
        for model_name in models_list:
            if "NA" not in dict_co_total[model_name][metric]:
                line_print += "$" + dict_co_total[model_name][metric] + "$ & "
            else:
                line_print += "NA & "
        line_print = line_print[:-2] + "\\\\ \\hline\n"
    caption_txt = "The accuracy, CI, NIR, $p$-value, and Kappa statistic for each model when using " + translate_data[wd] + " as input."
    label_txt = "tab:stats:" + wd.replace("_", "")
    line_print += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
    if by_metric:
        line_print = line_print.replace("2.2e-16", "2.2 \\times {10}^{-16}")
        #print(line_print)
        if not os.path.isdir(wd + "/latex_table"):
            os.makedirs(wd + "/latex_table")
        file_label = open(wd + "/latex_table/stats.tex", "w")
        file_label.write(line_print)
        file_label.close()
        for x1 in [True, False]:
            for x2 in [True, False]:
                for x3 in [True, False]:
                    if ((x1 or x2) or x3) == False:
                        continue
                    all_str[x1][x2][x3] += line_print + "\n"
                    all_str_dict[x1][x2][x3] += line_print + "\n"
        all_stats_dict += line_print + "\n"
    line_print = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c"
    for metric in metrics_list:
        if metric in skip_second:
            continue
        line_print += "|c"
    line_print += "|}"
    line_print += "\n\t\t\\hline\n\t\tModel & "
    for metric in metrics_list:
        if metric in skip_second:
            continue
        if use_alias_second:
            line_print += metric_alias_second[metric] + " & "
        else:
            line_print += metric_alias_fix[metric] + " & "
    line_print = line_print[:-2] + "\\\\ \\hline\n"
    for model_name in models_list:
        line_print += "\t\t" + model_name + " & "
        for metric in metrics_list:
            if metric in skip_second:
                continue
            if "NA" not in dict_co_total[model_name][metric]:
                line_print += "$" + dict_co_total[model_name][metric] + "$ & "
            else:
                line_print += "NA & "
        line_print = line_print[:-2] + "\\\\ \\hline\n"
    caption_txt = "The accuracy, CI, NIR, $p$-value, and Kappa statistic for each model when using " + translate_data[wd] + " as input."
    label_txt = "tab:stats:reverse:" + wd.replace("_", "")
    line_print += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
    if by_model:
        line_print = line_print.replace("2.2e-16", "2.2 \\times {10}^{-16}")
        #print(line_print)
        if not os.path.isdir(wd + "/latex_table"):
            os.makedirs(wd + "/latex_table")
        file_label = open(wd + "/latex_table/stats_reverse.tex", "w")
        file_label.write(line_print)
        file_label.close()
        for x1 in [True, False]:
            for x2 in [True, False]:
                for x3 in [True, False]:
                    if ((x1 or x2) or x3) == False:
                        continue
                    all_str[x1][x2][x3] += line_print + "\n"
                    all_str_dict[x1][x2][x3] += line_print + "\n"
        all_stats_reverse_dict += line_print + "\n"
    df_new_dict_co = pd.DataFrame(new_dict_co)
    df_new_dict_co.to_csv(wd + "/stats.csv", index = False)
    dict_time_a_total = {"Models": []}
    dict_time_a = dict()
    for num_ansamble in ansamble_list:
        dict_time_a[num_ansamble] = {"Models": []}
    for num_ansamble in ansamble_list:
        file_open = open(wd + "/ansamble" + str(num_ansamble) + ".txt")
        start_lines = file_open.readlines()
        file_open.close()
        all_lines = start_lines[- (1 + num_ansamble) * (1 + int(np.floor(num_ansamble/mod_val))) -2:-2]
        lines_time_a = start_lines[-2:]
        for lix in range(len(lines_time_a)):
            while "  " in lines_time_a[lix]:
                lines_time_a[lix] = lines_time_a[lix].replace("  ", " ")
            lines_time_a[lix] = lines_time_a[lix].strip().split(" ")
        for line_ix in range(len(all_lines)):
            orig_start = all_lines[line_ix][0]
            while "  " in all_lines[line_ix]:
                all_lines[line_ix] = all_lines[line_ix].replace("  ", " ")
            all_lines[line_ix] = all_lines[line_ix].strip().split()
            if orig_start == " ":
                all_lines[line_ix].insert(0, "Model")
        dict_ansamble = dict()
        for row_ix in range(len(all_lines)):
            if all_lines[row_ix][0] not in dict_ansamble:
                dict_ansamble[all_lines[row_ix][0]] = []
        for row_ix in range(len(all_lines)):
            if all_lines[row_ix] != "Model":
                for col_ix in range(1, len(all_lines[row_ix])):
                    dict_ansamble[all_lines[row_ix][0]].append(all_lines[row_ix][col_ix])
        df_new_dict_a = pd.DataFrame(dict_ansamble)
        df_new_dict_a.to_csv(wd + "/ansamble" + str(num_ansamble) + ".csv", index = False)
        #print(all_lines)
        lines_print_a = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c"
        for i in range(num_ansamble):
            lines_print_a += "|c"
        lines_print_a += "|}"
        lines_print_a += "\n\t\t\\hline\n"
        ord = ["Model"]
        for m in model_name_list:
            ord.append(m)
        for colname in ord:
            if colname not in dict_ansamble.keys():
                continue
            lines_print_a += "\t\t" + colname + " & "
            for colname2 in ord:
                if colname2 not in dict_ansamble.keys():
                    continue
                if colname2 != "Model":
                    val_ix = dict_ansamble["Model"].index(colname2)
                    if colname != "Model":
                        lines_print_a += "$" + str(np.round(float(dict_ansamble[colname][val_ix]) * 100, 4)) + "\%$ & "
                    else:
                        lines_print_a += str(dict_ansamble[colname][val_ix]) + " & "
            lines_print_a = lines_print_a[:-2] + "\\\\ \\hline\n"
        caption_txt = "The model coorelation of an ansamble of "  + str(num_ansamble) + " models when using " + translate_data[wd] + " as input."
        label_txt = "tab:ansamble" + str(num_ansamble) + ":" + wd.replace("_", "")
        lines_print_a += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
        if num_ansamble in ansamble_print and by_ansamble:
            #print(lines_print_a)
            file_label = open(wd + "/latex_table/ansamble" + str(num_ansamble) + ".tex", "w")
            file_label.write(lines_print_a)
            file_label.close()
            for x1 in [True, False]:
                for x2 in [True, False]:
                    for x3 in [True, False]:
                        if ((x1 or x2) or x3) == False:
                            continue
                        all_str[x1][x2][x3] += lines_print_a + "\n"
                        all_str_dict[x1][x2][x3] += lines_print_a + "\n"
            ansamble_dict[num_ansamble] += lines_print_a + "\n"
            ansamble_dict_total += lines_print_a + "\n"
        for tix in range(len(lines_time_a[0])):
            valt = lines_time_a[1][tix]
            if not marker_found:
                valt = "NA"
            if lines_time_a[0][tix] not in dict_time_a[num_ansamble]:
                dict_time_a[num_ansamble][lines_time_a[0][tix]] = []
            dict_time_a[num_ansamble][lines_time_a[0][tix]].append(valt)
            if lines_time_a[0][tix] not in dict_time_a_total:
                dict_time_a_total[lines_time_a[0][tix]] = []
            dict_time_a_total[lines_time_a[0][tix]].append(valt)
        dict_time_a[num_ansamble]["Models"].append(num_ansamble)
        dict_time_a_total["Models"].append(num_ansamble)
        df_new_dict_time_a = pd.DataFrame(dict_time_a[num_ansamble])
        df_new_dict_time_a.to_csv(wd + "/time_ansamble" + str(num_ansamble) + ".csv", index = False)
        lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{"
        for key_time in dict_time_a[num_ansamble]:
            if key_time in skip_time:
                continue
            lines_time += "|c"
        lines_time += "|}"
        lines_time += "\n\t\t\\hline\n\t\t"
        for key_time in dict_time_a[num_ansamble]:
            if key_time in skip_time:
                continue
            lines_time += key_time + " & "
        lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        for key_val_ix in range(len(dict_time_a[num_ansamble]["Models"])):
            lines_time += "\t\t"
            for key_name in dict_time_a[num_ansamble]:
                if key_name in skip_time:
                    continue
                if (str(dict_time_a[num_ansamble][key_name][key_val_ix]).isdigit() or "." in str(dict_time_a[num_ansamble][key_name][key_val_ix])) and "C" not in str(dict_time_a[num_ansamble][key_name][key_val_ix]):
                    lines_time += "$" + str(dict_time_a[num_ansamble][key_name][key_val_ix]) + "$ & "
                else:
                    lines_time += str(dict_time_a[num_ansamble][key_name][key_val_ix]) + " & "
            lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        caption_txt = "The time taken for all algorithm stages in seconds for an ansamble of "  + str(num_ansamble) + " models when using " + translate_data[wd] + " as input."
        label_txt = "tab:time:ansamble:" + wd.replace("_", "") + ":" + str(num_ansamble)
        lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
        if by_time_type_ansamble and num_ansamble in ansamble_print and by_ansamble:
            #print(lines_time)
            if not os.path.isdir(wd + "/latex_table"):
                os.makedirs(wd + "/latex_table")
            file_label = open(wd + "/latex_table/time_ansamble_" + str(num_ansamble) + ".tex", "w")
            file_label.write(lines_time)
            file_label.close()
            for x1 in [True, False]:
                for x2 in [True, False]:
                    for x3 in [True, False]:
                        if ((x1 or x2) or x3) == False:
                            continue
                        all_str[x1][x2][x3] += lines_time + "\n"
                        all_str_dict[x1][x2][x3] += lines_time + "\n"
            time_ansamble_reverse_dict[num_ansamble] += lines_time + "\n"
        lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c"
        for key_name in dict_time_a[num_ansamble]:
            if key_name in skip_time:
                continue
            for key_val in dict_time_a[num_ansamble][key_name]:
                lines_time += "|c"
            break
        lines_time += "|}"
        lines_time += "\n\t\t\\hline\n"
        for key_name in dict_time_a[num_ansamble]:
            if key_name in skip_time:
                continue
            lines_time += "\t\t"
            lines_time += key_name + " & "
            for key_val in dict_time_a[num_ansamble][key_name]:
                if (str(key_val).isdigit() or "." in str(key_val)) and "C" not in str(key_val):
                    lines_time += "$" + str(key_val) + "$ & "
                else:
                    lines_time += str(key_val) + " & "
            lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        caption_txt = "The time taken for all algorithm stages in seconds for an ansamble of "  + str(num_ansamble) + " models when using " + translate_data[wd] + " as input."
        label_txt = "tab:time:ansamble:reverse:" + wd.replace("_", "") + ":"  + str(num_ansamble)
        lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
        if by_time_model_ansamble and num_ansamble in ansamble_print and by_ansamble:
            #print(lines_time)
            if not os.path.isdir(wd + "/latex_table"):
                os.makedirs(wd + "/latex_table")
            file_label = open(wd + "/latex_table/time_ansamble_reverse_" + str(num_ansamble) + ".tex", "w")
            file_label.write(lines_time)
            file_label.close()
            for x1 in [True, False]:
                for x2 in [True, False]:
                    for x3 in [True, False]:
                        if ((x1 or x2) or x3) == False:
                            continue
                        all_str[x1][x2][x3] += lines_time + "\n"
                        all_str_dict[x1][x2][x3] += lines_time + "\n"
            time_ansamble_dict[num_ansamble] += lines_time + "\n"
    lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{"
    for key_time in dict_time_a_total:
        if key_time in skip_time:
            continue
        lines_time += "|c"
    lines_time += "|}"
    lines_time += "\n\t\t\\hline\n\t\t"
    for key_time in dict_time_a_total:
        if key_time in skip_time:
            continue
        lines_time += key_time + " & "
    lines_time = lines_time[:-2] + "\\\\ \\hline\n"
    for key_val_ix in range(len(dict_time_a_total["Models"])):
        lines_time += "\t\t"
        for key_name in dict_time_a_total:
            if key_name in skip_time:
                continue
            if (str(dict_time_a_total[key_name][key_val_ix]).isdigit() or "." in str(dict_time_a_total[key_name][key_val_ix])) and "C" not in str(dict_time_a_total[key_name][key_val_ix]):
                lines_time += "$" + str(dict_time_a_total[key_name][key_val_ix]) + "$ & "
            else:
                lines_time += str(dict_time_a_total[key_name][key_val_ix]) + " & "
        lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        caption_txt = "The time taken for all algorithm stages in seconds for an ansamble of different numbers of models when using " + translate_data[wd] + " as input."
    label_txt = "tab:time:ansamble:" + wd.replace("_", "")
    lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
    if by_time_type_ansamble and by_ansamble:
        #print(lines_time)
        if not os.path.isdir(wd + "/latex_table"):
            os.makedirs(wd + "/latex_table")
        file_label = open(wd + "/latex_table/time_ansamble.tex", "w")
        file_label.write(lines_time)
        file_label.close()
        for x1 in [True, False]:
            for x2 in [True, False]:
                for x3 in [True, False]:
                    if ((x1 or x2) or x3) == False:
                        continue
                    all_str[x1][x2][x3] += lines_time + "\n"
                    all_str_dict[x1][x2][x3] += lines_time + "\n"
        time_ansamble_reverse_total_dict += lines_time + "\n"
    lines_time = "\\begin{table}[" + position_start + "]\n\t\\centering\n\t\\begin{tabular}{|c"
    for key_name in dict_time_a_total:
        if key_name in skip_time:
            continue
        for key_val in dict_time_a_total[key_name]:
            lines_time += "|c"
        break
    lines_time += "|}"
    lines_time += "\n\t\t\\hline\n"
    for key_name in dict_time_a_total:
        if key_name in skip_time:
            continue
        lines_time += "\t\t"
        lines_time += key_name + " & "
        for key_val in dict_time_a_total[key_name]:
            if (str(key_val).isdigit() or "." in str(key_val)) and "C" not in str(key_val):
                lines_time += "$" + str(key_val) + "$ & "
            else:
                lines_time += str(key_val) + " & "
        lines_time = lines_time[:-2] + "\\\\ \\hline\n"
        caption_txt = "The time taken for all algorithm stages in seconds for an ansamble of different numbers of models when using " + translate_data[wd] + " as input."
    label_txt = "tab:time:ansamble:reverse:" + wd.replace("_", "")
    lines_time += "\t\\end{tabular}\n\t\\caption{" + caption_txt + "}\n\t\\label{" + label_txt + "}\n\\end{table}\n"
    if by_time_model_ansamble and by_ansamble:
        #print(lines_time)
        if not os.path.isdir(wd + "/latex_table"):
            os.makedirs(wd + "/latex_table")
        file_label = open(wd + "/latex_table/time_ansamble_reverse.tex", "w")
        file_label.write(lines_time)
        file_label.close()
        for x1 in [True, False]:
            for x2 in [True, False]:
                for x3 in [True, False]:
                    if ((x1 or x2) or x3) == False:
                        continue
                    all_str[x1][x2][x3] += lines_time + "\n"
                    all_str_dict[x1][x2][x3] += lines_time + "\n"
        time_ansamble_total_dict += lines_time + "\n"
    df_new_dict_time_a_total = pd.DataFrame(dict_time_a_total)
    df_new_dict_time_a_total.to_csv(wd + "/time_ansamble_total.csv", index = False)
    for x1 in [True, False]:
        for x2 in [True, False]:
            for x3 in [True, False]:
                if ((x1 or x2) or x3) == False:
                    continue
                one_name = ""
                if not x1:
                    one_name += "_no_cm"
                if not x2:
                    one_name += "_no_cs"
                if not x3:
                    one_name += "_no_cs_reverse"
                file_label = open(wd + "/latex_table/all_str" + one_name + ".tex", "w")
                file_label.write(all_str[x1][x2][x3][:-1])
                file_label.close()
                if not os.path.isdir("latex_table_total"):
                    os.makedirs("latex_table_total")
                file_label = open("latex_table_total/all_model_total_dict" + one_name + ".tex", "w")
                file_label.write(all_model_total_dict[x1][x2][x3][:-1])
                file_label.close()
                file_label = open("latex_table_total/reference_total_dict" + one_name + ".tex", "w")
                file_label.write(reference_total_dict[x1][x2][x3][:-1])
                file_label.close()
                file_label = open("latex_table_total/stats_total_dict" + one_name + ".tex", "w")
                file_label.write(stats_total_dict[x1][x2][x3][:-1])
                file_label.close()
                file_label = open("latex_table_total/stats_reverse_total_dict" + one_name + ".tex", "w")
                file_label.write(stats_reverse_total_dict[x1][x2][x3][:-1])
                file_label.close()
                for model_name in model_name_list:
                    if not os.path.isdir("latex_table_total/" + model_name):
                        os.makedirs("latex_table_total/" + model_name)
                    file_label = open("latex_table_total/" + model_name + "/all_model_dict_" + model_name + one_name + ".tex", "w")
                    file_label.write(all_model_dict[model_name][x1][x2][x3][:-1])
                    file_label.close()
                    file_label = open("latex_table_total/" + model_name + "/reference_dict_" + model_name + one_name + ".tex", "w")
                    file_label.write(reference_dict[model_name][x1][x2][x3][:-1])
                    file_label.close()
                    file_label = open("latex_table_total/" + model_name + "/stats_dict_" + model_name + one_name + ".tex", "w")
                    file_label.write(stats_dict[model_name][x1][x2][x3][:-1])
                    file_label.close()
                    file_label = open("latex_table_total/" + model_name + "/stats_reverse_dict_" + model_name + one_name + ".tex", "w")
                    file_label.write(stats_reverse_dict[model_name][x1][x2][x3][:-1])
                    file_label.close()
file_label = open("latex_table_total/time_total_dict.tex", "w")
file_label.write(time_total_dict[:-1])
file_label.close()
file_label = open("latex_table_total/time_reverse_total_dict.tex", "w")
file_label.write(time_reverse_total_dict[:-1])
file_label.close()
file_label = open("latex_table_total/all_stats_dict.tex", "w")
file_label.write(all_stats_dict[:-1])
file_label.close()
file_label = open("latex_table_total/all_stats_reverse_dict.tex", "w")
file_label.write(all_stats_reverse_dict[:-1])
file_label.close()
file_label = open("latex_table_total/ansamble_dict_total.tex", "w")
file_label.write(ansamble_dict_total[:-1])
file_label.close()
file_label = open("latex_table_total/time_ansamble_total_dict.tex", "w")
file_label.write(time_ansamble_total_dict[:-1])
file_label.close()
file_label = open("latex_table_total/time_ansamble_reverse_total_dict.tex", "w")
file_label.write(time_ansamble_reverse_total_dict[:-1])
file_label.close()
for an in ansamble_list:
    file_label = open("latex_table_total/ansamble_dict_" + str(an) + ".tex", "w")
    file_label.write(ansamble_dict[an][:-1])
    file_label.close()
    file_label = open("latex_table_total/time_ansamble_dict_" + str(an) + ".tex", "w")
    file_label.write(time_ansamble_dict[an][:-1])
    file_label.close()
    file_label = open("latex_table_total/time_ansamble_reverse_dict_" + str(an) + ".tex", "w")
    file_label.write(time_ansamble_reverse_dict[an][:-1])
    file_label.close()
all_str_dict = ""
for kt in keywords_time:
    file_label = open("latex_table_total/time_dict_" + kt.lower() + ".tex", "w")
    file_label.write(time_dict[kt][:-1])
    file_label.close()
    file_label = open("latex_table_total/time_reverse_dict_" + kt.lower() + ".tex", "w")
    file_label.write(time_reverse_dict[kt][:-1])
    file_label.close()