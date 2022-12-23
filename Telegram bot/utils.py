def generate_text_document(data, file):
    f = open(file, 'w', encoding='utf8')
    print('file was created')
    print(f"ФИО: {data['name']}", file=f)
    print(f"Пол: {data['gender']}", file=f)
    print(f"Возраст: {data['age']}", file=f)
    print(f"Род деятельности на данный момент: {data['role']}", file=f)
    print(f"Желаемая профессия: {data['profession']}", file=f)
    return f


def translate(string:str):
    a = {'а': 'a', 'б':'b', 'в':'v', 'г':'g', 'д':'d', 'е':'e', 'ё':'e', 'ж':'zh', 'з':'z', 'и':'i', 'к':'k', 'л':'l',
    'м':'m', 'н':'n', 'о':'o','п':'p', 'р':'r','с':'s', 'т': 't', 'у':'u', 'ф': 'f', 'х':'kh', 'ц':'ts', 'ч': 'ch', 'ш':'sh', 'щ':'sh', 'ъ':'',
    'ь':'', 'э': 'e', 'ю':'u', 'я':'ya', 'й':'y'}
    for i in a:
        string = string.replace(i, a[i])
    return string