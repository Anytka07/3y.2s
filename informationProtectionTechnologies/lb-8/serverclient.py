import socket

# Створення файлу з паролями 
with open('security_token.txt', 'w') as file:
    username = input("Enter username: ")
    password = input("Enter password: ")
    file.write(f"{username}|{password}\n")


# Створюється TCP-сокет, який прослуховує з'єднання
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 12354))
server_socket.listen(1)

print("Server is listening...")

# Перевірка паролю
def verify_password(token_data, username, password):
    stored_username, stored_password = token_data.split('|')
    if username == stored_username:
        return password == stored_password.strip()  # Видаляємо символ нового рядка з кінця рядка
    return False

# Отримання даних з файлу на токені безпеки
with open('security_token.txt', 'r') as file:
    token_data = file.readline()  # Читаємо лише перший рядок файлу

while True: 
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} has been established.")

    # Отримання даних з клієнта
    data = client_socket.recv(1024)
    username, password = data.decode().split('|')

    # Перевірка паролю
    if verify_password(token_data, username, password):
        client_socket.send(b"Authentication successful.")
    else:
        client_socket.send(b"Authentication failed.")

    client_socket.close()
