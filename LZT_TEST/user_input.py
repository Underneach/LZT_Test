import os


def User_Input():

    """
    Получаем от пользователя Введите поисковый запрос, индекс видео и путь к файлу с куками
    """

    while True:
        search_query = input("Введите поисковый запрос: ")
        if search_query:
            break

    while True:
        video_index = input("Введите индекс видео: ")
        if video_index:
            break

    while True:
        cookee_path = input("Введите путь к файлу с Netscape куками: ")
        if os.path.exists(cookee_path):
            break

    return search_query, int(video_index), cookee_path
