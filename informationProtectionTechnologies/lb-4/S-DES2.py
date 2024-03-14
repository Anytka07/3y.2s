# Підстановкові таблиці
s_box_1 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

s_box_2 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

# Початкова перестановка
ip = [1, 5, 2, 0, 3, 7, 4, 6]

# Кінцева перестановка
fp = [3, 0, 2, 4, 6, 1, 7, 5]

# Генерація ключів
def generate_keys(key):
    keys = []
    # Початкова перестановка ключа
    key_permuted = [key[i] for i in [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]]
    # Розділення ключа на дві частини
    left_half = key_permuted[:5]
    right_half = key_permuted[5:]
    # Застосування циклічних зсувів вліво
    for i in range(2):
        left_half = left_half[1:] + [left_half[0]]
        right_half = right_half[1:] + [right_half[0]]
        combined_key = left_half + right_half
        # Застосування перестановки P8
        round_key = [combined_key[i] for i in [5, 2, 6, 3, 7, 4, 9, 8]]
        keys.append(round_key)
    return keys

# Початкова перестановка
def initial_permutation(plaintext):
    permuted_text = [plaintext[i] for i in ip]
    return permuted_text

# Кінцева перестановка
def final_permutation(ciphertext):
    permuted_text = [ciphertext[i] for i in fp]
    return permuted_text

# Підстановка за допомогою S-Box
def s_box_substitution(text, s_box):
    row = int(text[0] + text[3], 2)
    col = int(text[1:3], 2)
    return format(s_box[row][col], '02b')

# Функція раунду S-DES
def round_function(text, key):
    # Розширена перестановка
    expanded_text = [text[i] for i in [3, 0, 1, 2, 1, 2, 3, 0]]
    # Виконання операції XOR між розширеним текстом і ключем
    xor_result = [int(expanded_text[i]) ^ int(key[i]) for i in range(8)]
    # Заміна за допомогою S-Box і отримання вихідних значень
    s_box_output = s_box_substitution(''.join(map(str, xor_result[:4])), s_box_1) + s_box_substitution(''.join(map(str, xor_result[4:])), s_box_2)
    # Перестановка P4
    permuted_text = [s_box_output[i] for i in [1, 3, 2, 0]]
    return permuted_text

# Функція шифрування тексту
def encrypt_text(plaintext, key):
    encrypted_text = ""
    for char in plaintext:
        # Конвертація кожного символу в двійковий формат
        binary_char = format(ord(char), '08b')
        # Шифрування кожного символу
        encrypted_char = encrypt(binary_char, key)
        # Додавання зашифрованого символу до загального шифротексту
        encrypted_text += ''.join(map(str, encrypted_char))
    return encrypted_text

# Функція розшифрування тексту
def decrypt_text(ciphertext, key):
    decrypted_text = ""
    for i in range(0, len(ciphertext), 8):
        # Розбиття шифротексту на 8-бітні блоки
        binary_char = ciphertext[i:i+8]
        # Розшифрування кожного блоку
        decrypted_char = decrypt(binary_char, key)
        # Додавання розшифрованого символу до загального тексту
        decrypted_text += chr(int(''.join(map(str, decrypted_char)), 2))
    return decrypted_text

# Функція шифрування
def encrypt(plaintext, key):
    keys = generate_keys(key)
    text = initial_permutation(plaintext)
    left_half, right_half = text[:4], text[4:]
    for i in range(2):
        temp = right_half
        # Виконання функції раунду для правої половини тексту
        right_half = [int(left_half[j]) ^ int(round_function(right_half, keys[i])[j]) for j in range(4)]
        left_half = temp
    # Після останнього раунду, об'єднання лівої та правої половин тексту та кінцева перестановка
    ciphertext = final_permutation(right_half + left_half)
    return ciphertext

# Функція розшифрування
def decrypt(ciphertext, key):
    keys = generate_keys(key)
    text = initial_permutation(ciphertext)
    left_half, right_half = text[:4], text[4:]
    for i in range(2):
        temp = right_half
        # Виконання функції раунду для правої половини тексту
        right_half = [int(left_half[j]) ^ int(round_function(right_half, keys[1 - i])[j]) for j in range(4)]
        left_half = temp
    # Після останнього раунду, об'єднання лівої та правої половин тексту та кінцева перестановка
    plaintext = final_permutation(right_half + left_half)
    return plaintext

# Використання функції розшифрування для тексту
if __name__ == "__main__":
    plaintext = "Kik"  # Вхідний текст
    key = "1100101001"  # 10-бітний ключ
    print("Оригінальний текст:", plaintext)
    print("Оригінальний ключ:", key)

    encrypted_text = encrypt_text(plaintext, key)
    print("Зашифрований текст:", encrypted_text)

    decrypted_text = decrypt_text(encrypted_text, key)
    print("Розшифрований текст:", decrypted_text)
