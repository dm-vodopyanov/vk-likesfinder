from src.lang import lang

locale = [
    ['Incorrect authorization token file. Check documentation for more help.',
     'Неверный файл авторизации токена. Обратитесь к документации для получения дополнительной информации.'],

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
     'ПРЕДУПРЕЖДЕНИЕ: время чтения истекло. VK API инициализируется снова...'],

    ['completed',
     'готово'],

    [' Nothing found.',
     ' Ничего не найдено.']
]


def print_config():
    print('lang = {}'.format(lang))
    for i in range(len(locale)):
        print('locale[{}][lang] = {}'.format(i, locale[i][lang]))
