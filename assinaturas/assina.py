
nome = 'João Carlos Bueno Masso'
cargo = 'Analista de Sistemas'
fone = '61 3462-5038'
cel = '61 9 8224-6622'
email = 'bueno@1linha.com.br'



assina = open('./assina.html', 'r', encoding='utf-8').read().format(nome=nome,
                                                                    cargo=cargo,
                                                                    fone=fone,
                                                                    cel=cel,
                                                                    email=email)

print(assina)
