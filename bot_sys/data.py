# Временная "база данных" вузов
UNIVERSITIES = [
    {
        "id": "msu",
        "short_name": "МГУ",
        "full_name": "Московский государственный университет имени М.В. Ломоносова",
        "url": "https://msu.ru",
        "description": "Классический университет, широкий спектр направлений.",
        "file_id": 'AgACAgIAAxkBAAOaauDv8IbJ-gQ0LNBOqWzOgX8ccMAAAkUoaxs0BwlLTxRBNfU8-F0BAAMCAAN5AAM9BA',
        "directions": [
            {"id": "it", "name": "IT", "passing_score": 290, "subjects": ["Русский", "Математика", "Информатика"]},
            {"id": "econ", "name": "Экономика", "passing_score": 285, "subjects": ["Русский", "Математика", "Обществознание"]},
            {"id": "med", "name": "Медицина", "passing_score": 270, "subjects": ["Русский", "Химия", "Биология"]},
            {"id": "hum", "name": "Гуманитарные", "passing_score": 260, "subjects": ["Русский", "История", "Литература"]}
        ]
    },
    {
        "id": "bauman",
        "short_name": "МГТУ",
        "full_name": "Московский государственный технический университет имени Н.Э. Баумана",
        "url": "https://bmstu.ru",
        "description": "Ведущий технический вуз, инженерия и IT.",
        "file_id": 'AgACAgIAAxkBAAOaauDv8IbJ-gQ0LNBOqWzOgX8ccMAAAkUoaxs0BwlLTxRBNfU8-F0BAAMCAAN5AAM9BA',
        "directions": [
            {"id": "it", "name": "IT", "passing_score": 285, "subjects": ["Русский", "Математика", "Информатика"]},
            {"id": "eng", "name": "Инженерия", "passing_score": 275, "subjects": ["Русский", "Математика", "Физика"]}
        ]
    },
    {
        "id": "hse",
        "short_name": "НИУ ВШЭ",
        "full_name": "Национальный исследовательский университет «Высшая школа экономики»",
        "url": "https://hse.ru",
        "description": "Экономика, бизнес-информатика, социальные науки.",
        "file_id": 'AgACAgIAAxkBAAOaauDv8IbJ-gQ0LNBOqWzOgX8ccMAAAkUoaxs0BwlLTxRBNfU8-F0BAAMCAAN5AAM9BA',
        "directions": [
            {"id": "it", "name": "IT", "passing_score": 295, "subjects": ["Русский", "Математика", "Информатика"]},
            {"id": "econ", "name": "Экономика", "passing_score": 300, "subjects": ["Русский", "Математика", "Обществознание"]},
            {"id": "hum", "name": "Гуманитарные", "passing_score": 280, "subjects": ["Русский", "История", "Иностранный язык"]}
        ]
    },
    {
        "id": "mipt",
        "short_name": "МФТИ",
        "full_name": "Московский физико-технический институт",
        "url": "https://mipt.ru",
        "description": "Физтех, математика и программирование, высокая сложность поступления.",
        "file_id": 'AgACAgIAAxkBAAOaauDv8IbJ-gQ0LNBOqWzOgX8ccMAAAkUoaxs0BwlLTxRBNfU8-F0BAAMCAAN5AAM9BA',
        "directions": [
            {"id": "it", "name": "IT", "passing_score": 300, "subjects": ["Русский", "Математика", "Информатика"]},
            {"id": "eng", "name": "Инженерия", "passing_score": 295, "subjects": ["Русский", "Математика", "Физика"]}
        ]
    },
    {
        "id": "mephi",
        "short_name": "МИФИ",
        "full_name": "Национальный исследовательский ядерный университет «МИФИ»",
        "url": "https://mephi.ru",
        "description": "Ядерная физика, кибербезопасность, IT.",
        "file_id": 'AgACAgIAAxkBAAOaauDv8IbJ-gQ0LNBOqWzOgX8ccMAAAkUoaxs0BwlLTxRBNfU8-F0BAAMCAAN5AAM9BA',
        "directions": [
            {"id": "it", "name": "IT", "passing_score": 260, "subjects": ["Русский", "Математика", "Информатика"]},
            {"id": "eng", "name": "Инженерия", "passing_score": 250, "subjects": ["Русский", "Математика", "Физика"]}
        ]
    },
    {
        "id": "mirea",
        "short_name": "РТУ МИРЭА",
        "full_name": "МИРЭА — Российский технологический университет",
        "url": "https://mirea.ru",
        "description": "Информационные технологии, электроника, химия.",
        "file_id": 'AgACAgIAAxkBAAOaauDv8IbJ-gQ0LNBOqWzOgX8ccMAAAkUoaxs0BwlLTxRBNfU8-F0BAAMCAAN5AAM9BA',
        "directions": [
            {"id": "it", "name": "IT", "passing_score": 240, "subjects": ["Русский", "Математика", "Информатика"]},
            {"id": "med", "name": "Медицина", "passing_score": 230, "subjects": ["Русский", "Химия", "Биология"]}
        ]
    },
    {
        "id": "mpei",
        "short_name": "НИУ МЭИ",
        "full_name": "Национальный исследовательский университет «МЭИ»",
        "url": "https://mpei.ru",
        "description": "Энергетика, электротехника, теплоэнергетика.",
        "file_id": 'AgACAgIAAxkBAAOaauDv8IbJ-gQ0LNBOqWzOgX8ccMAAAkUoaxs0BwlLTxRBNfU8-F0BAAMCAAN5AAM9BA',
        "directions": [
            {"id": "eng", "name": "Инженерия", "passing_score": 235, "subjects": ["Русский", "Математика", "Физика"]},
            {"id": "econ", "name": "Экономика", "passing_score": 220, "subjects": ["Русский", "Математика", "Обществознание"]}
        ]
    }
]
