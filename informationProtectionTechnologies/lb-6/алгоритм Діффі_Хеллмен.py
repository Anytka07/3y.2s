import random

# Функція перевірки на просте число
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Функція генерації простого числа
def generate_prime(min_value):
    while True:
        p = random.randint(min_value, 10*min_value)
        if is_prime(p):
            return p

# Функція пошуку первісного кореня за модулем p
def primitive_root(p):
    for a in range(2, p):
        if pow(a, p - 1, p) == 1:
            return a
    return None

# Основна функція алгоритму Діффі-Хеллмана
def diffie_hellman_key_exchange():
    # Крок 1: Обрання простого числа p та первісного кореня a
    p = generate_prime(1000)  # Мінімум 4-значне просте число
    a = primitive_root(p)
    
    if a is None:
        print("Не вдалося знайти первісний корінь")
        return
    
    print("Обране просте число p:", p)
    print("Первісний корінь a:", a)
    
    # Крок 2: Генерація приватних ключів кожною зі сторін
    private_key_A = random.randint(2, p - 1)  # Приватний ключ сторони A
    private_key_B = random.randint(2, p - 1)  # Приватний ключ сторони B
    print("\nПриватний ключ А:", private_key_A)
    print("Приватний ключ B:",private_key_B)
    
    # Крок 3: Обчислення відкритих ключів та їх обмін
    public_key_A = pow(a, private_key_A, p)  # Відкритий ключ сторони A
    public_key_B = pow(a, private_key_B, p)  # Відкритий ключ сторони B
    print("\nПублічний ключ А:", public_key_A)
    print("Публічний ключ B:",public_key_B)
    
    # Крок 4: Обчислення спільного секретного ключа кожною стороною
    shared_key_A = pow(public_key_B, private_key_A, p)  # Спільний ключ сторони A
    shared_key_B = pow(public_key_A, private_key_B, p)  # Спільний ключ сторони B
    
    # Вивід результатів обміну ключами
    print("\nСторона A обчислила спільний ключ:", shared_key_A)
    print("Сторона B обчислила спільний ключ:", shared_key_B)
    
    # Крок 5: Порівняння обчислених спільних ключів
    if shared_key_A == shared_key_B:
        print("Спільні ключі збігаються. Обмін ключами успішний.")
    else:
        print("Спільні ключі не збігаються. Обмін ключами неуспішний.")

# Виклик функції для обміну ключами
diffie_hellman_key_exchange()
