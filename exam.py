import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def encrypt_file(input_file_path, output_file_path, key):

    # Генеруємо випадковий 12-байтовий вектор ініціалізації (IV)
    iv = os.urandom(12)

    # Ініціюємо шифр AES-GCM
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=default_backend()
    ).encryptor()

    # Зчитуємо вміст вхідного файлу
    with open(input_file_path, 'rb') as input_file:
        plaintext = input_file.read()

    # Шифруємо текст
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    # Отримуємо тег аутентифікації
    tag = encryptor.tag

    # Записуємо IV, шифротекст і тег у двійковий файл
    with open(output_file_path, 'wb') as output_file:
        output_file.write(iv)  # Записуємо IV (12 байтів)
        output_file.write(tag)  # Записуємо тег (16 байтів)
        output_file.write(ciphertext)  # Записуємо шифротекст

    print(f"Файл '{input_file_path}' успішно зашифровано та збережено у '{output_file_path}'")


def main():
    # 32-байтовий (256-бітний) ключ AES (має бути надійно згенерований)
    key = os.urandom(32)  # У реальній програмі краще зберігати ключ у захищеному місці

    # Імена файлів
    input_file_path = '1test.txt'  # Вхідний текстовий файл
    output_file_path = 'encrypted.bin'  # Вихідний файл з шифротекстом

    # Виконуємо шифрування
    encrypt_file(input_file_path, output_file_path, key)

    # Збереження ключа для розшифровки (це потрібно робити обережно)
    with open('aes_key.bin', 'wb') as key_file:
        key_file.write(key)
    print(f"Ключ AES збережено у файлі 'aes_key.bin'")


if __name__ == "__main__":
    main()
