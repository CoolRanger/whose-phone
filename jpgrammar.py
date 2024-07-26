
N3 = {}
N2 = {}
N1 = {}
N123 = {}
f_index = 0
s_index = 0

def title_process(title):
    idx = 0
    for i in range(len(title)):
        if title[i] !=' ':
            idx = i
            break
    title = title[idx:]

def classify(title, link):
    N123[title] = link
    if title[2] == '３':
        N3[title] = link
    elif title[2] == '２':
        N2[title] = link
    elif title[2] == '１':
        N1[title] = link

def file_process():
    with open('japanses.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            for i in range(len(line)):
                if line[i]=='【':
                    f_index = i
                elif line[i]=='h':
                    s_index = i
                    break
            title = line[f_index:s_index-1]
            title_process(title)
            link = line[s_index:]
            classify(title, link)
        f.close

file_process()
