import le_excel
from PIL import Image, ImageDraw, ImageFont

dados = le_excel.le_excel()

# nome = 'Robério Barreto Filho'
# cargo = 'Coordenador Executivo'
# fone = '61 3462-5048'
# cel = '61 9 9649-9352'
# email = 'roberiofilho@1linha.com.br'

site = 'www.1linha.com.br'
empr = 'Primeira Linha Comercial de Rolamentos'

icon_peq = 40
pos_ipeq = 180

font1 = ImageFont.truetype("./fontes/verdanab.ttf", 28)
font2 = ImageFont.truetype("verdana.ttf", 23)

ifone = Image.open('./imagens/b_fone-1.jpg').convert("RGBA").resize((icon_peq,icon_peq))
iwhatsapp = Image.open('./imagens/b_whatsapp-1.jpg').convert("RGBA").resize((icon_peq,icon_peq))
iemail = Image.open('./imagens/b_email-1.jpg').convert("RGBA").resize((icon_peq,icon_peq))
iweb = Image.open('./imagens/b_web-1.jpg').convert("RGBA").resize((icon_peq,icon_peq))

for dado in dados:
    nome = dado['NOME']
    cargo = dado['CARGO ']
    fone = dado['RM']
    cel = dado['CELULAR ']
    email =dado['E-MAIL ']

    print(nome)

    n = "-".join(nome.split(' '))
    print(n)

    base = Image.open('./imagens/base-canva-1.png').convert("RGBA")

    base.paste(ifone, (300, pos_ipeq), ifone.convert("RGBA"))
    base.paste(iwhatsapp, (300, pos_ipeq + (1 * icon_peq) + 2), iwhatsapp.convert("RGBA"))
    base.paste(iemail, (300, pos_ipeq + (2 * icon_peq) + 2), iemail.convert("RGBA"))
    base.paste(iweb, (300, pos_ipeq + (3 * icon_peq) + 2), iweb.convert("RGBA"))

    draw = ImageDraw.Draw(base)
    draw.text((300, 100), text=nome, fill="#000", font=font1)
    draw.text((300, 130), text=cargo, fill="#898989", font=font2)
    draw.text((350, pos_ipeq + 4), text=fone, fill="#898989", font=font2)
    draw.text((350, pos_ipeq + (1 * icon_peq) + 4), text=cel, fill="#898989", font=font2)
    draw.text((350, pos_ipeq + (2 * icon_peq) + 4), text=email, fill="#898989", font=font2)
    draw.text((350, pos_ipeq + (3 * icon_peq) + 4), text=site, fill="#898989", font=font2)
    draw.text((350, pos_ipeq + (4 * icon_peq) + 4), text=empr, fill="#898989", font=font2)

    base.save('./' + n + '.png')