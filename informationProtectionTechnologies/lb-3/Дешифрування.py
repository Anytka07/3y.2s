def decrypt(text, key):
    decrypted_text = ""
    for char in text:
        if char.isalpha():  # перевіряємо, чи символ є буквою
            shift = (ord(char.lower()) - ord('a') - key) % 26
            decrypted_char = chr(shift + ord('a'))
            decrypted_text += decrypted_char.upper() if char.isupper() else decrypted_char
        else:
            decrypted_text += char
    return decrypted_text

def main():
    input_file_name = input("Введіть ім'я файлу з шифрограмою: ")
    key = int(input("Введіть ключ для розшифрування: "))

    try:
        with open(input_file_name, 'r') as input_file:
            ciphertext = input_file.read()
            decrypted_text = decrypt(ciphertext, key)
            print("Розшифрований текст:")
            print(decrypted_text)
    except FileNotFoundError:
        print("Помилка: файл не знайдено.")

if __name__ == "__main__":
    main()
