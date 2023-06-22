import requests
import time
import json
import os
import sys


def readText(filePath: str) -> str:
    """ Открывает текстовый файл и возвращает текст """

    # Открываем и читаем содержимое исходного файла для перевода в голос (в данном случае text.txt)
    with open(f'{filePath}', encoding='utf-8') as textFile:
        text = textFile.read()
    return text


def getAudioEdenai(text: str) -> bytes:
    """ В этой функции мы отправляем 2 HTTP запроса:
    # 1. Запрос к веб-сервису для перевода текста в голос;
    # 2. Запрос на скачивание готового аудио файла.
    """

    # API edenai
    headers = {
        # Ключ полученный после регистрации на https://www.edenai.co/
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
                         ".eyJ1c2VyX2lkIjoiOGEzYzc0ZWEtMDIwMi00NGQzLTg"
                         "2NTUtMDE3NTliZDBhN2U1IiwidHlwZSI6ImFwaV90b2tl"
                         "biJ9.S0gu0rchRCHnOwXKARoAFx18T-ZzKHfqPUbcS10PloI"}
    url = "https://api.edenai.run/v2/audio/text_to_speech"
    # Опции для переводчика
    payload = {
        # Режим перевода в голос (строгий, с ударениями и тд)
        "providers": "lovoai",
        # Сообщаем на каком языке исходные данные
        "language": "ru-RU",
        # Мужской или женский голос
        "option": "FEMALE",
        # Выбираем диктора
        "lovoai": "ru-RU_Anna Kravchuk",
        # Исходный текст
        "text": text
    }
    # Отправляем запрос на edenai
    response = requests.post(url, json=payload, headers=headers)
    print("Ваш запрос обрабатывается...")
    # После отправки запроса, веб-сервис некоторое время обрабатывает текст и переводит в голос.
    # Если статус ответа равно 200 - то все в порядке
    # Если же нет - выводим сообщение и приостанавливаем выполение программы
    if (response.status_code != 200):
        print("Что-то пошло не так. Перезапустите, пожалуйста, программу")
        sys.exit(0)
    # Парсим ответ
    result = json.loads(response.text)
    # В свойстве "audio_resource_url" содержится ссылка на аудио файл
    audio_url = result.get("lovoai").get("audio_resource_url")
    r = requests.get(audio_url)
    if (response.status_code != 200):
        print("Что-то пошло не так. Перезапустите, пожалуйста, программу")
        sys.exit(0)
    return r.content


def createWavfile(bytes: bytes) -> str:
    """ Создает файл если он не существуюет и записывает в него бинарные звуковые данные """

    # Генерируем число в формате юникс для имени файла
    filename = int(time.time())
    # Открываем файл и записываем бинарные аудио данные
    with open(f'{filename}.wav', 'wb') as wavFile:
        wavFile.write(bytes)
    return wavFile.name


def runAudio(filename: str):
    """ Запускает файл с помощью штатного проигрывателя """
    os.system(f'start {filename}')


def main():
    text = readText("text.txt")
    audio = getAudioEdenai(text)
    fileName = createWavfile(audio)
    runAudio(fileName)


if __name__ == '__main__':
    main()
