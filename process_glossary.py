file_open = open("main_glossary.tex", "r", encoding="UTF8")
all_lines = file_open.readlines()
file_open.close()

acro_dict = dict()
merged_lines_all = ""
for l in all_lines:
    merged_lines_all += l
    if "newacronym" in l:
        acro_parts = l.replace("\\newacronym{", "")[:-2].split("}{")
        acro_dict[acro_parts[0]] = (acro_parts[1], acro_parts[2])
merged_lines_no_acro = merged_lines_all
long_for_short = dict()
for w in acro_dict:
    merged_lines_no_acro = merged_lines_no_acro.replace("\\acrlong{" + w + "}", acro_dict[w][1])
    merged_lines_no_acro = merged_lines_no_acro.replace("\\acrshort{" + w + "}", acro_dict[w][0])
    merged_lines_no_acro = merged_lines_no_acro.replace("\\acrfull{" + w + "}", acro_dict[w][1]+ " (" + acro_dict[w][0] + ")")
    long_for_short[acro_dict[w][0]] = acro_dict[w][1]
all_acro_short = sorted(list(set([acro_dict[w][0] for w in acro_dict])))
first_letter = sorted(list(set([acro_dict[w][0][0] for w in acro_dict])))
all_acro = ""
for l in first_letter:
    for a in all_acro_short:
        if a[0] != l:
            continue
        all_acro += "\\textit{" + a + "} " + long_for_short[a] + "\n\n"
    if l != first_letter[-1]:
        all_acro += "\n\\\\[2\\baselineskip]\n\n"
print(all_acro)
merged_lines_no_acro = merged_lines_no_acro.replace("\\printglossary[type=\\acronymtype]", "\\section{Acronyms}\n\\label{sec:Acronyms}\n\n" + all_acro)
file_open_w = open("main.tex", "w", encoding="UTF8")
file_open_w .write(merged_lines_no_acro)
file_open_w.close()