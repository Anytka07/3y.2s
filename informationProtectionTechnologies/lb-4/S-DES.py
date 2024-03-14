# Реалізація шифрування та дешифрування S-DES в Python

# Таблиця початкової перестановки
IP = [2, 6, 3, 1, 4, 8, 5, 7]
# Таблиця зворотної початкової перестановки
IP_INV = [4, 1, 3, 5, 7, 2, 8, 6]
# Таблиця розширення
EP = [4, 1, 2, 3, 2, 3, 4, 1]
# Таблиця перестановки P4
P4 = [2, 4, 3, 1]
# Таблиця перестановки P8
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
# Таблиця перестановки P10
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
# S-бокси
S0 = [[1, 0, 3, 2],
      [3, 2, 1, 0],
      [0, 2, 1, 3],
      [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3],
      [2, 0, 1, 3],
      [3, 0, 1, 0],
      [2, 1, 0, 3]]

# Виконати перестановку вхідних бітів згідно з вказаною таблицею перестановок
def permute(input_bits, permutation_table):
    return ''.join(input_bits[i - 1] for i in permutation_table)

# Здійснити лівий циклічний зсув бітів вхідних даних на вказану кількість позицій
def left_circular_shift(input_bits, n):
    return input_bits[n:] + input_bits[:n]

# Виконати підстановку S-бокса
def s_box_substitution(input_bits, s_box):
    row = int(input_bits[0] + input_bits[3], 2)
    col = int(input_bits[1:3], 2)
    return format(s_box[row][col], '02b')

# Згенерувати ключ для наступного раунду
def generate_round_key(key, round_number):
    key = left_circular_shift(key[:5], 1) + left_circular_shift(key[5:], 1)
    return permute(key, P8)

# Виконати початкову перестановку
def initial_permutation(plaintext):
    return permute(plaintext, IP)

# Виконати зворотню початкову перестановку
def inverse_initial_permutation(ciphertext):
    return permute(ciphertext, IP_INV)

# Виконати розширену перестановку
def expansion_permutation(input_bits):
    return permute(input_bits, EP)

# Виконати перестановку P4
def p4_permutation(input_bits):
    return permute(input_bits, P4)

# Виконати перестановку P8
def p8_permutation(input_bits):
    return permute(input_bits, P8)

# Виконати перестановку P10
def p10_permutation(input_bits):
    return permute(input_bits, P10)

# Зашифрувати вхідне повідомлення за допомогою S-DES
def sdes_encrypt(plaintext, key):
    plaintext = initial_permutation(plaintext)
    left_half = plaintext[:4]
    right_half = plaintext[4:]

    # Раунд 1
    key1 = generate_round_key(key, 1)
    expanded_right_half = expansion_permutation(right_half)
    xor_result = format(int(expanded_right_half, 2) ^ int(key1, 2), '08b')
    substituted_left_half = s_box_substitution(xor_result[:4], S0)
    substituted_right_half = s_box_substitution(xor_result[4:], S1)
    p4_result = p4_permutation(substituted_left_half + substituted_right_half)
    new_right_half = format(int(left_half, 2) ^ int(p4_result, 2), '04b')

    # Раунд 2
    key2 = generate_round_key(key, 2)
    expanded_new_right_half = expansion_permutation(new_right_half)
    xor_result = format(int(expanded_new_right_half, 2) ^ int(key2, 2), '08b')
    substituted_left_half = s_box_substitution(xor_result[:4], S0)
    substituted_right_half = s_box_substitution(xor_result[4:], S1)
    p4_result = p4_permutation(substituted_left_half + substituted_right_half)
    new_left_half = format(int(right_half, 2) ^ int(p4_result, 2), '04b')

    ciphertext = new_left_half + new_right_half
    return inverse_initial_permutation(ciphertext)

# Розшифрувати шифротекст за допомогою S-DES
def sdes_decrypt(ciphertext, key):
    ciphertext = initial_permutation(ciphertext)
    left_half = ciphertext[:4]
    right_half = ciphertext[4:]

    # Раунд 1
    key2 = generate_round_key(key, 2)
    expanded_right_half = expansion_permutation(right_half)
    xor_result = format(int(expanded_right_half, 2) ^ int(key2, 2), '08b')
    substituted_left_half = s_box_substitution(xor_result[:4], S0)
    substituted_right_half = s_box_substitution(xor_result[4:], S1)
    p4_result = p4_permutation(substituted_left_half + substituted_right_half)
    new_right_half = format(int(left_half, 2) ^ int(p4_result, 2), '04b')

    # Раунд 2
    key1 = generate_round_key(key, 1)
    expanded_new_right_half = expansion_permutation(new_right_half)
    xor_result = format(int(expanded_new_right_half, 2) ^ int(key1, 2), '08b')
    substituted_left_half = s_box_substitution(xor_result[:4], S0)
    substituted_right_half = s_box_substitution(xor_result[4:], S1)
    p4_result = p4_permutation(substituted_left_half + substituted_right_half)
    new_left_half = format(int(right_half, 2) ^ int(p4_result, 2), '04b')

    plaintext = new_left_half + new_right_half
    return inverse_initial_permutation(plaintext)

# Запустіть головну функцію для шифрування
def encrypt_main():
    # Задайте ваше словесне повідомлення
    message = "Helo"

    # Перетворіть повідомлення в біти
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Виведіть бітове представлення повідомлення
    print("Бітове представлення повідомлення:", binary_message)

    # Тепер зашифруйте бітове повідомлення
    key = '1010000010'  # Ваш ключ
    encrypted_message = sdes_encrypt(binary_message, key)

    # Виведіть зашифроване повідомлення
    print("Зашифроване повідомлення:", encrypted_message)

# Запустіть головну функцію для дешифрування
def decrypt_main():
    # Ваш зашифрований текст
    encrypted_message = "01101111"

    # Ваш ключ
    key = '1010000010'

    # Розшифрувати зашифрований текст
    decrypted_message = sdes_decrypt(encrypted_message, key)

    # Перевести біти в слова
    decrypted_text = ''.join(chr(int(decrypted_message[i:i+8], 2)) for i in range(0, len(decrypted_message), 8))

    # Виведення розшифрованого тексту
    print("Розшифрований текст:", decrypted_text)

# Запустіть головну функцію для шифрування
if __name__ == "__main__":
    encrypt_main()

# Запустіть головну функцію для дешифрування
#if __name__ == "__main__":
 #   decrypt_main()
