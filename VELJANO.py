# -*- coding: utf-8 -*-
"""
Veljano — Справочник языка
Kivy 2.3.1 + KivyMD 2.0.0
Запуск: python main.py
"""

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ListProperty
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.appbar import MDTopAppBar, MDTopAppBarTitle

# ============================================================
#  ДАННЫЕ ЯЗЫКА
# ============================================================

PHONETICS = [
    ("Алфавит (A1)", [
        ("A",   "[a]",       "aj"),
        ("B",   "[b]",       "baj"),
        ("V",   "[β]",       "vaj"),
        ("W",   "[w]",       "waj"),
        ("G",   "[g]",       "gaj"),
        ("D",   "[d]",       "daj"),
        ("E",   "[ə]",       "ej"),
        ("Ż",   "[ʒ]",       "żaj"),
        ("Z",   "[z]",       "zaj"),
        ("Ï",   "[ʲi]",      "ïj"),
        ("J",   "[j]",       "jod"),
        ("K",   "[k]",       "kaj"),
        ("L",   "[l]",       "lej"),
        ("M",   "[m]",       "mej"),
        ("N",   "[n]",       "nej"),
        ("O",   "[o]",       "oj"),
        ("P",   "[p]",       "paj"),
        ("R",   "[ʀ] / [ʁ]", "raj"),
        ("S",   "[s]",       "saj"),
        ("T",   "[t]",       "taj"),
        ("U",   "[u]",       "uj"),
        ("F",   "[ɸ]",       "faj"),
        ("H",   "[h]",       "haj"),
        ("C",   "[ts]",      "caj"),
        ("Ĉ",   "[tɕ]",      "ĉej"),
        ("Ŝ",   "[ʃ]",       "ŝaj"),
        ("Ş",   "[ɕ]",       "şej"),
        ("Y",   "[ɨ]",       "yj"),
        ("I",   "[ʲ] / [ː]", "lände"),
        ("È",   "[ɛ]",       "förd ej"),
    ]),
    ("Буква i (A1)", [
        "• Никогда не читается.",
        "• После согласной — смягчает эту согласную.",
        "• После гласной — удлиняет эту гласную.",
    ]),
    ("JÏV (A1)", [
        "Гласные с двумя точками (это НЕ умлауты!) смягчают перед собой гласную.",
        ("Ä", "[ʲæ]", "jümüşakwa aj"),
        ("Ö", "[ʲɵ]", "jümüşakwa oj"),
        ("Ü", "[ʲʉ]", "jümüşakwa uj"),
        ("Ï", "[ʲi]", "ij"),
        ("Ë", "[ʲe]", "jümüşakwa ej"),
    ]),
    ("Правило редукции (A1)", [
        "Безударные буквы иногда редуцируются и читаются как ə.",
    ]),
    ("Дополнительные буквы (A2)", [
        ("ğ", "[ɦ]",  "(ğej)"),
        ("x", "[ks]", "(ïxej)"),
        ("Ô", "—",    "(förd oj) — не читается, обозначает м.р."),
        ("ñ", "[ŋ]",  ""),
    ]),
    ("Самые редкие буквы", [
        ("â", "(förd aj)", "— не читается, обозначает ж.р."),
        ("Œ", "[œ]",       "(latïnwa œ)"),
    ]),
    ("Устаревшие буквы (C2)", [
        ("ʍ", "[ʍ]"), ("ρ", "[ɾ]"), ("ñ", "[ŋ]"), ("ž", "[ʒ]"),
    ]),
    ("Полная транскрипция", [
        "A [a], b [b], v [β], w [w], g [g], gh [ɦ], d [d], ż [ʒ], z [z], ï [ʲi]",
        "j [j], k [k], l [l], m [m], n [n], o [o], p [p], r [ɹ] / [ʀ]",
        "s [s], zs [s]~[z], t [t], dt [t]~[d], u [u], f [ɸ], h [h]",
        "c [ts], ci / č [tɕ], ŝ [ʃ̻], ş [ɕ], e [ə], y [ɨ]",
        "JÏV: ë [ʲe], ü [ʲʉ], ö [ɵ], ä [ʲæ], ï [ʲi]",
    ]),
    ("Строгие правила (ЗАКОН)", [
        "1) JÏV — гласные с точками смягчают предыдущую согласную.",
        "2) Буква j читается ВСЕГДА раздельно, не сливаясь с согласной.",
        "3) Буква ŝ читается НЕ как русская ш. Строго: ʃ̻",
        "",
        "ЗАКОН: j не смягчает предыдущую согласную.",
        "На кириллице j = [й], НИКОГДА не ь.",
        "Примеры: Djomo [дйомо], Lajdwï [лайдви]",
    ]),
    ("Два акцента", [
        "ЛЕСНОЙ:",
        "• все гласные читаются чётко, без редукции",
        "• e всегда [ə]",
        "• j как [ʝ], короче русского «й»",
        "• w слабо, между гласной и [w]",
        "",
        "СЛАВЯНСКИЙ:",
        "• редукция максимальная",
        "• j как [j] или [ĭ]",
        "• w чётко, как [β]",
    ]),
]

DEFINITIONS = [
    ("Базовые сокращения", [
        ("Prasuffïx (PS)", "суффикс, определяющий лицо/инфинитив"),
        ("Önprasuffïx (OPS)", "суффикс, ставится ВСЕГДА после PS"),
        ("Jügprasuffïx (JPS)", "суффикс, ставится ВСЕГДА перед PS"),
    ]),
    ("Структурные термины", [
        ("Jügfïx", "приставка, перед корнем"),
        ("Suffïx", "любой суффикс"),
        ("Glagolisuffïx (GS)", "суффикс, что слово — глагол"),
        ("Ajnjugfïx", "приставка отрицания"),
        ("Slemïx", "слияние букв (-)"),
        ("Lëxïsuffïx", "словообразовательный суффикс"),
        ("Grammsuffïx", "формообразующий суффикс"),
        ("Ümcajto", "уточнительные времена"),
        ("JÏV", "гласные с точками, смягчают согласную"),
    ]),
    ("Времена", [
        ("Secajme", "прошедшее совершённое"),
        ("Ajnsecajme", "прошедшее несовершённое"),
        ("Secajüne", "будущее совершённое"),
        ("Ajnsecajüne", "будущее несовершённое"),
    ]),
    ("Глагольные термины", [
        ("Gïgkeglagoli", "глагольная частица"),
        ("Gïgke", "частица"),
        ("Modaliwa glagoli (MG)", "модальный глагол"),
        ("Lïnfïne", "особая форма глагола после MG"),
        ("Ïnfglagoli", "инфинитив"),
    ]),
]

NOTATION = [
    ("Строгие обозначения", [
        ("()",   "корень"),
        ("[]",   "PS"),
        ("[[]]", "JPS"),
        ("{{}}", "OPS"),
        ("{}",   "приставка"),
        ("<>",   "окончание"),
    ]),
    ("Примеры разбора", [
        "lajdwïn (я любил): (lajd) [[w]] [ï] {{n}}",
        "Dajwïns (я сделал): (daj) [[w]] [ï] {{ns}}",
        "Dajwïs (делаю сейчас): (daj) [[w]] [ï] {{s}}",
        "plyklwï (говорить): (plykl) [[w]] [ï]",
    ]),
]

GRAMMAR = [
    ("Глаголы: спряжение (A1)", [
        "Формула: [Корень] + w + [PS]",
        "GS = суффикс w, никогда не меняется.",
        "Инфинитив: -o (физические), -ï (моральные).",
        "Исключение: tajtwa",
        ("1 лицо", "-ï → Lajdwï, gwï"),
        ("2 лицо", "-u → Lajdwu, gwu"),
        ("3 лицо", "-e → Lajdwe, gwe"),
        "Мн.ч. без подлежащего: -ïz / -uz / -ez",
        "Мн.ч. с подлежащим: -ï / -u / -e",
        "Группа+говорящий: -ïm / -um / -em",
    ]),
    ("Глаголы: 12 времён", [
        ("Наст. простое", "—", "Ï lajdwï twï"),
        ("Наст. моментное", "-s", "Ï dajwïs ejzwo"),
        ("Cajme", "-n", "Ï dajwïn ejzwo"),
        ("Gëcajme", "gë- + -n", "Ïj gëdajwïn"),
        ("Secajme", "-ns", "Ïj dajwïns"),
        ("Gësecajme", "gë- + -ns", "Ï gëvïzzwïns"),
        ("Прош. давнее", "любое + da(П)", "Ïj wïns ejzwo je"),
        ("Прош. сейчашнее", "любое + je(П)", "Ï wïns ejzwo je"),
        ("Наст. моментное быстрое", "-s + je(П)", "Ï wïs ejzwo je"),
        ("Cajüne", "-jü", "Ï wïjü ejzwo"),
        ("Secajüne", "-j", "Ï wïj ejzwo"),
        ("Буд. сейчашнее", "gë-", "Ïj gëwï ejzwo"),
    ]),
    ("Objektïnwa glagoli (A1)", [
        "Глаголы, включающие объект. Формула: [Корень] + w + [PS]",
        "Пример: lëssïino → lëssïnwo",
        "3 частицы:",
        ("Nai", "включение"),
        ("Hei", "выключение"),
        ("Aus / auz", "полное закрытие"),
    ]),
    ("Wïllwï / Javïnwo (A1)", [
        "Сокращённые формы:",
        ("1", "Wïllwï: 'llwï | Javïnwo: 'nwï"),
        ("2", "Wïllwï: 'llwu | Javïnwo: 'nwu"),
        ("3", "Wïllwï: 'llwe / 'll | Javïnwo: 'nwe / 'n"),
        "Wïllwï — состояние. Javïnwo — место.",
    ]),
    ("Местоимения: базовые (A1)", [
        "Ед.ч.:",
        ("1", "Ï"),
        ("2", "Tü (неформ.) / Vü (вежл.)"),
        ("3", "Hï / Šï / Ït / Et / At"),
        "Мн.ч.:",
        ("1", "Ïiz"),
        ("2", "Tüz / Vüz"),
        ("3", "Zïi"),
    ]),
    ("Местоимения: дополнительные (A2)", [
        ("1 м.р.", "Ïj"), ("1 ж.р.", "Jï"),
        ("2 м.р.", "Tüo / Vüo"), ("2 ж.р.", "Tüa / Vüa"),
        ("1 мн.", "Ïjz / Jïz"),
        ("2 мн.", "Tüoz / Vüoz / Tüaz / Vüaz"),
        ("3 высш. м.", "Hïz"), ("3 высш. ж.", "Šïz"),
        ("3 предм. м.", "Ac"), ("3 предм. ж.", "Ïc"), ("3 предм. ср.", "Ec"),
        "Дв.ч. 1 лицо: zhö",
    ]),
    ("Местоимения в В.п. (A1)", [
        "1) Оканчивается на согласную → + wo / wï",
        "2) Оканчивается на гласную → гласная убирается, + wo / wï",
        "Исключения: Ïnwï/Ïnwo, Jïnwï/Jïnwo, nwï/nwo, zwï/zwo",
        "3) Мн.ч. на z, предпоследняя гласная → гласная убирается",
        "4) Мн.ч. на согласную → + wo / wï",
        "5) Доп. В.п. (B1): mwï / mwo (я)",
    ]),
    ("Родительный падеж (A2)", [
        "Местоимения не меняются. Исключения:",
        ("Ï / Ïj / Jï →", "mï"),
        ("Ïiz →", "mïiz"),
        ("Tü →", "Tï"),
        ("Vü →", "Vï"),
        ("Vüz / Tüz →", "Nï"),
    ]),
    ("Притяжательный падеж (A2)", [
        "М.р. ед.: -mo-", "Ж.р. ед.: -ma-", "Ср.р. ед.: -me",
        "М.р. мн.: -moz-", "Ж.р. мн.: -maz-", "Ср.р. мн.: -me",
    ]),
    ("Акцентное притяжение (4.11)", [
        ("Ï / Ïj / Jï", "De manï"),
        ("Ïiz", "De manïz"),
        ("Tü", "De tanï"),
        ("Tüz", "De tanïz"),
        ("Vü / Vüz", "De vanïz"),
        ("Hï / Šï", "De hanï"),
        ("Šï", "De šanï"),
    ]),
    ("Артикли (A1-A2)", [
        "Определённые:",
        ("М.р. предм.", "Lä"), ("Ж.р. предм.", "Lïi"), ("Ср.р. предм.", "Le"),
        ("М.р. высш.", "Loi"), ("Ж.р. высш.", "Loij"), ("Ср.р. высш.", "Lei"),
        "Неопределённые:",
        ("j после гласной", "Jün"), ("остальные", "Ün"), ("мн.ч.", "Jïn"),
        "Отрицательные:",
        ("М.р.", "Naj"), ("Ж.р.", "Nïij"), ("Ср.р.", "Nej"),
    ]),
    ("Существительные (A2)", [
        "M-pe (И.п.):",
        ("М.р. предм.", "-o / -e / -ô"),
        ("Ж.р. предм.", "-ï / -i / -a"),
        ("Ср.р. предм.", "—"),
        ("М.р. высш.", "-o"),
        ("Ж.р. высш.", "-ï / -i / -a"),
        ("Ср.р. высш.", "-e / -ô / -o"),
        "",
        "Akkjuzatwa-pe (В.п.):",
        "Инфинитив на -o → -wo",
        "Инфинитив на -ï → -wï",
        "Суффикс ïn: корень на 2 согласные, v, f, w",
        "",
        "T-pe: + -t в конце",
        "N-pe: корень на -n → m, иначе + -n",
        "Förd-pe: o/e/∅ → a, ï/i/a → ï",
        "Faicio-pe: O→ö, A→ä, E→ë, ∅→ö, I/ï→ï",
        "Avairciojo-pe: Faicio-pe + j",
    ]),
    ("Предикативы Najn / Kajn", [
        "Najn (A1) — нет в конкретный момент.",
        "Kajn (A2) — нет постоянно.",
        ("Najnwï së", "Не находится"),
        ("Kajnwï së", "Не быть"),
        ("Kajnwo", "Ничего не делать"),
        ("Najnwo", "Убирать"),
    ]),
    ("Числительные (A1)", [
        ("1", "adjam"), ("2", "djev"), ("3", "troja"),
        ("4", "cijöt"), ("5", "fjati"), ("6", "zejzs"),
        ("7", "zïivzs"), ("8", "jod"), ("9", "nojn"),
        ("10", "vfön"), ("100", "sjë"), ("1000", "mwa"),
        "11-19: jëlif, djölif, trolif, cijölif, fjälif, sjëlif, zïivli, jölif, njëlif",
        "Полная форма 11-19: [Единица] + vfön",
        "Десятки: [число] + lïhi",
        "Исключения: 30 trojlïhi, 60 zejzlïhi, 70 zïivzlïhi",
        "Fördciöto (1/2/3): jati, diva, trï",
    ]),
    ("Предлоги местные", [
        ("Ïn / Ïm / Ïns", "в — внутри"),
        ("Cu / Cum / Cuns", "в / на — открытое"),
        ("Äw / Äwn / Äwns", "в — транспорт"),
        ("A / Am / Ans", "в — время"),
        ("An / Am / Ans", "на / после — вертикаль"),
        ("Ön / Öm / Öns", "на — горизонталь"),
        ("Cï / Cïm / Cïns", "вдоль стены"),
        ("Ca / Cam / Cans", "вдоль улицы"),
        ("Kaj", "у"),
        ("Baj / Bajm / Bajs", "рядом с"),
        ("Ce / Cem / Cens", "по"),
        ("Jüg / Jüg / Jügs", "под / перед"),
        ("App / Apps", "вверх"),
        ("Ïss / Ïssn", "вниз"),
        ("Lë / Lëm / Lëns", "слева"),
        ("Rë / Rëm / Rëns", "справа"),
        ("Ïr / Ïrn / Ïrs", "у"),
        ("Ïir / Ïirn / Ïirs", "впившийся"),
    ]),
    ("Предлоги без форм", [
        ("Ojne", "без"), ("A-a", "между"),
        ("Cur", "похожий на"), ("De", "словообразование"),
        ("Mït", "вместе с"), ("Dïm", "делить на"),
        ("Für", "для"), ("Kojlo", "вокруг / целый"),
        ("Kojlo", "каждый"), ("Naj", "новый"),
        ("Adiü", "через"), ("Gadiü", "чувствовать"),
        ("Najn", "нет"), ("Kajne", "нет вообще"),
        ("Ïrïm", "на кого-то"), ("Ïrïns", "от кого-то"),
    ]),
    ("Суффиксы", [
        ("-sïin-", "предмет внутри предмета"),
        ("-od-", "здание / место"),
        ("-z- / -az-", "магазин"),
        ("-àt-", "человек"),
        ("-lat-", "профессия (ин. слова)"),
        ("-àl-", "говорящий на языке"),
        ("-us-", "соединение пары"),
        ("-ïic-", "создание ж.р."),
        ("-ovïci- / -vïci-", "русская фамилия м.р."),
        ("-ovn-", "русская фамилия ж.р."),
        ("-ïick-", "грубое (училка)"),
        ("-ert-", "предмет справа"),
        ("-elit-", "предмет слева"),
        ("-opp-", "предмет сверху"),
        ("-ov-", "вэльянская фамилия"),
        ("-av-", "человек по характеру"),
        ("-trak-", "чердак"),
        ("-af-", "предмет для еды"),
        ("-ïjf-", "результат действия"),
    ]),
    ("Наречия", [
        "Образование: убрать GS и PS, вставить -et.",
        ("Lui", "хорошо"), ("Fjat", "плохо"),
        ("Afrodïtet", "красиво"), ("Rodet", "красно"),
        ("Vïrïdet", "зелено"), ("Janet", "бело"), ("Ïnet", "черно"),
    ]),
    ("Прилагательные", [
        "Формула: [Корень] + [GS] + [a]",
        "Суффикс -a не меняется.",
        "Прошедшее: не -n → +n; на -n → n→m.",
        ("Vïrïdïnwa", "зелёный"), ("Rotwa", "красный"),
        ("Luïnwa", "хороший"), ("Fjatwa", "плохой"),
        ("Bonwa", "качественный"), ("Carulïnwa", "синий"),
    ]),
    ("Приветствия и этикет", [
        ("Vejl!", "Привет!"),
        ("Vejl-barkajvo!", "Здравствуйте!"),
        ("Ajo!", "Пока!"),
        ("Ajo-kajvo!", "До свидания!"),
        ("Bon tun!", "Добрый день!"),
        ("Bon matyna!", "Доброе утро!"),
        ("Bon marhen!", "Добрый вечер!"),
        ("Bon noŝi!", "Доброй ночи!"),
        ("Lui!", "Хорошо!"),
        ("Ejz'll lui!", "Это хорошо!"),
        ("Ejs veljanto?", "Как дела?"),
    ]),
    ("Топ-10 примеров с В.п.", [
        "1.  Ï lajdwï djomwï",
        "2.  Tü lajdwun ïnwï",
        "3.  Ï wïns ejzwo",
        "4.  Kajto vïzzwe stojlïnwï",
        "5.  Ï lejnwïns tjemwï",
        "6.  Tü auzlejzwuns lïbrïnwï",
        "7.  Ï vajzwï twï",
        "8.  Hï ajnwajzwe ïnwï",
        "9.  Ejz'll djomo",
        "10. Ï wajzwï hwï",
    ]),
]

LEXICON = [
    ("Местоимения", [
        ("Ï", "я"), ("Ïj", "я (высш. м.)"), ("Jï", "я (высш. ж.)"),
        ("Tü", "ты"), ("Vü", "Вы"), ("Hï", "он"), ("Šï", "она"),
        ("At", "он (предм.)"), ("Ït", "она (предм.)"), ("Et", "оно"),
        ("Ïiz", "мы"), ("Tüz", "вы"), ("Vüz", "Вы (мн.)"), ("Zïi", "они"),
        ("Kajnéjsoi", "никто"), ("Kajnéjs", "ничто"),
        ("Èlöi", "кто-то"), ("Èli", "что-то"),
    ]),
    ("Глаголы A-D", [
        ("Änwo", "плакать"), ("Äwlojantwo", "ездить на машине"),
        ("Adiügwo", "переходить"), ("Adiüwo", "переделать"),
        ("Ajnlajdwï", "не любить"), ("Ajnwo", "не делать"),
        ("Appzugwo", "ехать на лифте"), ("Arbajtwï", "работать"),
        ("Bëżwï", "бежать"), ("Bërëgïnwo", "беречь"),
        ("Blümwo", "пить"), ("Bonwa", "быть красивым"),
        ("Brawo", "брать"), ("Cajnwo", "чертить"),
        ("Ciötwï", "считать"), ("Dajwo", "делать"),
        ("Djenkwï", "думать"), ("Djomwo", "строить"),
        ("Dürwo hei", "закрывать дверь"), ("Dürwo nai", "открывать дверь"),
        ("Dürwo aus", "закрывать на замок"),
    ]),
    ("Глаголы F-K", [
        ("Farwo", "водить"), ("Fajwo", "жевать"),
        ("Fïlwo", "летать"), ("Föŝtejwï", "понимать"),
        ("Gadiü", "быть в чувстве"), ("Ganwo", "бежать"),
        ("Gëbwo", "брать"), ("Gëpälwïs", "получить"),
        ("Glacwo", "мыть"), ("Gwo", "двигаться"),
        ("Ïjwo", "использовать"), ("Ïmgwo", "входить"),
        ("Ïnsgwo", "выходить"), ("Jansonwï", "спать"),
        ("Jesswo", "кормить"), ("Jesswo së", "есть"),
        ("Kajnwo", "ничего не делать"), ("Kalikwo", "класть"),
        ("Kapwo", "копать"), ("Kjanwo", "уметь"),
        ("Kulliwo", "писать"), ("Kïllwo", "убивать"),
    ]),
    ("Глаголы L-P", [
        ("Lajdwï", "любить"), ("Lecojwï", "читать"),
        ("Lecwo", "сочинять"), ("Lejnwï", "учиться"),
        ("Lïigwï", "лететь"), ("Lïmwo", "красить"),
        ("Lïtwo", "создавать"), ("Malliwï", "рисовать"),
        ("Marwo", "умереть"), ("Mïnwo", "звонить"),
        ("Nadwï / Najdwï", "хотеть"), ("Navïnwo", "исчезать"),
        ("Nożwo", "резать"), ("Pajwï", "ошибаться"),
        ("Pälwï", "иметь"), ("Pälülwï", "учить"),
        ("Pjekwï", "просить"), ("Plaswo", "лежать"),
        ("Plyklwï", "говорить"),
    ]),
    ("Глаголы R-Z", [
        ("Rajswï", "читать"), ("Remwo", "грызть"),
        ("Sakwo", "мыть (миски)"), ("Sejtwï", "чувствовать"),
        ("Sohwï", "хотеть узнать"), ("Sonwï", "спать"),
        ("Stojlwo", "сидеть за столом"), ("Stojwo", "ставить"),
        ("Stojwo së", "стоять"), ("Tajtwa", "верить"),
        ("Tunwo", "проводить досуг"), ("Two", "идти"),
        ("Vajzwï", "знать"), ("Veljanwï", "говорить по-вэльянски"),
        ("Vïzzwï", "видеть"), ("Vokaliwï", "петь"),
        ("Wajswo", "мыть"), ("Wajswo ön së", "мыться"),
        ("Wo", "делать"), ("Wïllwï", "быть"),
        ("Woikwo së", "гулять"), ("Zagwo", "говорить"),
        ("Żyhavïnwo", "пылесосить"),
    ]),
    ("Существительные: общая лексика", [
        ("veljano", "вэльянский язык"), ("djomo", "дом"),
        ("kajto", "кот"), ("kajta", "кошка"),
        ("jundo / jündo", "собака"), ("wajsa", "вода"),
        ("kullï", "ручка"), ("arkullï", "карандаш"),
        ("mülo", "мыло"), ("lïbro / lïbra", "книга"),
        ("jesso", "еда"), ("brodo", "хлеб"),
        ("mlako", "молоко"), ("kojfï", "кофе"),
        ("liŝlïno", "сок"), ("cijaj", "чай"),
        ("äwlojanto", "машина"), ("taxï", "такси"),
    ]),
    ("Существительные: лингвистика", [
        ("lekswï", "словарь"), ("leco", "текст"),
        ("gramatïkje", "грамматика"), ("suffajks", "суффикс"),
        ("ausvordo", "окончание"), ("ïje", "предмет"),
        ("m-pe", "именительный"), ("akkjuzatwa-pe", "винительный"),
        ("t-pe", "инструментальный"), ("faicio-pe", "местный"),
        ("n-pe", "притяжательный"),
        ("vordto", "слово"), ("ïnvordto", "слог"),
        ("pravvordto", "корень"), ("cajte", "время"),
        ("glagolisïino", "глагол"),
        ("fördaglagolisïino", "прилагательное"),
        ("jajnpravï", "исключение"),
        ("djaloko", "диалог"),
        ("fïzïkïica", "физика"), ("biölogïica", "биология"),
        ("lïtëraturïica", "литература"),
        ("awsplwklanto", "иностранный язык"),
        ("maoteplwklanto", "родной язык"),
        ("fonemàte", "фонетика"), ("foneme", "фонема"),
        ("ojneije", "местоимение"), ("ijo", "вещь"),
    ]),
    ("Существительные: быт", [
        ("arbajtàto", "рабочий"), ("dżuŝeciï", "шприц"),
        ("żyhavo", "пылесос"), ("mïsko", "миска"),
        ("uno", "начало"), ("banano", "банан"),
        ("nosoko", "носок"), ("nożo", "нож"),
        ("nożïica", "ножница"), ("ebpżŝdtjomo", "погреб"),
        ("havo", "пыль"), ("hoha", "одеяло"),
        ("mato", "матрас"), ("vïn", "шуруп"),
        ("mamo", "еда (бытовая)"), ("vïnta / vïnto", "зима"),
        ("fja", "диван"), ("bjata", "кровать"),
        ("fofa", "мешок"), ("buba", "подушка"),
        ("amo", "кухня"), ("noŝi", "ночь"),
        ("tajsa", "рука / нога"), ("istajsa", "нога"),
        ("avptajsa", "рука"), ("kojko", "колено"),
        ("foto", "фото"), ("papïi", "бумага"),
        ("vïlïks", "вилка"), ("ŝtajko", "розетка"),
        ("tajzo", "чашка"), ("zalato", "салат"),
        ("züipo", "суп"),
    ]),
    ("Существительные: транспорт, город", [
        ("mëtro", "метро"), ("ŝtrajto", "улица"),
        ("buso", "автобус"), ("tajksï", "такси"),
        ("cug", "поезд"), ("djomàto", "город"),
        ("ŝujla", "школа"), ("bajsajo", "мост"),
        ("appcugo", "лифт"), ("bëröza", "берёза"),
        ("stujlïika", "скамейка"), ("zlomöno", "бензин"),
        ("sëjpo", "серп"), ("murajvïo", "муравей"),
        ("krykva", "кирпич"),
    ]),
    ("Существительные: наука, медицина", [
        ("plüs", "плюс"), ("majnus", "минус"),
        ("dïskrïmïnante", "дискриминант"),
        ("formule", "формула"), ("tjoreme", "теорема"),
        ("funkciï", "функция"), ("awsnoj", "число"),
        ("moduli", "модуль"), ("reno", "степень"),
        ("kreto", "корень (матем.)"),
        ("ràke", "рак (опухоль)"), ("kòre", "сердце"),
        ("pasïko", "член (мед.)"),
        ("bïcisïino", "воспаление"), ("bïciojo", "диагноз"),
        ("awtïps", "аутизм"), ("ŝïzofrenja", "шизофрения"),
        ("noso", "нос"), ("lečyne", "лицо"),
        ("rajo", "кровь"),
    ]),
    ("Существительные: музыка, архитектура", [
        ("zejzssolö", "струна"), ("salo", "палец"),
        ("cajsalo", "мизинец"), ("jajsalo", "безымянный"),
        ("majsalo", "средний"), ("ajsalo", "указательный"),
        ("pajsalo", "большой"), ("gjïv", "гриф"),
        ("kapïteli", "капитель"), ("ehïno", "эхин"),
        ("abako", "абака"), ("volüta", "волюта"),
        ("ïntazïe", "энтазис"), ("šlüze / šlüzo", "шлюз"),
        ("djomtrako", "чердак"), ("kojlotenco", "циркуль"),
        ("čiötsïinodo", "куб"), ("kojlàtodo", "шар"),
        ("zejzssïino", "шестиугольник"),
    ]),
    ("Существительные: мифология, география, имена", [
        ("aljano", "бог"), ("aljanso", "божество"),
        ("mil", "бог света"), ("unsu-dojо", "дух-хранитель дома"),
        ("majo", "магия"), ("majkïps", "оккультизм"),
        ("rossïja", "Россия"), ("dojtŝciland", "Германия"),
        ("dżonguo", "Китай"), ("amerik", "Америка"),
        ("krasnogórsk", "Красногорск"), ("klín", "Клин"),
        ("dubná", "Дубна"),
        ("artëmij", "Артемий"), ("david", "Давид"),
        ("dima", "Дима"), ("igor", "Игорь"),
        ("sajša", "Саша"), ("grïša", "Гриша"),
        ("maks", "Макс"),
    ]),
    ("Существительные: профессии, люди", [
        ("ŝulàto", "учитель"), ("ïjàto", "пользователь"),
        ("palülat", "репетитор"), ("auslänŝàto", "иностранец"),
        ("karulgebàto", "собиратель кораллов"),
        ("matadora / matadoro", "убийца"),
        ("lecàto", "сочиняющий"), ("arbajtàto", "рабочий"),
        ("figlat", "шут"), ("afïn", "король"),
    ]),
]

# ============================================================
#  KIVY UI
# ============================================================

KV = """
<HomeScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.96, 0.96, 0.96, 1
        MDTopAppBar:
            type: "small"
            MDTopAppBarTitle:
                text: "Veljano"
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height
                MDLabel:
                    text: "Справочник языка"
                    halign: "center"
                    font_style: "Title"
                    size_hint_y: None
                    height: dp(50)
                MDButton:
                    style: "filled"
                    size_hint: 1, None
                    height: dp(60)
                    md_bg_color: 0.13, 0.59, 0.95, 1
                    on_release: app.open_section("Фонетика", app.phonetics)
                    MDButtonText:
                        text: "🔤  Фонетика"
                MDButton:
                    style: "filled"
                    size_hint: 1, None
                    height: dp(60)
                    md_bg_color: 0.61, 0.15, 0.69, 1
                    on_release: app.open_section("Определения", app.definitions)
                    MDButtonText:
                        text: "📘  Определения"
                MDButton:
                    style: "filled"
                    size_hint: 1, None
                    height: dp(60)
                    md_bg_color: 0.38, 0.49, 0.55, 1
                    on_release: app.open_section("Обозначения", app.notation)
                    MDButtonText:
                        text: "🔣  Обозначения"
                MDButton:
                    style: "filled"
                    size_hint: 1, None
                    height: dp(60)
                    md_bg_color: 0.30, 0.69, 0.31, 1
                    on_release: app.open_section("Грамматика", app.grammar)
                    MDButtonText:
                        text: "📖  Грамматика"
                MDButton:
                    style: "filled"
                    size_hint: 1, None
                    height: dp(60)
                    md_bg_color: 1.0, 0.34, 0.13, 1
                    on_release: app.open_section("Лексика", app.lexicon)
                    MDButtonText:
                        text: "📚  Лексика"

<SectionScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.96, 0.96, 0.96, 1
        MDTopAppBar:
            type: "small"
            MDTopAppBarTitle:
                text: root.section_name
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "arrow-left"
                    on_release: app.go_home()
        MDScrollView:
            MDBoxLayout:
                id: section_box
                orientation: 'vertical'
                padding: dp(15)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

<TopicScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: 0.96, 0.96, 0.96, 1
        MDTopAppBar:
            type: "small"
            MDTopAppBarTitle:
                text: root.topic_title
            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "arrow-left"
                    on_release: app.go_back()
        MDScrollView:
            MDBoxLayout:
                id: topic_box
                orientation: 'vertical'
                padding: dp(15)
                spacing: dp(8)
                size_hint_y: None
                height: self.minimum_height
"""


class HomeScreen(Screen):
    pass

class SectionScreen(Screen):
    section_name = StringProperty("")

class TopicScreen(Screen):
    topic_title = StringProperty("")


class VeljanoApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.phonetics = PHONETICS
        self.definitions = DEFINITIONS
        self.notation = NOTATION
        self.grammar = GRAMMAR
        self.lexicon = LEXICON

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(SectionScreen(name="section"))
        sm.add_widget(TopicScreen(name="topic"))
        self.sm = sm
        return sm

    def go_home(self):
        self.sm.current = "home"

    def go_back(self):
        self.sm.current = "section"

    def open_section(self, name, data):
        sec = self.sm.get_screen("section")
        sec.section_name = name

        box = sec.ids.section_box
        box.clear_widgets()

        for i, (title, _) in enumerate(data):
            btn = MDButton(
                style="filled",
                size_hint=(1, None),
                height=dp(55),
                md_bg_color=(0.30, 0.69, 0.31, 1),
                on_release=lambda x, idx=i, d=data: self.open_topic(idx, d),
            )
            btn.add_widget(MDButtonText(text=title))
            box.add_widget(btn)

        self.sm.current = "section"

    def open_topic(self, idx, data):
        title, content = data[idx]
        topic = self.sm.get_screen("topic")
        topic.topic_title = title

        box = topic.ids.topic_box
        box.clear_widgets()

        for line in content:
            if isinstance(line, tuple):
                cells = [str(c) for c in line]
                text = "  |  ".join(cells)
                lbl = MDLabel(
                    text=text,
                    size_hint_y=None,
                    height=dp(35),
                    font_style="Body",
                )
            elif line == "":
                lbl = MDLabel(text="", size_hint_y=None, height=dp(10))
            else:
                # Заголовки (строки с ":" в конце или короткие с заглавной)
                is_title = (line.endswith(":") or 
                            (len(line) < 50 and 
                             line[0].isupper() and 
                             "—" not in line and 
                             "." not in line))
                if is_title:
                    lbl = MDLabel(
                        text=line,
                        size_hint_y=None,
                        height=dp(40),
                        font_style="Title",
                    )
                else:
                    lbl = MDLabel(
                        text=line,
                        size_hint_y=None,
                        height=dp(35),
                        font_style="Body",
                    )
            box.add_widget(lbl)

        self.sm.current = "topic"


if __name__ == "__main__":
    VeljanoApp().run()
