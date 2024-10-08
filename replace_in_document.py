
name = "main"

def replace_begin_end(merged_lines, old_start, new_start, old_end, new_end):
    while old_start in merged_lines:
        ix_begin = merged_lines.find(old_start)
        ix_end = ix_begin + len(old_start)
        substr_use = merged_lines[ix_begin:ix_end+1]
        while not old_start in substr_use or not old_end in substr_use or substr_use.count("{") != substr_use.count("}") or substr_use.count("$") % 2 != 0:
            ix_end += 1
            if ix_end >= len(merged_lines):
                break
            substr_use = merged_lines[ix_begin:ix_end+1]
        substr_use_new = substr_use.replace(old_start, new_start).replace(old_end, new_end)
        merged_lines = merged_lines.replace(substr_use, substr_use_new)
    return merged_lines

def remove_begin_end(merged_lines, old_start, old_end):
    while old_start in merged_lines:
        ix_begin = merged_lines.find(old_start)
        ix_end = ix_begin + len(old_start)
        substr_use = merged_lines[ix_begin:ix_end+1]
        while not old_start in substr_use or not old_end in substr_use or substr_use.count("{") != substr_use.count("}") or substr_use.count("$") % 2 != 0:
            ix_end += 1
            if ix_end >= len(merged_lines):
                break
            substr_use = merged_lines[ix_begin:ix_end+1]
        merged_lines = merged_lines.replace(substr_use, "")
    return merged_lines

def add_ix_replace(merged_lines):
    ix_start = []
    for pos in range(len(merged_lines)):
        if merged_lines[pos] == "$":
            ix_start.append(pos)
    replacements = []
    for ix in range(0, len(ix_start) - 1, 2):
        pos1 = ix_start[ix]
        pos2 = ix_start[ix + 1]
        new_use = merged_lines[pos1:pos2+1]
        in_tabular = merged_lines[:pos2+1].count("begin{tabular}") != merged_lines[:pos2+1].count("end{tabular}")
        if in_tabular:
            continue
        long_equality = "=" in new_use 
        if long_equality:
            parts = new_use[1:-1].split("=")
            parts = [len(p.strip()) for p in parts]
            long_equality = len(parts) > 2
        if long_equality or "frac" in new_use or "\\sum" in new_use or "\\int" in new_use or "max" in new_use:
            replacements.append((pos1, pos2, new_use, "\\begin{equation}\n\t" + new_use[1:-1].strip() + "\n\t\label{eqn:" + str(len(replacements)+1) + "}\n\\end{equation}"))
    for r in replacements:
        merged_lines = merged_lines.replace(r[2], r[3])
    print(len(replacements))
    return merged_lines

file_open = open(name + ".tex", "r")
all_lines = file_open.readlines()
file_open.close()
old_starts = ["\\cite{", "Equation~\\ref{eqn:", "$\\displaystyle ", "{\\displaystyle ", "\\begin{equation}", "\\begin{align*}"]
old_ends = ["}", "}", "$", "}", "\\end{equation}", "\\end{align*}"]
new_starts = ["citestuff(", "Equation~", "$", "$", "$", "$\\begin{aligned}"]
new_ends = [")", "", "$", "$", "$", "\\end{aligned}$"]
merged_lines_all = ""
for l in all_lines:
    merged_lines_all += l
merged_lines_no_cite_all = merged_lines_all
for ix in range(len(old_ends)):
    if not "cite" in old_starts[ix] or "ation" in old_starts[ix]:
        merged_lines_all = replace_begin_end(merged_lines_all, old_starts[ix], new_starts[ix], old_ends[ix], new_ends[ix])
    merged_lines_no_cite_all = replace_begin_end(merged_lines_no_cite_all, old_starts[ix], new_starts[ix], old_ends[ix], new_ends[ix])
merged_lines_all = remove_begin_end(merged_lines_all, "\\label{eqn:", "}")
merged_lines_all = add_ix_replace(merged_lines_all)
merged_lines_no_cite_all = remove_begin_end(merged_lines_no_cite_all, "\\label{eqn:", "}")
merged_lines_no_cite_all = add_ix_replace(merged_lines_no_cite_all)
file_w = open(name + "_replaced.tex", "w")
file_w.write(merged_lines_all)
file_w.close()
file_w = open(name + "_no_cite_replaced.tex", "w")
file_w.write(merged_lines_no_cite_all)
file_w.close()
from subprocess import call
list_subproc_no_cite_replaced = ["pandoc", "-s", "-o", name + "_no_cite_replaced.docx", name + "_no_cite_replaced.tex"]
list_subproc_replaced = ["pandoc", "-s", "-o", name + "_replaced.docx", name + "_replaced.tex"]
list_subproc = ["pandoc", "-s", "-o", name + ".docx", name + ".tex"]

call(list_subproc_no_cite_replaced)
call(list_subproc_replaced)
call(list_subproc)