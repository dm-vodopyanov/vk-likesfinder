from src.lang import lang

locale = [
    ['Incorrect authorization token file. Check documentation for more help.',
     'Неверный файл авторизации токена. Обратитесь к документации\nдля получения дополнительной информации.'],

    ['Searching interval is empty',
     'Интервал поиска не задан'],

    ['User is not initialized',
     'Профиль пользователя не задан'],

    ['Cannot identify tool location',
     'Невозможно определить местоположение программы на системе'],

    ['HTML report created:',
     'HTML отчёт создан в'],

    ['Report',
     'Отчёт'],

    ['Report generated:',
     'Отчёт создан в'],

    ['Authorized to VK successfully.',
     'Авторизация на сайт VK прошла успешно.'],

    ['VK API initialized successfully.',
     'VK API инициализирован успешно.'],

    ['ERROR: failed to initialize VK API',
     'ОШИБКА: невозможно проинициализировать VK API'],

    ['VK API is not initialized',
     'VK API не был проинициализирован'],

    ['HTML report is not initialized',
     'HTML отчёт не был создан'],

    ['Checking user',
     'Ищем лайки у пользователя'],

    ['Searching interval',
     'Интервал поиска'],

    ['hour(s) till now (since',
     'часов до текущего времени (начиная с'],

    ['like(s) were found.',
     'лайк(ов) было найдено.'],

    ['ERROR: Failed to get user\'s groups:',
     'ОШИБКА: невозможно получить группы пользователя:'],

    ['SKIPPING:',
     'ПРОПУСК:'],

    ['',
     ''],

    ['WARNING: can\'t skip {} as it is not in the default set of {}',
     'ПРЕДУПРЕЖДЕНИЕ: {} отсутсвует в {}, пропустить невозможно'],

    ['WARNING: {} is invalid {}',
     'ПРЕДУПРЕЖДЕНИЕ: {} не в {}'],

    ['WARNING: {} already in the default set of {}',
     'ПРЕДУПРЕЖДЕНИЕ: {} уже находится в {}'],

    ['Earliest time is not calculated',
     'Время начала поиска не было вычислено'],

    ['Check',
     'Проверяется'],

    ['public pages',
     'публичных страниц'],

    ['WARNING: Read timed out. Re-initialize VK API...',
     'ПРЕДУПРЕЖДЕНИЕ: время чтения данных истекло. Повторная инициализация VK API...'],

    ['completed',
     'готово'],

    [' Nothing found.',
     ' Ничего не найдено.'],

    ['Check groups...',
     'Сканирование групп...'],

    ['WARNING: can\'t skip {} as it is not in the default set of {}',
     'ПРЕДУПРЕЖДЕНИЕ: {} не в списке по умолчанию для {}, невозможно пропустить'],

    ['WARNING: {} is invalid {}',
     'ПРЕДУПРЕЖДЕНИЕ: {} не является {}'],

    ['Earliest time is not calculated',
     'Время начало поиска не было вычислено'],

    ['Check {} {}...',
     'Сканирование {} {}...'],

    ['Check {}/{}: {}',
     'Сканирование {}/{}: {}'],

    ['Check {} {}... completed.',
     'Сканирование {} {}... завершено.'],

    ['Login/password or token are empty.',
     'Передан пустой токен или логин/пароль.'],

    ['User ID is not initialized',
     'ID пользователя не был задан'],

    ['ERROR: %s\n',
     'ОШИБКА: %s\n'],

    ['Hello! Do you want to find the likes of some VK user? There are two steps:\n',
     'Привет! Хочешь найти лайки у кого-то из VK? Ты в двух шагах на пути к этому:\n'],

    ['1. Enter short name or ID of the user (e.g., durov or 1): ',
     '1. Введи короткое имя или ID пользователя (например, durov или 1): '],

    ['2. Specify searching interval in hours (e.g., 10): ',
     '2. Укажи поисковый интервал в часах (например, 10): '],

    ['\nNOTE: use command line options to customize the search. E.g., include '
     '\nor filter some public pages, groups or people.\n',
     '\nПОДСКАЗКА: используй аргументы командной строки для кастомизации поиска.'
     '\nНапример, добавлять или исключать какие-нибудь публичные страницы, группы'
     '\nили людей из поиска.\n'],

    ['en',
     'ru'],

    ['Your access/service token. It needs for authorization\n'
     'to VK. If you need to obtain token or use your\n'
     'login/password, don\'t mention this option, the\n'
     'application will suggest you how you can authorize to\n'
     'VK in user-interactive mode',
     'Твой токен пользователя или сообщества. Он необходим\n'
     'для авторизации на сайт VK. Если тебе нужно получить\n'
     'этот токен или войти, используя логин и пароль, не\n'
     'запускай приложение с этим ключом - приложение само\n'
     'предложит тебе авторизоваться в интерактивном режиме'],

    ['Path to text file with your access/service token for\n'
     'accessing VK. Follow documentation to see how it\n'
     'should be organized. Paste a token to it, and it will\n'
     'be automatically used on authorization step. If you\n'
     'need to obtain token, you will be moved to\n'
     'user-interactive mode. After that\n'
     '{}\n'
     'will be created automatically, and you won\'t need to\n'
     'obtain your token again.',
     'Путь до текстового файла, содержащего твой токен\n'
     'пользователя или сообщества для доступа на сайт VK.\n'
     'Посмотри в документации, как этот файл должен\n'
     'выглядеть. Скопируй в него свой токен, и он будет\n'
     'автоматически использоваться на шаге авторизации.\n'
     'Если тебе нужно получить токен, ты будешь перенаправлен\n'
     'в интерактивный режим. После этого\n'
     '{}\n'
     'будет создан автоматически, и тебе не нужно будет\n'
     'получать токен снова.'],

    ['Short name or ID of checked user',
     'Короткое имя или ID пользователя, у которого нужно\n'
     'найти лайки'],

    ['Searching interval in hours',
     'Поисковый интервал в часах'],
]


def print_config():
    print('lang = {}'.format(lang))
    for i in range(len(locale)):
        print('locale[{}][lang] = {}'.format(i, locale[i][lang]))

if __name__ == '__main__':
    print_config()
