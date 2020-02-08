nZero = True
# for j in range(0, 1001):
for j in range(2, 3):
    print('\n\n\\section{Base ',j ,'}\n\n')
    for i in range(0, 100001):
        print(i)
        k = pow(j, i)
        for m in str(k):
            if m=='0':
                nZero = False;
                break;
        if (nZero==True):
            print('$', j, '^{', i, '} = ', k, '$\\\\')
        nZero = True
