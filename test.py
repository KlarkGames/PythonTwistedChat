box = []

def Here():
    global box
    cat = input()
    if cat in box:
        print('Такой кот уже есть!')
        print (box)
    else:
        box.append(cat)
        print ('У нас есть новый кот!')
        print(box)

Here()
Here()
Here()