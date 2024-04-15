from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa


# Генеруємо пару ключів для RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()


# Функція для підпису файлу за допомогою приватного ключа
def sign_file(file_path, private_key):
    # Відкриваємо файл для зчитування вмісту
    with open(file_path, 'rb') as file:
        # Зчитуємо вміст файлу
        data = file.read()
        # Виводимо вміст файлу перед підписом
        print("Дані до підпису:")
        print(data)

    # Обчислюємо підпис для даних
    signature = private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Додаємо підпис до кінця файлу
    with open(file_path, 'ab') as file:
        file.write(signature)

# Функція для перевірки підпису файлу за допомогою публічного ключа
def verify_signature(file_path, public_key):
    # Відкриваємо файл для зчитування вмісту та підпису
    with open(file_path, 'rb') as file:
        data = file.read()

    # Виділяємо підпис з кінця файлу (припускаючи, що довжина підпису - 256 байт)
    signature = data[-256:]
    # Видаляємо підпис з даних
    data = data[:-256]

    try:
        # Перевіряємо підпис
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # Виводимо повідомлення про те, що підпис є валідним
        print("Digital signature is valid.")
    except:
        # Виводимо повідомлення про те, що підпис є невалідним
        print("Digital signature is invalid.")


file_path = 'message.txt'
text = b'Example data to be signed.'

# Підписуємо файл
sign_file(file_path, private_key)

# Перевіряємо підпис
verify_signature(file_path, public_key)

# Виводимо вміст файлу після перевірки підпису
print("Дані після перевірки підпису:")
with open(file_path, 'rb') as file:
    print(file.read())

# Виводимо підпис
print("Підпис:")
with open(file_path, 'rb') as file:
    signature = file.read()[-256:]  # Assuming signature length is 256 bytes
    print(signature)

# Перевіряємо підпис ще раз і виводимо результат
verify_signature(file_path, public_key)
