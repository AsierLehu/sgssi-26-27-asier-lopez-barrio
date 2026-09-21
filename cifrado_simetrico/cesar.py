from langdetect import detect, detect_langs


input = "Uunejvxb dw vdwmx wdnex jzdr, nw wdnbcaxb lxajixwnb"

letras_es = "abcdefghijklmnopqrstuvwxyz"

def cesar(input):
    for key in range(26): # iteramos sobre las 26 posibles claves
        output = ""
        for char in input: # iteramos sobre cada caracter del input
            char = char.lower()
            if char not in letras_es: # si el caracter no es una letra, lo añadimos al output y saltamos
                output += char
                continue
            output += letras_es[(letras_es.index(char) + key) % 26] # %26 para cuando es la ultima letra, se vuelve a empezar desde la primera
        try:
            if detect(output) == "es":
                return output
        except:
            continue

    return None

if __name__ == "__main__":
    print(cesar(input))