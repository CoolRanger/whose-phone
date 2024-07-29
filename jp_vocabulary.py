import random

#word[0]單字 word[1]假名 word[2]意思 word[3~?]例句

"""
程序
1.新增使用者(使用者註冊)
2.使用者添加單詞 slash 3參數(單字、假名、意思)
3.詢問是否需要添加例句(word[3~未知])
"""
user = {}

def initialize():
    """
    初始化函數，讀取文件內容並構建用戶字典。
    必須在其他操作之前運行。
    """
    user.clear()
    name=""

    with open('jp_vocabulary.txt', 'r', encoding='utf-8') as file:
        content = file.readlines()

    for line in content:
        line = line.strip()  # 去除每行的換行符
        if line.startswith('$'):
            name = line[1:]  # 去掉前面的 $
            if name not in user:
                user[name] = []
        else:
            word = list(line.split('*'))
            user[name].append(word)

def rewrite_database():
    new_content = ""
    for user_name in user:
        new_content += f'${user_name}\n'
        for word in user[user_name]:
            new_content += f'{'*'.join(word)}\n'
    with open("jp_vocabulary.txt", 'w', encoding='utf-8') as file:
        file.write(new_content)
    initialize()

def check_info():
    print("以下是目前資料庫內容\n請確認資料完整性")
    print(user)

def add_user(user_name):
    if user_name in user:
        return 0
    new_content = f'${user_name}'
    with open("jp_vocabulary.txt", 'a', encoding='utf-8') as file:
        file.write(new_content)
    initialize()
    return 1

def add_voc(user_name, word): #word is list (3參數)
    if user_name not in user:
        return "查無該使用者資料"
    user[user_name].append(word)
    rewrite_database()
    return f"已成功新增{word[0]}至{user_name}的資料庫中"

def del_voc(user_name, word): #word is str
    if user_name not in user:
        return "查無該使用者資料"
    for i in user[user_name]:
        if i[0] == word:
            user[user_name].remove(i)
            rewrite_database()
            return f"已從{user_name}的資料庫中刪除{word}"
    return "查無資料"

def add_sentence(user_name, word, sentence):
    if user_name not in user:
        return "查無該使用者資料"
    for i in user[user_name]:
        if i[0] == word:
            i.append(sentence)
            rewrite_database()
            return f"已新增該例句至{user_name}資料庫中的{word}中"
    return "查無資料"

def inquire_voc_num(user_name):
    if user_name not in user:
        return "查無該使用者資料"
    return f"{user_name}有{len(user[user_name])}個單字在資料庫中"


def inquire_voc_info(user_name, word): 
    if user_name not in user:
        return "查無該使用者資料"
    r = ''
    for i in user[user_name]:
        if i[0] == word:
            r = f"單字:{i[0]}\n假名:{i[1]}\n意思:{i[2]}"
        for j in range(3, len(i)):
            r += f'\n例句{j-2}:{i[j]}'
        return r
    return "查無資料"


def voc_test(user_name):
    if user_name not in user:
        return "查無該使用者資料"
    word = random.choice(user[user_name])
    return f"隨機從{user_name}的資料庫中抽取單字\n{word[0]}"

def voc_list(user_name):
    if user_name not in user:
        return "查無該使用者資料"
    respond = f"以下是{user_name}的單字\n"
    for word in user[user_name]:
        respond += word[0]+'\n'
    return respond

initialize()
voc_list("ranger0904")