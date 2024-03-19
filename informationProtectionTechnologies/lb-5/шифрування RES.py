import math

# Визначення українського алфавіту
ukrainian_alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ '

# Визначення таблиці підстановки
substitution_table = {
    'А': '00', 'Б': '01', 'В': '02', 'Г': '03', 'Ґ': '04',
    'Д': '05', 'Е': '06', 'Є': '07', 'Ж': '08', 'З': '09',
    'И': '10', 'І': '11', 'Ї': '12', 'Й': '13', 'К': '14',
    'Л': '15', 'М': '16', 'Н': '17', 'О': '18', 'П': '19',
    'Р': '20', 'С': '21', 'Т': '22', 'У': '23', 'Ф': '24',
    'Х': '25', 'Ц': '26', 'Ч': '27', 'Ш': '28', 'Щ': '29',
    'Ь': '30', 'Ю': '31', 'Я': '32', ' ': '33'
}

substitution_table_inv = {value: key for key, value in substitution_table.items()}

# Вибираємо два прості числа
p = 3
q = 11

# Обчислюємо n
n = p * q
print("n =", n)

# Обчислюємо функцію Ейлера
phi = (p - 1) * (q - 1)

# Вибираємо е
e = 7
while 1 < e < phi:
    if math.gcd(e, phi) == 1:
        break
    else:
        e += 1

print("e =", e)

# Обчислюємо d
d = 3

# Зчитуємо відкрите повідомлення з файлу
with open('open_message.txt', 'r', encoding='utf-8') as file:
    plaintext = file.read().strip()

# Перетворюємо відкрите повідомлення в верхній регістр
plaintext = plaintext.upper()

# Шифруємо повідомлення за допомогою таблиці підстановки
encrypted_message = ' '.join(substitution_table[char] for char in plaintext)
print(f'Оригінальне повідомлення: {plaintext}')
print(f'Зашифроване повідомлення: {encrypted_message}')

# Перетворюємо зашифроване повідомлення в цілі числа
encrypted_numbers = [int(num) for num in encrypted_message.split()]

# Шифрування
encrypted = [pow(num, e, n) for num in encrypted_numbers]

# Обчислюємо хеш
hash_value = sum(map(int, encrypted_message.split())) % 34
print(f'Хеш: {hash_value}')

# Розшифрування
decrypted = [pow(num, d, n) for num in encrypted]
print(f'Розшифровані числа: {decrypted}')

# Відображаємо розшифровані числа у вихідний діапазон (0-33)
decrypted = [num % 34 for num in decrypted]

# Перетворюємо розшифровані числа назад у символи
decrypted_message = ''.join(substitution_table_inv[str(num).zfill(2)] for num in decrypted)
print(f'Розшифроване повідомлення: {decrypted_message}')

# Обчислюємо хеш розшифрованого повідомлення
decrypted_hash = sum(decrypted) % 34
print(f'Хеш розшифрованого повідомлення: {decrypted_hash}')

# Перевіряємо цілісність повідомлення
if hash_value == decrypted_hash:
    print("Хеші вихідного та розшифрованого повідомлень одинакові.")
else:
    print("Хеші не збігаються. Можливо, повідомлення було не правильне.")
