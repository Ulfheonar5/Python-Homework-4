import sqlite3

conn = sqlite3.connect('metinler.db')
c = conn.cursor()

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    onceki_satir = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        mevcut_satir = [i + 1]
        for j, c2 in enumerate(s2):
            karakter_ekle = onceki_satir[j + 1] + 1
            karakter_sil = mevcut_satir[j] + 1
            karakter_degistir = onceki_satir[j] + (c1 != c2)
            mevcut_satir.append(min(karakter_ekle, karakter_sil, karakter_degistir))
        onceki_satir = mevcut_satir

    return onceki_satir[-1]

while(True):
    selection=input("-----------------------------------------------------\n"
                    "Benzerlik ölçümü yapmak için(1),\nÇıkmak için(2):")
    if(selection=="2"):
        break
    else:
        metin1 = input("Lütfen birinci metni girin: ")
        metin2 = input("Lütfen ikinci metni girin: ")

        c.execute("CREATE TABLE IF NOT EXISTS metinler (id INTEGER PRIMARY KEY, metin TEXT)")
        c.execute("INSERT INTO metinler (metin) VALUES (?)", (metin1,))
        c.execute("INSERT INTO metinler (metin) VALUES (?)", (metin2,))
        conn.commit()

        mesafe = levenshtein(metin1, metin2)
        max_uzunluk = max(len(metin1), len(metin2))
        benzerlik_orani = (max_uzunluk - mesafe) / max_uzunluk * 100

        print(f"Metinler arasındaki benzerlik oranı: {benzerlik_orani:.2f}%")

        with open('benzerlik_durumu.txt', 'w') as file:
            file.write(f"Metinler arasındaki benzerlik oranı: {benzerlik_orani:.2f}%")

        conn.close()