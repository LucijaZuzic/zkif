dir = ""

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

def find_citation(merged_lines):
    keys_cite = set()
    for pos in range(len(merged_lines)):
        if merged_lines[pos] == "@":
            pos_start = pos + 1
            while merged_lines[pos_start] != "{":
                pos_start += 1
            pos_end = pos + 1
            while merged_lines[pos_end] != ",":
                pos_end += 1
            keys_cite.add((merged_lines[pos:pos_end], merged_lines[pos_start+1:pos_end]))
    return keys_cite

file_bibliography = open(dir + "bibliography.bib", "r")
all_lines_bibliography = file_bibliography.readlines()
file_bibliography.close()
merged_lines_all_bibliography = ""
for l in all_lines_bibliography:
    if l[0] != "#":
        merged_lines_all_bibliography += l
merged_lines_no_cite = merged_lines_all_bibliography
file_open = open(dir + "main_replaced.tex", "r")
all_lines = file_open.readlines()
file_open.close()
merged_lines_all = ""
for l in all_lines:
    merged_lines_all += l
keys_cited = find_citation(merged_lines_all_bibliography)
errs = 0
for k in keys_cited:
    if k[1] not in merged_lines_all:
        errs += 1
        merged_lines_no_cite = remove_begin_end(merged_lines_no_cite, k[0], "}")
print(errs)
file_bibliography_new = open(dir + "bibliography_short.bib", "w")
while "\n\n" in merged_lines_no_cite:
    merged_lines_no_cite = merged_lines_no_cite.replace("\n\n", "\n")
file_bibliography_new.write(merged_lines_no_cite.replace("author = {}", "author = {Developers, R}").replace("}\n", "}\n\n").replace("}\n\n}", "}\n}"))
file_bibliography_new.close()