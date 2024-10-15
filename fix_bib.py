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

def get_begin_end(merged_lines, old_start, old_end):
    while old_start in merged_lines:
        ix_begin = merged_lines.find(old_start)
        ix_end = ix_begin + len(old_start)
        substr_use = merged_lines[ix_begin:ix_end+1]
        while not old_start in substr_use or not old_end in substr_use or substr_use.count("{") != substr_use.count("}") or substr_use.count("$") % 2 != 0:
            ix_end += 1
            if ix_end >= len(merged_lines):
                break
            substr_use = merged_lines[ix_begin:ix_end+1]
        pos_start = ix_begin + 1
        while merged_lines[pos_start] != "{":
            pos_start += 1
        substr_use = substr_use.replace(merged_lines[ix_begin:pos_start], merged_lines[ix_begin:pos_start].lower())
        kws = ["title"]
        for kw in kws:
            pos_title_begin = substr_use.find(kw)
            if pos_title_begin == -1:
                continue
            while substr_use[pos_title_begin - 1] >= "a" and substr_use[pos_title_begin - 1] <= "z":
                pos_title_begin = substr_use.find(kw, pos_title_begin + len(kw))
            pos_title_end = pos_title_begin + 1
            substr_title = substr_use[pos_title_begin:pos_title_end+1]
            while substr_title.count("{") != substr_title.count("}") or substr_title.count("{") < 1 or substr_title.count("}") < 1:
                pos_title_end += 1 
                substr_title = substr_use[pos_title_begin:pos_title_end+1]
            substr_title_new = substr_title
            for letter in substr_title:
                if letter.isupper():
                    substr_title_new = substr_title_new.replace(letter, "{" + letter + "}")
                    while substr_title_new.count("{{" + letter + "}}"):
                        substr_title_new = substr_title_new.replace("{{" + letter + "}}", "{" + letter + "}")
            substr_use = substr_use.replace(substr_title, substr_title_new)
        if "author" not in substr_use:
            print(substr_use)
        return substr_use

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

def add_citation(merged_lines, dicti_stuff, marker_start, marker_end):
    pos_o_citen = []
    posf = 0
    find_cite = merged_lines.find("\\cite", posf)
    while find_cite != -1 and posf < len(merged_lines):
        begin_cite = merged_lines.find("\\cite", posf)
        posf = begin_cite + 1
        if "\\citestuff" not in merged_lines:
            end_cite = merged_lines.find("}", posf)
        if "\\citestuff" in merged_lines:
            end_cite = merged_lines.find(")", posf)
        pos_o_citen.append(merged_lines[begin_cite:end_cite+1])
        find_cite = merged_lines.find("\\cite", posf)
    prep = 0
    for substr_use in pos_o_citen:
        #print(substr_use)
        substr_use_new = substr_use.replace(" ", "").replace("\\citestuff", "").replace("\\cite", "").replace("(", "").replace(")", "").replace("{", "").replace("}", "")
        #print(substr_use_new)
        for d in dicti_stuff:
            substr_use_new = substr_use_new.replace(d, str(dicti_stuff[d]))
        prep += 1
        merged_lines = merged_lines.replace(substr_use, marker_start + substr_use_new.replace(",", ", ").replace("  ", " ") + marker_end)
    print(prep)
    return merged_lines

file_refs = open(dir + "refs.txt", "r", encoding="UTF8")
all_refs = file_refs.readlines()
file_refs.close()
merged_refs_all = ""
for l in all_refs:
    merged_refs_all += l.replace("]", "] ")
file_refs_new = open(dir + "refs_new.txt", "w", encoding="UTF8")
file_refs_new.write(merged_refs_all)
file_refs_new.close()
file_bibliography = open(dir + "bibliography.bib", "r", encoding="UTF8")
all_lines_bibliography = file_bibliography.readlines()
file_bibliography.close()
merged_lines_all_bibliography = ""
for l in all_lines_bibliography:
    if l[0] != "#":
        merged_lines_all_bibliography += l
file_open = open(dir + "main_replaced.tex", "r", encoding="UTF8")
all_lines = file_open.readlines()
file_open.close()
merged_lines_all = ""
for l in all_lines:
    merged_lines_all += l
keys_cited = find_citation(merged_lines_all_bibliography)
errs = 0
errs_set = set()
loc_of_keys = dict()
nk_of_keys = dict()
ks = []
pos_o_cite = []
posf = 0
find_cite = merged_lines_all.find("\\cite{", posf)
while find_cite != -1 and posf < len(merged_lines_all):
    begin_cite = merged_lines_all.find("\\cite{", posf)
    posf = begin_cite + 1
    end_cite = merged_lines_all.find("}", posf)
    pos_o_cite.append((begin_cite, end_cite))
    find_cite = merged_lines_all.find("\\cite{", posf)
for k in keys_cited:
    if k[1] not in merged_lines_all:
        errs += 1
        errs_set.add(k[1])
    else:
        posc = 0
        find_ref = merged_lines_all.find(k[1], posc)
        pos_ref = []
        while find_ref != -1 and posc < len(merged_lines_all):
            begin_ref = merged_lines_all.find(k[1], posc)
            pos_ref.append(begin_ref)
            posc = begin_ref + 1
            find_ref = merged_lines_all.find(k[1], posc)
        for pr in pos_ref:
            is_in_cite = False
            for pc in pos_o_cite:
                if pr > pc[0] and pr < pc[1]:
                    is_in_cite = True
                    break
            if is_in_cite:
                break
        if is_in_cite:
            pos_k = merged_lines_all.find(k[1])
            loc_of_keys[pos_k] = get_begin_end(merged_lines_all_bibliography, k[0], "}")
            nk_of_keys[pos_k] = k[1]
            ks.append(pos_k)
merged_lines_no_cite_new = ""
for k in sorted(ks):
    merged_lines_no_cite_new += loc_of_keys[k] + "\n\n"
merged_lines_no_misc_new = ""
for k in sorted(ks):
    if "@misc" not in loc_of_keys[k]:
        merged_lines_no_misc_new += loc_of_keys[k] + "\n\n"
print(errs, len(ks))
print(errs_set)
file_bibliography_new = open(dir + "bibliography_short.bib", "w", encoding="UTF8")
file_bibliography_new.write(merged_lines_no_cite_new.replace("author = {}", "author = {Developers, R}").replace("year = {}", "year = {2024}").replace("year={}", "year={2024}"))
file_bibliography_new.close()
file_bibliography_new_no_misc = open(dir + "bibliography_short_no_misc.bib", "w", encoding="UTF8")
file_bibliography_new_no_misc.write(merged_lines_no_misc_new.replace("author = {}", "author = {Developers, R}").replace("year = {}", "year = {2024}").replace("year={}", "year={2024}"))
file_bibliography_new_no_misc.close()
start_bib = "\\bibliography{sn-bibliography}% common bib file"
new_start_bib = "\\begin{thebibliography}{"
new_start_bibliography = "\\section{Bibliography}\n%\label{sec:Bibliography}\n"
for ix_zero in range(len(str(len(ks)))):
    new_start_bib += "0"
new_start_bib += "}\n"
end_bib = "%%\\input sn-article.bbl"
new_end_bib = "\\end{thebibliography}"
new_end_bibliography = ""
file_merged_refs_all_bibitem_old = open(dir + "refs_bibitem.txt", "r", encoding="UTF8")
linesbibitem = file_merged_refs_all_bibitem_old.readlines()
file_merged_refs_all_bibitem_old.close()
merged_refs_all_bibitem_original = ""
for l in linesbibitem:
    merged_refs_all_bibitem_original += l
merged_refs_all_bibitem = merged_refs_all_bibitem_original
ix = 0
k_of_keys = dict()
for k in sorted(ks):
    ix += 1
    k_of_keys[nk_of_keys[k]] = ix
import os
namesall = os.listdir()
names = []
file_chicago = open(dir + "chicago.txt", "r", encoding="UTF8")
clines = file_chicago.readlines()[0][1:-1].split("; ")
clines_fix = []
for c in clines:
    letter_replace = {"ä": "a", "è": "e", "æbø": "aebo", "ö": "o", "ć": "c"}
    chicago_use_new = c.lower().replace("&", ",").replace(", et al.", "").replace("et al.", "")
    for l in letter_replace:
        chicago_use_new = chicago_use_new.replace(l, letter_replace[l])
    newline_split = chicago_use_new
    newline_split = chicago_use_new.split(", ")
    c_no_year = c
    for y in range(1899, 2025):
        c_no_year = c_no_year.replace(", " + str(y) + "a", "")
        c_no_year = c_no_year.replace(", " + str(y) + "b", "")
        c_no_year = c_no_year.replace(", " + str(y), "")
    new_dic = {"authors": [], "years": [], "original": c_no_year}
    for part in newline_split:
        if part[0] == "2" or part[0] == "1":
            new_dic["years"].append(part.strip())
        else:
            new_dic["authors"].append(part.split(". ")[-1].strip())
    clines_fix.append(new_dic)
file_chicago.close()
find_match_chicago = dict()
new_key_order = dict()
for chicago_use in clines_fix:
    for y in chicago_use["years"]:
        found_matches_author = dict()
        for a in chicago_use["authors"]:
            found_matches_author[a] = set()
        found_matches_author_any = set()
        found_matches_year_text = set()
        found_matches_author_text = set()
        for k in sorted(ks):
                for a in chicago_use["authors"]:
                    if a in nk_of_keys[k].lower():
                        found_matches_author[a].add(nk_of_keys[k])
                        found_matches_author_any.add(nk_of_keys[k])
                    if a in loc_of_keys[k].lower():
                        found_matches_author_text.add(nk_of_keys[k])
                if y[:4] in loc_of_keys[k].lower():
                    found_matches_year_text.add(nk_of_keys[k])
        found_bib = set()
        for f in found_matches_author_text:
            if f in found_matches_year_text:
                found_bib.add(f)
        filtered_bib_old = set()
        if len(found_bib) > 1:
            filtered_bib_old = found_bib
            filtered_bib = set()
            for f in found_bib:
                if f in found_matches_author_any:
                    filtered_bib.add(f)
            found_bib = filtered_bib
        if len(found_bib) > 1:
            filtered_bib_old = found_bib
            filtered_bib = set()
            for f in found_bib:
                found_authors = True
                for a in chicago_use["authors"]:
                    if f not in found_matches_author[a]:
                        found_authors = False
                        break
                if found_authors:
                    filtered_bib.add(f)
            found_bib = filtered_bib
        if len(found_bib) != 1:
            print(chicago_use["authors"], y[:4])
            print(found_bib, filtered_bib_old)
            ix_a = 0
            letters_use = ["a", "b", "c", "d", "e"]
            for f in sorted(list(filtered_bib_old)):
                if f not in new_key_order:
                    new_key_order[f] = chicago_use["original"] + ", " + str(y[:4]) + letters_use[ix_a]
                ix_a += 1
        else:
            new_key_order[list(found_bib)[0]] = chicago_use["original"] + ", " + str(y[:4])
for k in new_key_order:
    print(k, new_key_order[k])
for n in namesall:
    if ".tex" in n:
        names.append(n.replace(".tex", ""))
for name in names:
    if "_new_bib" in name:
        continue
    if "_no_eqn" in name:
        continue
    if "_new_chicago" in name:
        continue
    file_fn_old = open(dir + name + ".tex", "r", encoding="UTF8")
    all_lines_fn = file_fn_old.readlines()
    file_fn_old.close()
    merged_lines_all_fn = ""
    for l in all_lines_fn:
        merged_lines_all_fn += l
    merged_lines_all_fn = merged_lines_all_fn.replace(start_bib, new_start_bib + merged_refs_all_bibitem + "\n").replace(end_bib, new_end_bib)
    file_fn = open(dir + name + "_new_bib.tex", "w", encoding="UTF8")
    file_fn.write(merged_lines_all_fn)
    file_fn.close()
    from subprocess import call
    list_subproc = ["pandoc", "-s", "-o", name + "_new_bib.docx", name + "_new_bib.tex"]
    call(list_subproc)
for name in names:
    if "_new_bib" in name:
        continue
    if "_no_eqn" in name:
        continue
    if "_new_chicago" in name:
        continue
    file_fn_old = open(dir + name + ".tex", "r", encoding="UTF8")
    all_lines_fn = file_fn_old.readlines()
    file_fn_old.close()
    merged_lines_all_fn = ""
    for l in all_lines_fn:
        merged_lines_all_fn += l
    merged_lines_all_fn = add_citation(merged_lines_all_fn, k_of_keys, "[", "]")
    merged_lines_all_fn = merged_lines_all_fn.replace(start_bib, new_start_bibliography + merged_refs_all.replace("\n", "\n\n")).replace(end_bib, new_end_bibliography)
    file_fn = open(dir + name + "_new_bibliography.tex", "w", encoding="UTF8")
    file_fn.write(merged_lines_all_fn)
    file_fn.close()
    print(dir + name + "_new_bibliography.tex")
    from subprocess import call
    list_subproc = ["pandoc", "-s", "-o", name + "_new_bibliography.docx", name + "_new_bibliography.tex"]
    call(list_subproc)
for name in names:
    if "_new_bib" in name:
        continue
    if "_no_eqn" in name:
        continue
    if "_new_chicago" in name:
        continue
    file_fn_old = open(dir + name + ".tex", "r", encoding="UTF8")
    all_lines_fn = file_fn_old.readlines()
    file_fn_old.close()
    merged_lines_all_fn = ""
    for l in all_lines_fn:
        merged_lines_all_fn += l
    merged_lines_all_fn = add_citation(merged_lines_all_fn, new_key_order, "(", ")")
    merged_lines_all_fn = merged_lines_all_fn.replace(start_bib, new_start_bibliography + merged_refs_all.replace("\n", "\n\n")).replace(end_bib, new_end_bibliography)
    file_fn = open(dir + name + "_new_chicago.tex", "w", encoding="UTF8")
    file_fn.write(merged_lines_all_fn)
    file_fn.close()
    print(dir + name + "_new_chicago.tex")
    from subprocess import call
    list_subproc = ["pandoc", "-s", "-o", name + "_new_chicago.docx", name + "_new_chicago.tex"]
    call(list_subproc)
for name in names:
    if "_no_eqn" in name:
        continue
    file_fn_old = open(dir + name + ".tex", "r", encoding="UTF8")
    all_lines_fn = file_fn_old.readlines()
    file_fn_old.close()
    merged_lines_all_fn = ""
    for l in all_lines_fn:
        merged_lines_all_fn += l
    for n in range(merged_lines_all_fn.count("\\label{eqn:")):
        merged_lines_all_fn = merged_lines_all_fn.replace("\\label{eqn:" + str(n + 1) + "}", "\\quad\\left(" + str(n + 1) + "\\right)")
        merged_lines_all_fn = merged_lines_all_fn.replace("~\\ref{eqn:" + str(n + 1) + "}", "~" + str(n + 1))
    file_fn = open(dir + name + "_no_eqn.tex", "w", encoding="UTF8")
    file_fn.write(merged_lines_all_fn)
    file_fn.close()
    from subprocess import call
    list_subproc = ["pandoc", "-s", "-o", name + "_no_eqn.docx", name + "_no_eqn.tex"]
    call(list_subproc)