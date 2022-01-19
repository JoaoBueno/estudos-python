import sys
from funcoes.isEmail import isEmail

lista = [
    '#bueno@1linha.com.br',
    'bueno=joao@1linha.com.br',
    'presidencia@sindivaregista.org.b',
    'cso.brasilia@bb.com.br',
    'eliveltonmendesdossantos@gmail.com',
    'rayssalovemae31@gmail.com',
    'NAO POSSUI E-MAIL',
    'fazendasoa@brasal.com.br',
    'fazenda_recreio@terra.com.br'
]


if __name__ == '__main__':
    for email in lista:
        if isEmail(email):
            print('{:40} - This is a valid e-mail address'.format(email))
        else:
            print('{:40} - This is not a valid e-mail address'.format(email))
