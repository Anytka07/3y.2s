import socket

# Введення даних користувача
username = input("Enter username: ")
password = input("Enter password: ")

# Підключення до серверу
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 12354))

# Відправка даних на сервер
client_socket.send(f"{username}|{password}".encode())

# Отримання результату аутентифікації
response = client_socket.recv(1024)
print(response.decode())

client_socket.close()