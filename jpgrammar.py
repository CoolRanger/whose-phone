N3 = {}
N2 = {}
N1 = {}
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
        N3[title] = link
    f.close
print(N3)