def rttd_lttr(letter, key):
    if letter.isalpha():    
        num = ord(letter)
        if (num + key) > 122: 
            x = (num + key) - 122
            return chr(x + ord('a') - 1)
        else:
            return chr(num + key)
    else:
            return letter

def dcrpt(word, key):
    new_word = ""
    for letter in word:
        new_letter = rttd_lttr(letter, key)
        new_word += new_letter

    return new_word

print(dcrpt("Adgcv, jmbpgcj z azgdxdyvyz kjm npvn xjilpdnovn! Kvmvwzin! Oz Vhj <3", 5))

print(dcrpt("jwmdbvyv kvvvvvvd!!!! oz vhj hpdoj hpdoj hpdoj <3 qjp nziodm nvpyvyzn", 5))