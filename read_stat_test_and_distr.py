make_a_table_start = "\\begin{table}[!ht]\n\t\\centering"
make_a_table_start += "\n\t\\caption{The minimum, $1^{st}$ quartile, median, arithmetic mean, $3^{rd}$ quartile, and maximum values for all variables, DESCUSE.}"
make_a_table_start += "\n\t\label{tab:minmaxKEYUSE}\n\t\\begin{tabular}{|c|}\n\t\t\\hline"

make_a_table_end = "\n\t\end{tabular}\n\end{table}"

filenames_desc = {"_2": "regardless of $\acrshort{tec}$ ranges",
                  "_3": "where the $\acrshort{tec}$ is less than $300$ $nT$",
                  "_3_P": "for the P class based on $\\acrshort{dst}$",
                  "_3_N": "for the N class based on $\\acrshort{dst}$",
                  "_3_R": "for the R class based on $\\acrshort{dst}$",
                  "_3_T": "for the T class based on $\\acrshort{dst}$",
                  "_3_E": "for the E class based on $\\acrshort{dst}$"}

for filename_use in filenames_desc:

    csv_name = "data_vars" + filename_use + ".txt"
    csv_name_normal = "data_vars" + filename_use + "_test_normal.txt"

    file_csv_name = open(csv_name, "r")
    lines_csv_name = file_csv_name.readlines()
    file_csv_name.close()

    file_csv_name_normal = open(csv_name_normal, "r")
    lines_csv_name_normal = file_csv_name_normal.readlines()
    file_csv_name_normal.close()
    
    p_vals = dict()
    last_test = ""
    last_data = ""
    for line_p_val in lines_csv_name_normal:
        if "test" in line_p_val:
            last_test = line_p_val.strip()
        if "data:" in line_p_val:
            last_data = line_p_val.replace("data:", "").strip()
        if "p-value" in line_p_val:
            if last_data not in p_vals:
                p_vals[last_data] = dict()
            p_vals[last_data][last_test] = eval(line_p_val.strip().split(" ")[-1])
    
    for use_data in p_vals:
        for use_test in p_vals[use_data]:
            if p_vals[use_data][use_test] > 0.05:
                print(use_data, use_test, p_vals[use_data][use_test])

    dict_usable = dict()
    for line_stat_val in lines_csv_name:
        if ":" in line_stat_val:
            metric_one = line_stat_val.strip().split(":")[0].strip()
            values_used = line_stat_val.replace(metric_one, "").replace(":", "")
            while "  " in values_used:
                values_used = values_used.replace("  ", " ")
            values_used = [float(x) for x in values_used.strip().split(" ")]
            for ix_var in range(len(values_used)):
                var_used = variables_partial[ix_var]
                if var_used in ["DOY", "hr"]:
                    continue
                if metric_one not in dict_usable:
                    dict_usable[metric_one] = dict()
                dict_usable[metric_one][var_used] = values_used[ix_var]
        else:
            variables_line = line_stat_val.strip()
            while "  " in variables_line:
                variables_line = variables_line.replace("  ", " ")
            variables_partial = variables_line.split(" ")
            
    strtotal = make_a_table_start
    strline = "\n\t\t "
    transform_var = {"TEC": "$\\acrshort{tec}$",
                     "dTEC": "$\\acrshort{dtec}$",
                     "Dst": "$\\acrshort{dst}$",
                     "Bx": "$B_{x}$", 
                     "By": "$B_{y}$",
                     "Bz": "$B_{z}$",
                     "ap": "$a_{p}$"}
    numvar = len(dict_usable[list(dict_usable.keys())[0]]) + 1
    if "3_" in filename_use:
        strtotal += "\n\t\t\\multicolumn{" + str(numvar) + "}{|c|}{" + filename_use.split("_")[-1] + "} \\\\ \\hline"
    for var_use in dict_usable[list(dict_usable.keys())[0]]:
        strline += " & " + transform_var[var_use]
    strtotal += strline + " \\\\ \\hline"
    for metric_use in dict_usable:
        strline = "\n\t\t" + metric_use.replace("1st", "$1^{st}$").replace("3rd", "$3^{rd}$")
        for var_use in dict_usable[metric_use]:
            strline += " & $" + str(dict_usable[metric_use][var_use]) + "$"
        strtotal += strline + " \\\\ \\hline"
    strtotal += make_a_table_end
    numc = "|c" * numvar + "|"
    print(strtotal.replace("{tabular}{|c|", "{tabular}{" + numc).replace("KEYUSE", filename_use).replace("DESCUSE", filenames_desc[filename_use]))
