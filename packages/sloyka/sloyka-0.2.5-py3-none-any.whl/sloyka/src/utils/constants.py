TARGET_SCORE: int = 0.7
END_INDEX_POSITION: int = 4
START_INDEX_POSITION: int = 3
SCORE_THRESHOLD = 0.7

TOPONYM_PATTERN = r"путепровод|улица|набережная реки|проспект"\
            r"|бульвар|мост|переулок|площадь|переулок"\
            r"|набережная|канала|канал|дорога на|дорога в"\
            r"|шоссе|аллея|проезд|линия"

TARGET_TOPONYMS = [
    "пр",
    "проспект",
    "проспекте",
    "ул",
    "улица",
    "улице",
    "площадь",
    "площади",
    "пер",
    "переулок",
    "проезд",
    "проезде",
    "дорога",
    "дороге",
    "линия",
    "линии"
]
REPLACEMENT_DICT = {
    "пр": "проспект",
    "ул": "улица",
    "пер": "переулок",
    "улице": "улица",
    "проспекте": "проспект",
    "площади": "площадь",
    "проезде": "проезд",
    "дороге": "дорога",
    "линии": "линия"
}

GLOBAL_CRS = 4326
GLOBAL_METRIC_CRS = 3857

OSM_TAGS = {
    "subway": ["yes"],
    "amenity": ["university", "school"],
    "landuse": [
        "brownfield",
        "cemetery",
        "commercial",
        "construction",
        "flowerbed",
        "grass",
        "industrial",
        "meadow",
        "military",
        "plant_nursery",
        "recreation_ground",
        "religious",
        "residential",
        "retail",
    ],
    "natural": ["water", "beach"],
    "leisure": [
        "garden",
        "marina",
        "nature_reserve",
        "park",
        "pitch",
        "sports_centre",
    ],
    "highway": [
        "construction",
        "footway",
        "motorway",
        "pedestrian",
        "primary",
        "primary_link",
        "residential",
        "secondary",
        "service",
        "steps",
        "tertiary",
        "tertiary_link",
        "unclassified",
    ],
    "railway": ["rail", "subway"],
    "amenity": [
        "arts_centre",
        "atm",
        "bank",
        "bar",
        "boat_rental",
        "bus_station",
        "bicycle_rental",
        "biergarten",
        "cafe",
        "car_wash",
        "childcare",
        "cinema",
        "clinic",
        "clinic;doctors;audiologist",
        "college",
        "community_centre",
        "courthouse",
        "coworking_space",
        "dancing_school",
        "dentist",
        "doctors",
        "driving_school",
        "events_venue",
        "fast_food",
        "fire_station",
        "food_court",
        "fountain",
        "fuel",
        "hookah_lounge",
        "hospital",
        "internet_cafe",
        "kindergarten",
        "language_school",
        "library",
        "music_school",
        "music_venue",
        "nightclub",
        "offices",
        "parcel_locker",
        "parking",
        "payment_centre",
        "pharmacy",
        "place_of_worship",
        "police",
        "post_office",
        "pub",
        "recycling",
        "rescue_station",
        "restaurant",
        "school",
        "social_centre",
        "social_facility",
        "studio",
        "theatre",
        "training",
        "university",
        "vending_machine",
        "veterinary",
        "townhall",
        "shelter",
        "marketplace",
        "monastery",
        "planetarium",
        "research_institute",
    ],
    "building": [
        "apartments",
        "boat",
        "bunker",
        "castle",
        "cathedral",
        "chapel",
        "church",
        "civic",
        "college",
        "commercial",
        "detached",
        "dormitory",
        "garages",
        "government",
        "greenhouse",
        "hospital",
        "hotel",
        "house",
        "industrial",
        "kindergarten",
        "kiosk",
        "mosque",
        "office",
        "pavilion",
        "policlinic",
        "public",
        "residential",
        "retail",
        "roof",
        "ruins",
        "school",
        "service",
        "ship",
        "sport_centre",
        "sports_hall",
        "theatre",
        "university",
    ],
    "man_made": [
        "bridge",
        "courtyard",
        "lighthouse",
        "mineshaft",
        "pier",
        "satellite",
        "tower",
        "works",
    ],
    "leisure": [
        "amusement_arcade",
        "fitness_centre",
        "playground",
        "sauna",
        "stadium",
        "track",
    ],
    "office": [
        "company",
        "diplomatic",
        "energy_supplier",
        "government",
        "research",
        "telecommunication",
    ],
    "shop": [
        "alcohol",
        "antiques",
        "appliance",
        "art",
        "baby_goods",
        "bag",
        "bakery",
        "bathroom_furnishing",
        "beauty",
        "beauty;hairdresser;massage;cosmetics;perfumery",
        "bed",
        "beverages",
        "bicycle",
        "binding",
        "bookmaker",
        "books",
        "boutique",
        "butcher",
        "car",
        "car_parts",
        "car_repair",
        "carpet",
        "cheese",
        "chemist",
        "clothes",
        "coffee",
        "computer",
        "confectionery",
        "convenience",
        "copyshop",
        "cosmetics",
        "cosmetics;chemist",
        "craft",
        "craft;paint",
        "curtain",
        "dairy",
        "deli",
        "doityourself",
        "doors",
        "dry_cleaning",
        "e-cigarette",
        "electrical",
        "electronics",
        "electronics;fishing",
        "erotic",
        "estate_agent",
        "fabric",
        "farm",
        "fireplace",
        "fishing",
        "flooring",
        "florist",
        "frame",
        "frozen_food",
        "furniture",
        "games",
        "garden_centre",
        "gas",
        "general",
        "gift",
        "glaziery",
        "gold_buyer",
        "greengrocer",
        "hairdresser",
        "hairdresser_supply",
        "hardware",
        "health_food",
        "hearing_aids",
        "herbalist",
        "honey",
        "houseware",
        "interior_decoration",
        "jeweller_tools",
        "jewelry",
        "kiosk",
        "kitchen",
        "laundry",
        "leather",
        "lighting",
        "lottery",
        "massage",
        "medical_supply",
        "mobile_phone",
        "money_lender",
        "motorcycle",
        "music",
        "newsagent",
        "nuts",
        "optician",
        "orthopaedic",
        "orthopaedics",
        "outdoor",
        "outpost",
        "paint",
        "pastry",
        "pawnbroker",
        "perfumery",
        "pet",
        "pet_grooming",
        "photo",
        "pottery",
        "printer_ink",
        "printing",
        "radiotechnics",
        "repair",
        "seafood",
        "second_hand",
        "security",
        "sewing",
        "shoes",
        "sports",
        "stationery",
        "stationery;copyshop",
        "storage_rental",
        "supermarket",
        "tableware",
        "tailor",
        "tattoo",
        "tea",
        "ticket",
        "tobacco",
        "toys",
        "travel_agency",
        "variety_store",
        "watches",
        "water_filter",
        "weapons",
        "wine",
    ],
    "bus": ["yes"],
    "public_transport": ["platform", "station", "stop_position"],
    "railway": ["tram_stop", "station"],
}

TAG_ROUTER = {"NOUN": "содержит", "ADJF": "описание", "ADJS": "описание", "VERB": "активность", "INFN": "активность"}

STOPWORDS = [
    "фото",
    "улица",
    "улицы",
    "улице",
    "улицу",
    "улицей",
    "улицею",
    "улиц",
    "улицам",
    "улицами",
    "улицах",
    "дом",
    "дома",
    "дому",
    "домом",
    "доме",
    "домов",
    "домам",
    "домами",
    "домах",
    "проспект",
    "проспекта",
    "проспекту",
    "проспектом",
    "проспекте",
    "проспекты",
    "проспектов",
    "проспектам",
    "проспектами",
    "проспектах",
    "дорога",
    "дороги",
    "дороге",
    "дорогу",
    "дорогой",
    "дорогою",
    "дорог",
    "дорогам",
    "дорогами",
    "дорогах",
    "час",
    "часа",
    "часу",
    "часом",
    "часе",
    "часы",
    "часов",
    "часам",
    "часами",
    "часах",
    "год",
    "года",
    "году",
    "годом",
    "годе",
    "годы",
    "лета",
    "годов",
    "лет",
    "годам",
    "годами",
    "годах",
    "гг",
    "летам",
    "летами",
    "летах",
    "утро",
    "утра",
    "утру",
    "утром",
    "утре",
    "утр",
    "утрам",
    "утрами",
    "утрах",
    "здравствуйте",
    "ул",
    "пр",
    "здание",
    "зданье",
    "здания",
    "зданья",
    "зданию",
    "зданью",
    "зданием",
    "зданьем",
    "здании",
    "зданьи",
    "зданий",
    "зданиям",
    "зданьям",
    "зданиями",
    "зданьями",
    "зданиях",
    "зданьях",
    "город",
    "города",
    "городу",
    "городом",
    "городе",
    "городов",
    "городам",
    "городами",
    "городах",
    "аноним",
    "анонима",
    "анониму",
    "анонимом",
    "анониме",
    "анонимы",
    "анонимов",
    "анонимам",
    "анонимами",
    "анонимах",
    "день",
    "дня",
    "дню",
    "днём",
    "дне",
    "дни",
    "дней",
    "дням",
    "днями",
    "днях",
    "вечер",
    "вечера",
    "вечеру",
    "вечером",
    "вечере",
    "вечеров",
    "вечерам",
    "вечерами",
    "вечерах" "адрес",
    "адреса",
    "адресу",
    "адресом",
    "адресе",
    "адресы",
    "адресов",
    "адресам",
    "адресами",
    "адресах",
]
SPB_DISTRICTS = [
    {"name": "Санкт-Петербург", "admin_level": 4, "parent": None},
    {"name": "Адмиралтейский", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Василеостровский", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Выборгский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Калининский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Кировский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Колпинский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Красногвардейский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Красносельский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Кронштадтский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Курортный район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Ломоносовский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Московский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Невский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Петроградский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Петродворцовый район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Приморский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Пушкинский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Фрунзенский район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "Центральный район", "admin_level": 5, "parent": "Санкт-Петербург"},
    {"name": "мун. округ Коломна", "admin_level": 6, "parent": "Адмиралтейский район"},
    {"name": "мун. округ Сенной округ", "admin_level": 6, "parent": "Адмиралтейский район"},
    {"name": "мун. округ Адмиралтейский округ", "admin_level": 6, "parent": "Адмиралтейский район"},
    {"name": "мун. округ Семёновский", "admin_level": 6, "parent": "Адмиралтейский район"},
    {"name": "мун. округ Измайловское", "admin_level": 6, "parent": "Адмиралтейский район"},
    {"name": "мун. округ Екатерингофский", "admin_level": 6, "parent": "Адмиралтейский район"},
    {"name": "мун. округ № 7", "admin_level": 6, "parent": "Василеостровский район"},
    {"name": "мун. округ Васильевский", "admin_level": 6, "parent": "Василеостровский район"},
    {"name": "мун. округ Гавань", "admin_level": 6, "parent": "Василеостровский район"},
    {"name": "мун. округ Морской", "admin_level": 6, "parent": "Василеостровский район"},
    {"name": "nan округ Морской", "admin_level": 6, "parent": "nan район"},
    {"name": "мун. округ Остров Декабристов", "admin_level": 6, "parent": "Василеостровский район"},
    {"name": "мун. округ Сампсониевское", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "мун. округ Светлановское", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "мун. округ Сосновское", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "мун. округ № 15", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "мун. округ Сергиевское", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "nan Парнас", "admin_level": 6, "parent": "nan район"},
    {"name": "мун. округ Шувалово-Озерки", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "посёлок Левашово", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "посёлок Парголово", "admin_level": 6, "parent": "Выборгский район"},
    {"name": "мун. округ Гражданка", "admin_level": 6, "parent": "Калининский район"},
    {"name": "мун. округ Академическое", "admin_level": 6, "parent": "Калининский район"},
    {"name": "мун. округ Финляндский округ", "admin_level": 6, "parent": "Калининский район"},
    {"name": "мун. округ № 21", "admin_level": 6, "parent": "Калининский район"},
    {"name": "мун. округ Пискарёвка", "admin_level": 6, "parent": "Калининский район"},
    {"name": "мун. округ Северный", "admin_level": 6, "parent": "Калининский район"},
    {"name": "мун. округ Прометей", "admin_level": 6, "parent": "Калининский район"},
    {"name": "мун. округ Княжево", "admin_level": 6, "parent": "Кировский район"},
    {"name": "мун. округ Ульянка", "admin_level": 6, "parent": "Кировский район"},
    {"name": "мун. округ Дачное", "admin_level": 6, "parent": "Кировский район"},
    {"name": "мун. округ Автово", "admin_level": 6, "parent": "Кировский район"},
    {"name": "мун. округ Нарвский округ", "admin_level": 6, "parent": "Кировский район"},
    {"name": "мун. округ Красненькая речка", "admin_level": 6, "parent": "Кировский район"},
    {"name": "мун. округ Морские ворота", "admin_level": 6, "parent": "Кировский район"},
    {"name": "город Колпино", "admin_level": 6, "parent": "Колпинский район"},
    {"name": "посёлок Понтонный", "admin_level": 6, "parent": "Колпинский район"},
    {"name": "посёлок Усть-Ижора", "admin_level": 6, "parent": "Колпинский район"},
    {"name": "посёлок Петро-Славянка", "admin_level": 6, "parent": "Колпинский район"},
    {"name": "посёлок Сапёрный", "admin_level": 6, "parent": "Колпинский район"},
    {"name": "посёлок Металлострой", "admin_level": 6, "parent": "Колпинский район"},
    {"name": "мун. округ Полюстрово", "admin_level": 6, "parent": "Красногвардейский район"},
    {"name": "мун. округ Большая Охта", "admin_level": 6, "parent": "Красногвардейский район"},
    {"name": "мун. округ Малая Охта", "admin_level": 6, "parent": "Красногвардейский район"},
    {"name": "мун. округ Пороховые", "admin_level": 6, "parent": "Красногвардейский район"},
    {"name": "мун. округ Ржевка", "admin_level": 6, "parent": "Красногвардейский район"},
    {"name": "мун. округ Юго-Запад", "admin_level": 6, "parent": "Красносельский район"},
    {"name": "мун. округ Южно-Приморский", "admin_level": 6, "parent": "Красносельский район"},
    {"name": "мун. округ Сосновая Поляна", "admin_level": 6, "parent": "Красносельский район"},
    {"name": "мун. округ Урицк", "admin_level": 6, "parent": "Красносельский район"},
    {"name": "мун. округ Константиновское", "admin_level": 6, "parent": "Красносельский район"},
    {"name": "мун. округ Горелово", "admin_level": 6, "parent": "Красносельский район"},
    {"name": "город Красное Село", "admin_level": 6, "parent": "Красносельский район"},
    {"name": "город Кронштадт", "admin_level": 6, "parent": "Кронштадтский район"},
    {"name": "город Зеленогорск", "admin_level": 6, "parent": "Курортный район"},
    {"name": "город Сестрорецк", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Белоостров", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Комарово", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Молодёжное", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Песочный", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Репино", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Серово", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Смолячково", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Солнечное", "admin_level": 6, "parent": "Курортный район"},
    {"name": "посёлок Ушково", "admin_level": 6, "parent": "Курортный район"},
    {"name": "мун. округ Московская застава", "admin_level": 6, "parent": "Московский район"},
    {"name": "мун. округ Гагаринское", "admin_level": 6, "parent": "Московский район"},
    {"name": "мун. округ Новоизмайловское", "admin_level": 6, "parent": "Московский район"},
    {"name": "мун. округ Пулковский меридиан", "admin_level": 6, "parent": "Московский район"},
    {"name": "мун. округ Звёздное", "admin_level": 6, "parent": "Московский район"},
    {"name": "мун. округ Невская застава", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Ивановский", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Обуховский", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Рыбацкое", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Народный", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ № 54", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Невский округ", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Оккервиль", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Правобережный", "admin_level": 6, "parent": "Невский район"},
    {"name": "мун. округ Введенский", "admin_level": 6, "parent": "Петроградский район"},
    {"name": "мун. округ Кронверкское", "admin_level": 6, "parent": "Петроградский район"},
    {"name": "мун. округ Посадский", "admin_level": 6, "parent": "Петроградский район"},
    {"name": "мун. округ округ Петровский", "admin_level": 6, "parent": "Петроградский район"},
    {"name": "мун. округ Чкаловское", "admin_level": 6, "parent": "Петроградский район"},
    {"name": "посёлок Стрельна", "admin_level": 6, "parent": "Петродворцовый район"},
    {"name": "город Ломоносов", "admin_level": 6, "parent": "Петродворцовый район"},
    {"name": "город Петергоф", "admin_level": 6, "parent": "Петродворцовый район"},
    {"name": "мун. округ Лахта-Ольгино", "admin_level": 6, "parent": "Приморский район"},
    {"name": "мун. округ № 65", "admin_level": 6, "parent": "Приморский район"},
    {"name": "мун. округ Ланское", "admin_level": 6, "parent": "Приморский район"},
    {"name": "nan Чёрная речка", "admin_level": 6, "parent": "nan район"},
    {"name": "мун. округ Комендантский аэродром", "admin_level": 6, "parent": "Приморский район"},
    {"name": "мун. округ Озеро Долгое", "admin_level": 6, "parent": "Приморский район"},
    {"name": "мун. округ Аптекарский остров", "parent": "Приморский район"},
    {"name": "мун. округ Юнтолово", "admin_level": 6, "parent": "Приморский район"},
    {"name": "мун. округ Коломяги", "admin_level": 6, "parent": "Приморский район"},
    {"name": "посёлок Лисий Нос", "admin_level": 6, "parent": "Приморский район"},
    {"name": "город Павловск", "admin_level": 6, "parent": "Пушкинский район"},
    {"name": "город Пушкин", "admin_level": 6, "parent": "Пушкинский район"},
    {"name": "посёлок Шушары", "admin_level": 6, "parent": "Пушкинский район"},
    {"name": "посёлок Александровская", "admin_level": 6, "parent": "Пушкинский район"},
    {"name": "посёлок Тярлево", "admin_level": 6, "parent": "Пушкинский район"},
    {"name": "мун. округ Волковское", "admin_level": 6, "parent": "Фрунзенский район"},
    {"name": "мун. округ № 72", "admin_level": 6, "parent": "Фрунзенский район"},
]

CITY_SERVICES_NAMES = [
    "Детский сад",
    "Школа",
    "Сад",
    "Дом детского творчества",
    "Детско-юношеская спортивная школа",
    "Детский лагерь",
    "Среднее специальное учебное заведение",
    "Высшее учебное заведение",
    "Поликлиника",
    "Детская поликлиника",
    "Стоматологическая клиника",
    "Фельдшерско-акушерский пункт",
    "Женская консультация",
    "Реабилитационный центр",
    "Аптека",
    "Метро",
    "Больница",
    "Роддом",
    "Детская больница",
    "Хоспис",
    "Станция скорой медицинской помощи",
    "Травматологические пункты",
    "Морг",
    "Диспансер",
    "Комплексный центр социального обслуживания населения",
    "Дом престарелых",
    "Центр занятости населения",
    "Детские дома-интернаты",
    "Многофункциональные центры предоставления государственных и муниципальных услуг",
    "Библиотека",
    "Дворец культуры",
    "Музей",
    "Театр",
    "Ботанический сад",
    "Концертный зал",
    "Цирк",
    "Зоопарк",
    "Кинотеатр",
    "Торговый центр",
    "Аквапарк",
    "Стадион",
    "Ледовая арена",
    "Кафе",
    "Ресторан",
    "Бар",
    "Столовая",
    "Булочная",
    "Парк",
    "Лес",
    "Заказник",
    "Заповедник",
    "Газон",
    "Поле",
    "Пляж",
    "Река",
    "Озеро",
    "Болото",
    "Ручей",
    "Залив",
    "Спортивная площадка",
    "Бассейн",
    "Спортивный зал",
    "Каток",
    "Футбольное поле",
    "Веревочный парк",
    "Экологическая тропа",
    "Скалодром",
    "Детская площадка",
    "Парк атракционов",
    "Игровое пространство",
    "Скейт-парк",
    "Полицейский участок",
    "Пожарная станция",
    "Железнодорожная станция",
    "Железнодорожный вокзал",
    "Аэропорт",
    "Аэродром",
    "Автозаправка",
    "Парковка",
    "Автовокзал",
    "Остановка наземного общественного транспорта",
    "Выход метро",
    "Супермаркет",
    "Продукты",
    "Рынок",
    "Хозяйственные товары",
    "Одежда и обувь",
    "Бытовая техника",
    "Книжный магазин",
    "Детские товары",
    "Спортивный магазин",
    "Почтовое отделение",
    "Пункт выдачи",
    "Отделение банка",
    "Банкомат",
    "Адвокат",
    "Нотариальная контора",
    "Парикмахер",
    "Салон красоты",
    "Общественная баня",
    "Ветеринарная клиника",
    "Зоомагазин",
    "Площадка для выгула собак",
    "Гостиница",
    "Хостел",
    "Фонтан",
    "База отдыха",
    "Памятник",
    "Церковь",
    "Кладбище",
    "Котельная",
    "Тепло-электроцентраль",
    "Атомная электростанция",
    "Гидро-электростанция",
    "Тепловая электростанция",
    "Солнечная батарея",
    "Ветрогенератор",
    "Электрическая подстанция",
    "Водозаборные сооружения",
    "Насосные станции водоснабжения",
    "Сооружения для очистки воды",
    "Водонапорные башни и резервуары",
    "Водоочистное сооружение",
    "Выпуски сточных вод в водоем",
    "Насосная станция водоотведения",
    "Воинская часть",
    "Промышленная зона",
    "Магазин",
    "Остановка",
    "ДК",
    "Детская площадка",
    "Сад",
    "Баня",
    "Университет",
    "Институт",
]

NUM_CITY_OBJ = {
    "школа": [
        "школа",
        "школы",
        "школе",
        "школу",
        "школой",
        "школе",
        "школы",
        "школ",
        "школам",
        "школы",
        "школами",
        "школах",
        "школ",
    ],
    "лицей": [
        "лицей",
        "лицея",
        "лицею",
        "лицей",
        "лицеем",
        "лицее",
        "лицеи",
        "лицеев",
        "лицеям",
        "лицеи",
        "лицеями",
        "лицеях",
        "лицеев",
    ],
    "гимназия": [
        "гимназия",
        "гимназии",
        "гимназии",
        "гимназию",
        "гимназией",
        "гимназии",
        "гимназии",
        "гимназий",
        "гимназиям",
        "гимназии",
        "гимназиями",
        "гимназиях",
        "гимназий",
    ],
    "поликлиника": [
        "поликлиника",
        "поликлиники",
        "поликлинике",
        "поликлинику",
        "поликлиникой",
        "поликлинике",
        "поликлиники",
        "поликлиник",
        "поликлиникам",
        "поликлиники",
        "поликлиниками",
        "поликлиниках",
        "поликлиник",
    ],
    "больница": [
        "больница",
        "больницы",
        "больнице",
        "больницу",
        "больницей",
        "больнице",
        "больницы",
        "больниц",
        "больницам",
        "больницы",
        "больницами",
        "больницах",
        "больниц",
    ],
    "городская больница": [
        "городская больница",
        "городской больницы",
        "городской больнице",
        "городскую больницу",
        "городской больницей",
        "городской больнице",
        "городские больницы",
        "городских больниц",
        "городским больницам",
        "городские больницы",
        "городскими больницами",
        "городских больницах",
        "городских больниц",
    ],
    "детский сад": [
        "детский сад",
        "детского сада",
        "детскому саду",
        "детский сад",
        "детским садом",
        "детском саде",
        "детские сады",
        "детских садов",
        "детским садам",
        "детские сады",
        "детскими садами",
        "детских садах",
        "детских садов",
    ],
    "стоматологическая поликлиника": [
        "стоматологическая поликлиника",
        "стоматологической поликлиники",
        "стоматологической поликлинике",
        "стоматологическую поликлинику",
        "стоматологической поликлиникой",
        "стоматологической поликлинике",
        "стоматологические поликлиники",
        "стоматологических поликлиник",
        "стоматологическим поликлиникам",
        "стоматологические поликлиники",
        "стоматологическими поликлиниками",
        "стоматологических поликлиниках",
        "стоматологических поликлиник",
    ],
    "детская поликлиника": [
        "детская поликлиника",
        "детской поликлиники",
        "детской поликлинике",
        "детскую поликлинику",
        "детской поликлиникой",
        "детской поликлинике",
        "детские поликлиники",
        "детских поликлиник",
        "детским поликлиникам",
        "детские поликлиники",
        "детскими поликлиниками",
        "детских поликлиниках",
        "детских поликлиник",
    ],
    "женская консультация": [
        "женская консультация",
        "женской консультации",
        "женской консультации",
        "женскую консультацию",
        "женской консультацией",
        "женской консультации",
        "женские консультации",
        "женских консультаций",
        "женским консультациям",
        "женские консультации",
        "женскими консультациями",
        "женских консультациях",
        "женских консультаций",
    ],
    "городская поликлиника": [
        "городская поликлиника",
        "городской поликлиники",
        "городской поликлинике",
        "городскую поликлинику",
        "городской поликлиникой",
        "городской поликлинике",
        "городские поликлиники",
        "городских поликлиник",
        "городским поликлиникам",
        "городские поликлиники",
        "городскими поликлиниками",
        "городских поликлиниках",
        "городских поликлиник",
    ],
    "детская городская поликлиника": [
        "детская городская поликлиника",
        "детской городской поликлиники",
        "детской городской поликлинике",
        "детскую городскую поликлинику",
        "детской городской поликлиникой",
        "детской городской поликлинике",
        "детские городские поликлиники",
        "детских городских поликлиник",
        "детским городским поликлиникам",
        "детские городские поликлиники",
        "детскими городскими поликлиниками",
        "детских городских поликлиниках",
        "детских городских поликлиник",
    ],
}

EXCEPTIONS_CITY_COUNTRY = [
    "Санкт-Петербург",
    "СПБ",
    "спб",
    "санкт-петербург",
    "питер",
    "Питербург",
    "Питер",
    "питербург",
    "Москва",
    "москва",
    "мск",
    "МСК",
    "Петербург",
    "петербург ",
    "ФОЛКЛЕНДСКИЕ О-ВА",
    "МИКРОНЕЗИЯ",
    "ФАРЕРСКИЕ О-ВА",
    "ФРАНЦИЯ",
    "ГАБОН",
    "ВЕЛИКОБРИТАНИЯ",
    "ГРЕНАДА",
    "ГРУЗИЯ",
    "ГВИАНА",
    "ГАНА",
    "ГИБРАЛТАР",
    "ГРЕНЛАНДИЯ",
    "ГАМБИЯ",
    "ГВИНЕЯ",
    "ГВАДЕЛУПА",
    "ЭКВАТОР. ГВИНЕЯ",
    "ГРЕЦИЯ",
    "Ю.ДЖ.И САНДВ.О-ВА",
    "ГВАТЕМАЛА",
    "ГУАМ",
    "ГВИНЕЯ-БИСАУ",
    "ГАЙАНА",
    "СЯНГАН (ГОНКОНГ)",
    "ХЕРД И МАКДОНАЛЬД",
    "ГОНДУРАС",
    "ХОРВАТИЯ",
    "ГАИТИ",
    "ВЕНГРИЯ",
    "ИНДОНЕЗИЯ",
    "ИРЛАНДИЯ",
    "ИЗРАИЛЬ",
    "О-В МЭН",
    "ИНДИЯ",
    "БРИТ.ТЕР.В ИНД.ОК",
    "ИРАК",
    "ИРАН",
    "ИСЛАНДИЯ",
    "ИТАЛИЯ",
    "ЯМАЙКА",
    "ИОРДАНИЯ",
    "ЯПОНИЯ",
    "ДЖОНСТОН АТОЛЛ",
    "КЕНИЯ",
    "КЫРГЫЗСТАН",
    "КАМБОДЖА",
    "КИРИБАТИ",
    "КОМОРСКИЕ О-ВА",
    "СЕНТ-КИТС И НЕВИС",
    "КОРЕЯ (КНДР)",
    "КОРЕЯ РЕСП.",
    "КУВЕЙТ",
    "КАЙМАН",
    "КАЗАХСТАН",
    "ЛАОС",
    "ЛИВАН",
    "СЕНТ-ЛЮСИЯ",
    "ЛИХТЕНШТЕЙН",
    "ШРИ-ЛАНКА",
    "ЛИБЕРИЯ",
    "ЛЕСОТО",
    "ЛИТВА",
    "ЛЮКСЕМБУРГ",
    "ЛАТВИЯ",
    "ЛИВИЯ",
    "МАРОККО",
    "МОНАКО",
    "МОЛДОВА",
    "МАДАГАСКАР",
    "МАРШАЛЛОВЫ О-ВА",
    "О-ВА МИДУЭЙ",
    "МАКЕДОНИЯ",
    "МАЛИ",
    "МОНГОЛИЯ",
    "АОМЫНЬ(МАКАО)",
    "МАРИАНСКИЕ О-ВА",
    "МАРТИНИКА",
    "МАВРИТАНИЯ",
    "МОНТСЕРРАТ",
    "МАЛЬТА",
    "МАВРИКИЙ",
    "МАЛЬДИВЫ",
    "МАЛАВИ",
    "МЕКСИКА",
    "МАЛАЙЗИЯ",
    "МОЗАМБИК",
    "НАМИБИЯ",
    "НОВ.КАЛЕДОНИЯ",
    "НИГЕР",
    "НОРФОЛК",
    "НИГЕРИЯ",
    "НИКАРАГУА",
    "НИДЕРЛАНДЫ",
    "НОРВЕГИЯ",
    "НЕПАЛ",
    "НАУРУ",
    "НИУЭ",
    "НОВАЯ ЗЕЛАНДИЯ",
    "ОМАН",
    "ПАНАМА",
    "ПЕРУ",
    "ФР. ПОЛИНЕЗИЯ",
    "ПАПУА-НОВ.ГВИНЕЯ",
    "ФИЛИППИНЫ",
    "ПАКИСТАН",
    "ПОЛЬША",
    "С-ПЬЕР И МИКЕЛОН",
    "ПИТКЭРН",
    "ПУЭРТО-РИКО",
    "ПОРТУГАЛИЯ",
    "ПАЛАУ",
    "ПАРАГВАЙ",
    "КАТАР",
    "РЕЮНЬОН",
    "РУМЫНИЯ",
    "РОССИЯ",
    "РУАНДА",
    "САУДОВСКАЯ АРАВИЯ",
    "СОЛОМОНОВЫ О-ВА",
    "СЕЙШЕЛЬСКИЕ О-ВА",
    "СУДАН",
    "ШВЕЦИЯ",
    "СИНГАПУР",
    "О-В СВЯТОЙ ЕЛЕНЫ",
    "СЛОВЕНИЯ",
    "ШПИЦБЕРГЕН О-ВА",
    "СЛОВАКИЯ",
    "СЬЕРРА-ЛЕОНЕ",
    "САН-МАРИНО",
    "СЕНЕГАЛ",
    "СОМАЛИ",
    "СУРИНАМ",
    "САН-ТОМЕ И ПРИНС.",
    "САЛЬВАДОР",
    "СИРИЯ",
    "СВАЗИЛЕНД",
    "ТЕРКС И КАЙКОС",
    "ЧАД",
    "ФР.ЮЖНЫЕ ТЕРИТОР.",
    "ТОГО",
    "ТАИЛАНД",
    "ТАДЖИКИСТАН",
    "ТОКЕЛАУ (ЮНИОН)",
    "ТУРКМЕНИСТАН",
    "ТУНИС",
    "ТОНГА",
    "ВОСТОЧНЫЙ ТИМОР",
    "ТУРЦИЯ",
    "ТРИНИДАД И ТОБАГО",
    "ТУВАЛУ",
    "ТАЙВАНЬ",
    "ТАНЗАНИЯ",
    "УКРАИНА",
    "УГАНДА",
    "МАЛЫЕ ТИХООК.О-ВА",
    "США",
    "УРУГВАЙ",
    "УЗБЕКИСТАН",
    "ВАТИКАН",
    "С.ВИНСЕНТ.ГРЕНАД.",
    "ВЕНЕСУЭЛА",
    "ВИРГИН.О-ВА(БРИТ)",
    "ВИРГИН.О-ВА (США)",
    "ВЬЕТНАМ",
    "ВАНУАТУ",
    "УОЛЛИС И ФУТУНА",
    "О-В УЭЙК",
    "ЗАПАДНОЕ САМОА",
    "ЙЕМЕН",
    "ЮГОСЛАВИЯ",
    "ЮЖНО-АФР.РЕСПУБЛ.",
    "ЗАМБИЯ",
    "ЗАИР",
    "ЗИМБАБВЕ",
    "МЬЯНМА",
    "МАЙОТТА",
    "КОНГО",
    "ЭЛАНДСКИЕ О-ВА",
    "ПАЛЕСТИНА ОКУП.",
    "ТИМОР-ЛЕСТЕ",
    "ЧЕРНОГОРИЯ",
    "МЕЖДУНАРОДНЫЕ ОРГ",
    "ДЖЕРСИ",
    "Кюрасао",
    "ГЕРНСИ",
    "ДРУГАЯ СТРАНА",
    "АБХАЗИЯ",
    "СЕРБИЯ",
    "СТРАНА НЕ ОПР.",
    "АНДОРРА",
    "ОБЪЕД.РАБ.ЭМИРАТ",
    "АФГАНИСТАН",
    "АНТИГУА.БАРБ",
    "АНГИЛЬЯ",
    "АЛБАНИЯ",
    "АРМЕНИЯ",
    "АНТИЛЬСКИЕ О-ВА",
    "АНГОЛА",
    "АНТАРКТИКА",
    "АРГЕНТИНА",
    "ВОСТ.САМОА (США)",
    "АВСТРИЯ",
    "АВСТРАЛИЯ",
    "АРУБА",
    "АЗЕРБАЙДЖАН",
    "БОСНИЯ И ГЕРЦОГ.",
    "БАРБАДОС",
    "БАНГЛАДЕШ",
    "БЕЛЬГИЯ",
    "БУРКИНА-ФАСО",
    "БОЛГАРИЯ",
    "БАХРЕЙН",
    "БУРУНДИ",
    "БЕНИН",
    "БЕРМУДСКИЕ О-ВА",
    "БРУНЕЙ",
    "БОЛИВИЯ",
    "БРАЗИЛИЯ",
    "БАГАМСКИЕ О-ВА",
    "БУТАН",
    "БУВЕ",
    "БОТСВАНА",
    "БЕЛАРУСЬ",
    "БЕЛИЗ",
    "КАНАДА",
    "КОКОСОВЫЕ О-ВА",
    "ЦЕНТР.АФР.РЕСПУБ.",
    "КОНГО",
    "ШВЕЙЦАРИЯ",
    "КОТ-Д'ИВУАР",
    "О-ВА КУКА",
    "ЧИЛИ",
    "КАМЕРУН",
    "КИТАЙ",
    "КОЛУМБИЯ",
    "КОСТА-РИКА",
    "КУБА",
    "КАБО-ВЕРДЕ",
    "О-В РОЖДЕСТВА",
    "КИПР",
    "ЧЕХИЯ",
    "ГЕРМАНИЯ",
    "ДЖИБУТИ",
    "ДАНИЯ",
    "ДОМИНИКА",
    "ДОМИНИКАНСК.РЕСП.",
    "АЛЖИР",
    "ЭКВАДОР",
    "ЭСТОНИЯ",
    "ЕГИПЕТ",
    "ЗАПАДНАЯ САХАРА",
    "ЭРИТРЕЯ",
    "ИСПАНИЯ",
    "ЭФИОПИЯ",
    "ФИНЛЯНДИЯ",
    "ФИДЖИ",
]

AREA_STOPWORDS = ["сельское поселение", "городское поселение", "район", "округ"]

GROUP_STOPWORDS = [
    "сельское поселение",
    "городское поселение",
    "округ",
    "город",
    "муниципальное образование",
    "Муниципальный",
    "Администрация",
    " МО",
    "МО ",
]

REGEX_PATTERN = r"[\"!?\u2665\u2022()|,.-:]"

REPLACEMENT_STRING = " "
