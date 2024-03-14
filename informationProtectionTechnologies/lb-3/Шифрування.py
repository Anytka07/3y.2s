def encrypt(text, a, b, m): # функція шифрування
    encrypted_text = ""
    for char in text:
        if char.isalpha():  # Перевіряємо, чи символ є буквою
            if char.isupper():  # Якщо символ велика літера
                char_code = ord(char) - ord('A')  # Перетворюємо літеру в числове значення (0-25)
                encrypted_char = chr(((a * char_code + b) % m) + ord('A'))  # Шифруємо літеру
            else:  # Якщо символ маленька літера
                char_code = ord(char) - ord('a')  # Перетворюємо літеру в числове значення (0-25)
                encrypted_char = chr(((a * char_code + b) % m) + ord('a'))  # Шифруємо літеру
        else:  # Якщо символ не є буквою
            encrypted_char = char  # Залишаємо символ без змін
        encrypted_text += encrypted_char  # Додаємо зашифрований символ до результуючого тексту
    return encrypted_text


def main():
    input_file_name = input("Введіть ім'я вхідного файлу: ")
    output_file_name = input("Введіть ім'я вихідного файлу: ")
    a = int(input("Введіть множник a: "))  # Введення множника для шифрування
    b = int(input("Введіть зсув b: "))  # Введення зсуву для шифрування
    m = 26  # Розмір алфавіту (модуль)

    try:
        with open(input_file_name, 'r') as input_file:
            plaintext = input_file.read()
            encrypted_text = encrypt(plaintext, a, b, m)  # Шифрування тексту
            with open(output_file_name, 'w') as output_file:
                output_file.write(encrypted_text)  # Збереження зашифрованого тексту у файл
            print("Текст успішно зашифровано та збережено у файлі", output_file_name)
    except FileNotFoundError:
        print("Помилка: файл не знайдено.")

if __name__ == "__main__":
    main()
