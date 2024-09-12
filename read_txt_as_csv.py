import pandas as pd

model_name_list = ["svmPoly", "C5.0", "nb", "nnet", "pls", "fda", "pcaNNet", "binda"]
wd = ""
for model_name in model_name_list:
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
        cm = all_lines[line_ref + 1:line_ref + 7]
        for line_ix in range(len(cm)):
            while "  " in cm[line_ix]:
                cm[line_ix] = cm[line_ix].replace("  ", " ")
            cm[line_ix] = cm[line_ix].strip().split(" ")
            for val_ix in range(len(cm[line_ix])):
                if str(cm[line_ix][val_ix]).isdigit():
                    cm[line_ix][val_ix] = int(cm[line_ix][val_ix])
            print(cm[line_ix])
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
        print(dict_cm)
        df_cm = pd.DataFrame(dict_cm)
        df_cm.to_csv(wd + model_name + "_cm.csv", index = False)
        cs = all_lines[line_sen - 1:line_sen + 8]
        for line_ix in range(len(cs)):
            while "  " in cs[line_ix]:
                cs[line_ix] = cs[line_ix].replace("  ", " ")
            cs[line_ix] = cs[line_ix].replace("Class: ", "")
            cs[line_ix] = cs[line_ix].replace("NaN", "1000")
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
            print(cs[line_ix])
        dict_cs = dict()
        for col_ix in range(len(cs[0])):
            colname = cs[0][col_ix]
            dict_cs[colname] = []
            for row_ix in range(1, len(all_lines[line_sen:line_sen + 9])):
                val_use = cs[row_ix][col_ix]
                if str(val_use).isdigit() and val_use > 100:
                    dict_cs[colname].append("Na")
                else:
                    dict_cs[colname].append(cs[row_ix][col_ix])
        line_one = "\\cline{2-6}\n\\multicolumn{1}{c|}{} & \\multicolumn{5}{c|}{Class} \\\\ \\hline\n"
        for row_ix in range(len(cs)):
            for col_ix in range(len(cs[row_ix])):
                line_one += str(cs[row_ix][col_ix]) + " & "
            line_one = line_one[:-2]
            line_one += "\\\\ \\hline\n"
        print(line_one)
        print(dict_cs)
        df_cs = pd.DataFrame(dict_cs)
        df_cs.to_csv(wd + model_name + "_cs.csv", index = False)