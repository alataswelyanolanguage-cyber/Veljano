# -*- coding: utf-8 -*-
"""Veljano — Справочник языка (Kivy)"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

# ---------- ДАННЫЕ ----------
PHONETICS = [
    ("Алфавит (A1)", [
        ("A","[a]","aj"),("B","[b]","baj"),("V","[β]","vaj"),("W","[w]","waj"),
        ("G","[g]","gaj"),("D","[d]","daj"),("E","[ə]","ej"),("Ż","[ʒ]","żaj"),
        ("Z","[z]","zaj"),("Ï","[ʲi]","ïj"),("J","[j]","jod"),("K","[k]","kaj"),
        ("L","[l]","lej"),("M","[m]","mej"),("N","[n]","nej"),("O","[o]","oj"),
        ("P","[p]","paj"),("R","[ʀ]/[ʁ]","raj"),("S","[s]","saj"),("T","[t]","taj"),
        ("U","[u]","uj"),("F","[ɸ]","faj"),("H","[h]","haj"),("C","[ts]","caj"),
        ("Ĉ","[tɕ]","ĉej"),("Ŝ","[ʃ]","ŝaj"),("Ş","[ɕ]","şej"),("Y","[ɨ]","yj"),
        ("I","[ʲ]/[ː]","lände"),("È","[ɛ]","förd ej"),
    ]),
    ("Буква i (A1)", [
        "• Никогда не читается.",
        "• После согласной — смягчает.",
        "• После гласной — удлиняет.",
    ]),
    ("JÏV (A1)", [
        ("Ä","[ʲæ]","jümüşakwa aj"),
        ("Ö","[ʲɵ]","jümüşakwa oj"),
        ("Ü","[ʲʉ]","jümüşakwa uj"),
        ("Ï","[ʲi]","ij"),
        ("Ë","[ʲe]","jümüşakwa ej"),
    ]),
    ("Редукция (A1)", ["Безударные читаются как ə."]),
    ("Доп. буквы (A2)", [
        ("ğ","[ɦ]","(ğej)"),("x","[ks]","(ïxej)"),
        ("Ô","—","не читается, м.р."),("ñ","[ŋ]",""),
    ]),
    ("Редкие буквы", [("â","förd aj","ж.р."),("Œ","[œ]","")]),
    ("Устаревшие (C2)", [("ʍ","[ʍ]"),("ρ","[ɾ]"),("ñ","[ŋ]"),("ž","[ʒ]")]),
]

DEFINITIONS = [
    ("PS, OPS, JPS", [
        ("Prasuffïx (PS)","лицо/инфинитив"),
        ("Önprasuffïx (OPS)","после PS"),
        ("Jügprasuffïx (JPS)","перед PS"),
    ]),
    ("Термины", [
        ("Jügfïx","приставка"),("Suffïx","суффикс"),
        ("Glagolisuffïx (GS)","суффикс глагола"),
        ("Ajnjugfïx","отрицание"),
        ("Slemïx","слияние (-)"),
        ("Ümcajto","уточнит. времена"),
    ]),
    ("Времена", [
        ("Secajme","прош. соверш."),("Ajnsecajme","прош. несоверш."),
        ("Secajüne","буд. соверш."),("Ajnsecajüne","буд. несоверш."),
    ]),
    ("Глагольные", [
        ("Gïgkeglagoli","глаг. частица"),
        ("Modaliwa glagoli (MG)","модальный глагол"),
        ("Lïnfïne","форма после MG"),
        ("Ïnfglagoli","инфинитив"),
    ]),
]

NOTATION = [
    ("Обозначения", [
        ("()","корень"),("[]","PS"),("[[]]","JPS"),
        ("{{}}","OPS"),("{}","приставка"),("<>","окончание"),
    ]),
    ("Примеры", [
        "lajdwïn: (lajd) [[w]] [ï] {{n}}",
        "Dajwïns: (daj) [[w]] [ï] {{ns}}",
        "plyklwï: (plykl) [[w]] [ï]",
    ]),
]

GRAMMAR = [
    ("Глаголы: спряжение (A1)", [
        "Формула: [Корень] + w + [PS]",
        "Инфинитив: -o / -ï",
        ("1","-ï → Lajdwï"),("2","-u → Lajdwu"),("3","-e → Lajdwe"),
        "Мн.ч. без подл.: -ïz / -uz / -ez",
        "Мн.ч. с подл.: Ïiz lajdwï / Tüz lajdwu / Zïi lajdwe",
    ]),
    ("Спряжение с «это» (B1)", [
        ("1","-öjz → Lajdwöjz"),
        ("2","-ëjz → Lajdwëjz"),
        ("3","-äjz → Lajdwäjz"),
    ]),
    ("Все виды PS", [
        ("Инфинитив","-o- / -ï-"),
        ("1 неопр.","-ï-"),("1 опр.","-ëz-"),
        ("2 неопр.","-u-"),("2 опр.","-öz-"),
        ("3 неопр.","-e-"),("3 опр.","-äz-"),
    ]),
    ("12 времён", [
        ("Наст. простое","—"),
        ("Наст. моментное","-s"),
        ("Cajme","-n"),
        ("Gëcajme","gë-+-n"),
        ("Secajme","-ns"),
        ("Gësecajme","gë-+-ns"),
        ("Прош. давнее","любое+da"),
        ("Прош. сейчас","любое+je"),
        ("Наст. быстр.","-s+je"),
        ("Cajüne","-jü"),
        ("Secajüne","-j"),
        ("Буд. сейчашнее","gë-"),
    ]),
    ("Прошедшее", [
        "Корень НЕ на -n: -ns / -n",
        "Корень на -n: n→m",
        "Ï kjamwï (умел), Ï kjamwïs (сумел).",
    ]),
    ("Акциональность", [
        ("Начатая","Gë-"),
        ("Прерывистая","-yl-"),
        ("Законченная","—"),
    ]),
    ("Objektïnwa glagoli", [
        "Формула: [Корень] + w + [PS]",
        ("Nai","включение"),("Hei","выключение"),("Aus","закрытие"),
        "Dürwo nai / hei / aus",
    ]),
    ("Modaliwa glagoli", [
        "Группа 1: [Lïnfïne] + lïnfïne",
        "Группа 2: Wïllwï, Tajtwa",
        "Формула Lïnfïne: (Glagoli)+[[GS]]+[PS]+{{l}}",
    ]),
    ("Wïllwï / Javïnwo", [
        ("1","'llwï / 'nwï"),
        ("2","'llwu / 'nwu"),
        ("3","'llwe / 'nwe"),
    ]),
    ("Приставки", ["Отделяемые — свободные.", "Неотделяемые: gë-, ajn-."]),
    ("Местоимения (A1)", [
        ("1","Ï"),("2","Tü / Vü"),
        ("3","Hï / Šï / Ït / Et / At"),
        ("1 мн.","Ïiz"),("2 мн.","Tüz / Vüz"),("3 мн.","Zïi"),
    ]),
    ("Доп. местоимения (A2)", [
        ("1 м.","Ïj"),("1 ж.","Jï"),
        ("2 м.","Tüo/Vüo"),("2 ж.","Tüa/Vüa"),
        ("1 мн. м.","Ïjz"),("1 мн. ж.","Jïz"),
        ("3 выс. м.","Hïz"),("3 выс. ж.","Šïz"),
        ("3 предм.","Ac / Ïc / Ec"),
        "Дв.ч.: zhö",
    ]),
    ("Литературные (C2)", [
        ("1","Zhö"),("2","Tva / Vwa"),
        ("3 м.","Atva"),("3 ж.","Ïtva"),("3 с.","Etva"),
        ("3 выс. м.","Hva"),("3 выс. ж.","Šva"),
    ]),
    ("В.п. местоимений", [
        "Искл.: Ïnwï, Jïnwï, nwï, zwï",
        "Мн.: Ïizwï, Jïzwï, Ïjwïz",
        "B1: mwï / mwo",
    ]),
    ("Р.п. местоимений", [
        ("Ï/Ïj/Jï","mï"),("Ïiz","mïiz"),
        ("Tü","Tï"),("Vü","Vï"),("Vüz/Tüz","Nï"),
    ]),
    ("Притяж. суффиксы", [
        ("Ед. м.","-mo-"),("Ед. ж.","-ma-"),("Ед. с.","-me-"),
        ("Мн. м.","-moz-"),("Мн. ж.","-maz-"),("Мн. с.","-me"),
    ]),
    ("Артикли опред.", [
        ("М.","Lä"),("Ж.","Lïi"),("С.","Le"),
        ("М. в.","Loi"),("Ж. в.","Loij"),("С. в.","Lei"),
    ]),
    ("Артикли неопред.", [
        ("j после гл.","Jün"),("ост.","Ün"),("Мн.","Jïn"),
    ]),
    ("Артикли отриц.", [
        ("М.","Naj"),("Ж.","Nïij"),("С.","Nej"),
    ]),
    ("Najn / Kajn", [
        "Najn — нет сейчас.",
        "Kajn — нет постоянно.",
        ("Najnwï së","не находится"),
        ("Kajnwï së","не быть"),
        ("Kajnwo","бездействовать"),
        ("Najnwo","убирать"),
    ]),
    ("M-pe / рода", [
        ("М. предм.","-o/-e/-ô"),
        ("Ж. предм.","-ï/-i/-a"),
        ("С. предм.","—"),
        ("М. высш.","-o"),
        ("Ж. высш.","-ï/-i/-a"),
        ("С. высш.","-e/-ô/-o"),
    ]),
    ("Akkjuzatwa-pe (A1)", [
        "Зависит от инфинитива.",
        "Инф. -o → -wo; -ï → -wï.",
        "Суффикс ïn: 2 согл., или v/f/w.",
        "djomo → djomwo / djomwï",
    ]),
    ("T-pe", [
        "Чем делают. Окончание -t.",
        "Ï wïns ejzwo ejzot",
        "Ï jesswï së züpot",
    ]),
    ("N-pe / Förd / Faicio", [
        "N-pe: -n → -m, иначе +n.",
        "Förd-pe: o/e/∅ → a; ï/i/a → ï.",
        "Faicio: O→ö, A→ä, E→ë, ∅→ö, I→ï.",
        "Avaircio: Faicio + j.",
    ]),
    ("Предлог en", ["en = на/в.", "Местный: wuj?/a ejsö?", "djomo → djomö."]),
    ("Числительные", [
        "Ciöto: adjam, djev, troja, cijöt, fjati, zejzs, zïivzs, jod, nojn",
        "10=vfön, 100=sjë, 1000=mwa, 10⁶=mïllijön",
        "11–19: jëlif, djölif, trolif, cijölif, fjälif, sjëlif, zïivli, jölif, njëlif",
        "Десятки: djevlïhi, trojlïhi…",
        "21 = djevlïhi jati",
    ]),
    ("Местные предлоги", [
        ("Ïn/Ïm/Ïns","в (замкн.)"),
        ("Cu/Cum/Cuns","в (откр.)"),
        ("Äw/Äwn/Äwns","в трансп."),
        ("A/Am/Ans","во времени"),
        ("An/Am/Ans","на вертикали"),
        ("Ön/Öm/Öns","на горизонтали"),
        ("Cï/Ca","вдоль"),
        ("Kaj","у"),("Baj","рядом"),("Ce","по"),
        ("Jüg","под/перед"),("App/Ïss","вверх/вниз"),
        ("Lë/Rë","слева/справа"),
        ("Ïr/Ïir","впритык/впившийся"),
    ]),
    ("Предлоги без форм", [
        ("Ojne","без"),("A-a","между"),
        ("Cur","похожий"),("De","словообр."),
        ("Mït","вместе"),("Dïm","делить"),
        ("Für","для"),("Kojlo","вокруг/каждый"),
        ("Naj","с нового"),("Adiü","через"),
        ("Gadiü","чувствовать"),("Najn","нет"),
        ("Kajne","нет вообще"),
    ]),
    ("Суффиксы", [
        ("-sïin-","предмет с содержимым"),
        ("-od-","здание/место"),
        ("-z-/-az-","магазин"),
        ("-àt-","национ./профессия"),
        ("-lat-","профессия"),
        ("-àl-","говорящий"),
        ("-us-","пара"),
        ("-ïic-","высш. ж.р."),
        ("-ert-/-elit-","справа/слева"),
        ("-opp-","сверху"),
        ("-ov-","фамилия"),
        ("-av-","человек по хар."),
        ("-trak-","чердак"),
        ("-af-","связан с едой"),
        ("-ïjf-","результат"),
    ]),
    ("Наречия", [
        "Убираем GS/PS, + -et.",
        ("Lui","хорошо"),("Fjat","плохо"),
        ("Afrodïtet","красиво"),("Rodet","красно"),
        ("Vïrïdet","зелено"),("Janet","бело"),("Ïnet","черно"),
    ]),
    ("Прилагательные", [
        "Формула: [Корень]+[GS]+[a]",
        "Прош.: не на -n → +n; на -n → -m.",
        ("Vïrïdïnwa","зелёный"),("Rotwa","красный"),
        ("Luïnwa","хороший"),("Fjatwa","плохой"),
        ("Bonwa","хороший"),("Carulïnwa","синий"),
    ]),
    ("Сокращения", [
        "Së ejzwï/ejzwo = sëjzwï/sëjzwo",
        "Jï äwlojantwï së = Jëwlojantwï së",
    ]),
    ("Приветствия", [
        ("Vejl!","Привет!"),
        ("Vejl-barkajvo!","Здравствуйте!"),
        ("Ajo!","Пока!"),
        ("Ajo-kajvo!","До свидания!"),
        ("Bon tun!","Добрый день!"),
        ("Bon matyna!","Доброе утро!"),
        ("Bon marhen!","Добрый вечер!"),
        ("Bon noŝi!","Доброй ночи!"),
        ("Jas!","Да, сэр!"),
        ("Lui!","Хорошо!"),
        ("Jal!","Да, хорошо!"),
        ("Ejz'll lui!","Это хорошо!"),
        ("Mït vordtod","к слову"),
        ("Ejs veljanto?","Как дела?"),
        "Этика: vejl-barkajvo → pravï-kajvo",
    ]),
    ("Чувства и язык", [
        "Ï veljanwï (говорю по-вэльянски)",
        "Ï russwï (говорю по-русски)",
        "Ï gwo adiü bïci = мне больно",
        "Ï gadiü bïci (разг.)",
    ]),
    ("Порядок обучения", [
        "1) Алфавит, чтение, приветствия.",
        "2) Глаголы или существительные.",
        "Падежи: A1 (M,N+Akkjuz,T,D,R), A2–C2 (остальные).",
    ]),
    ("Топ-10 с В.п.", [
        "1. Ï lajdwï djomwï",
        "2. Tü lajdwun ïnwï",
        "3. Ï wïns ejzwo",
        "4. Kajto vïzzwe stojlïnwï",
        "5. Ï lejnwïns tjemwï",
        "6. Tü auzlejzwuns lïbrïnwï",
        "7. Ï vajzwï twï",
        "8. Hï ajnwajzwe ïnwï",
        "9. Ejz'll djomo",
        "10. Ï wajzwï hwï",
    ]),
]

LEXICON = [
    ("Местоимения", [
        ("Ï","я"),("Ïj","я (м.)"),("Jï","я (ж.)"),
        ("Tü","ты"),("Vü","Вы"),
        ("Hï","он (высш.)"),("Šï","она (высш.)"),
        ("At","он"),("Ït","она"),("Et","оно"),
        ("Ïiz","мы"),("Tüz","вы"),("Vüz","Вы (мн.)"),("Zïi","они"),
    ]),
    ("Числительные", [
        ("adjam","1"),("djev","2"),("troja","3"),
        ("cijöt","4"),("fjati","5"),("zejzs","6"),
        ("zïivzs","7"),("jod","8"),("nojn","9"),
        ("vfön","10"),("sjë","100"),("mwa","1000"),
    ]),
    ("Глаголы A–B", [
        ("Änwo","плакать"),("Adiügwo","переходить"),
        ("Ajnlajdwï","не любить"),("Ajnwo","не делать"),
        ("Arbajtwï","работать"),("Bëżwï","бежать"),
        ("Blümwo","пить"),("Brawo","брать"),
    ]),
    ("Глаголы D–G", [
        ("Dajwo","делать"),("Djenkwï","думать"),
        ("Djomwo","строить"),("Farwo","водить"),
        ("Fïlwo","летать"),("Föŝtejwï","понимать"),
        ("Gwo","двигаться"),
    ]),
    ("Глаголы K–L", [
        ("Kjanwo","уметь"),("Kulliwo","писать"),
        ("Lajdwï","любить"),("Lecojwï","читать"),
        ("Lejnwï","учиться"),("Lïmwo","красить"),
    ]),
    ("Глаголы M–P", [
        ("Marwo","умереть"),("Nadwï","хотеть"),
        ("Nożwo","резать"),("Pälwï","иметь"),
        ("Plyklwï","говорить"),("Pjekwï","просить"),
    ]),
    ("Глаголы S–V", [
        ("Sejtwï","чувствовать"),("Sonwï","спать"),
        ("Stojwo","ставить"),("Two","идти"),
        ("Vajzwï","знать"),("Veljanwï","говорить по-вэльянски"),
        ("Vïzzwï","видеть"),
    ]),
    ("Глаголы W–Z", [
        ("Wo","делать"),("Wïllwï","быть"),
        ("Woikwo së","гулять"),("Zagwo","говорить"),
        ("Żyhavïnwo","пылесосить"),
    ]),
    ("Существительные: базовые", [
        ("veljano","вэльянский"),("djomo","дом"),
        ("kajto","кот"),("kajta","кошка"),
        ("jundo","собака"),("wajsa","вода"),
        ("kullï","ручка"),("lïbro","книга"),
        ("jesso","еда"),("brodo","хлеб"),
        ("mlako","молоко"),("kojfï","кофе"),
        ("cijaj","чай"),("äwlojanto","машина"),
        ("taxï","такси"),
    ]),
    ("Существительные: лингвистика", [
        ("lekswï","словарь"),("gramatïkje","грамматика"),
        ("vordàto","словарь"),("ausvordo","окончание"),
        ("cajte","время (грам.)"),("glagolisïino","глагол"),
        ("fördaglagolisïino","прилагательное"),
        ("vordto","слово"),("ïnvordto","слог"),
        ("pravvordto","корень"),("fonemàte","фонетика"),
        ("sïntaksàte","синтаксис"),("ojneije","местоимение"),
        ("cajme","прошедшее"),("cajüne","будущее"),
        ("najcajte","настоящее"),
        ("jügausvordte","суффикс"),("jügvordte","префикс"),
    ]),
    ("Существительные: быт", [
        ("mülo","мыло"),("mïsko","миска"),
        ("nożo","нож"),("nożïica","ножница"),
        ("hoha","одеяло"),("mato","матрас"),
        ("buba","подушка"),("fja","диван"),
        ("bjata","кровать"),("amo","кухня"),
        ("noŝi","ночь"),("tajsa","рука/нога"),
        ("foto","фото"),("papïi","бумага"),
        ("arpapïi","картон"),("vïlïks","вилка"),
        ("ŝtajko","розетка"),("tajzo","чашка"),
    ]),
    ("Существительные: наука", [
        ("fïzïkïica","физика"),("biölogïica","биология"),
        ("lïtëraturïica","литература"),("tjoreme","теорема"),
        ("funkciï","функция"),("awsnoj","число"),
        ("moduli","модуль"),("reno","степень"),
        ("kreto","корень (матем.)"),("ümo","ум"),
        ("jodo","растение/жизнь"),
    ]),
    ("Существительные: медицина", [
        ("ràke","рак"),("kòre","сердце"),
        ("bïcisïino","воспаление"),("bïciojo","диагноз"),
        ("noso","нос"),("plyklàntsïino","рот"),
        ("rajo","кровь"),
    ]),
    ("Существительные: транспорт", [
        ("mëtro","метро"),("ŝtrajto","улица"),
        ("buso","автобус"),("tajksï","такси"),
        ("cug","поезд"),("djomàto","город"),
        ("ŝujla","школа"),("appcugo","лифт"),
        ("zlomöno","бензин"),
    ]),
    ("Существительные: мифология", [
        ("aljano","бог"),("aljanso","божество"),
        ("mil","бог света"),("unsu-dojо","дух-хранитель"),
        ("majo","магия"),
    ]),
    ("Существительные: география", [
        ("rossïja","Россия"),("dojtŝciland","Германия"),
        ("dżonguo","Китай"),("amerik","Америка"),
        ("krasnogórsk","Красногорск"),("klín","Клин"),
        ("dubná","Дубна"),
    ]),
    ("Имена", [
        ("artëmij","Артемий"),("david","Давид"),
        ("dima","Дима"),("igor","Игорь"),
        ("sajša","Саша"),("grïša","Гриша"),
    ]),
    ("Еда", [
        ("zalato","салат"),("züipo","суп"),
        ("tajzo","чашка"),("trüfeli","трюфель"),
        ("banano","банан"),("arva","яблоко"),
        ("ara","груша"),
    ]),
]


# ---------- ИНТЕРФЕЙС ----------
DARK = get_color_from_hex("#212121")
WHITE = get_color_from_hex("#FFFFFF")


def mk_button(text, bg_hex, on_press, height=60):
    b = Button(
        text=text,
        size_hint_y=None,
        height=dp(height),
        background_normal="",
        background_color=get_color_from_hex(bg_hex),
        color=WHITE,
        font_size=dp(18),
        bold=True,
    )
    b.bind(on_press=on_press)
    return b


def mk_label(text, size=14, color="#000000", bold=False, height=None):
    lb = Label(
        text=text,
        font_size=dp(size),
        color=get_color_from_hex(color),
        bold=bold,
        size_hint_y=None,
        halign="left",
        valign="top",
    )
    lb.bind(width=lambda *_: setattr(lb, "text_size", (lb.width, None)))
    if height:
        lb.height = dp(height)
    else:
        lb.bind(texture_size=lambda *_: setattr(lb, "height", lb.texture_size[1]))
    return lb


class VeljanoApp(App):
    def build(self):
        self.title = "Veljano"
        Window.clearcolor = get_color_from_hex("#F5F5F5")
        self.root_box = BoxLayout(orientation="vertical")
        self.show_home()
        return self.root_box

    def _clear(self):
        self.root_box.clear_widgets()

    def _add_scroll(self, widget):
        sv = ScrollView()
        sv.add_widget(widget)
        self.root_box.add_widget(sv)

    # ---------- ГЛАВНЫЙ ЭКРАН ----------
    def show_home(self, *args):
        self._clear()
        box = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10),
                        size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        box.add_widget(mk_label("Veljano", size=36, bold=True, height=50))
        box.add_widget(mk_label("Справочник языка", size=16,
                                color="#666666", height=30))
        box.add_widget(mk_label("", height=20))

        box.add_widget(mk_button("🔤  Фонетика", "#2196F3",
                                 lambda e: self.show_toc("Фонетика", PHONETICS)))
        box.add_widget(mk_button("📘  Определения", "#9C27B0",
                                 lambda e: self.show_toc("Определения", DEFINITIONS)))
        box.add_widget(mk_button("🔣  Обозначения", "#607D8B",
                                 lambda e: self.show_toc("Обозначения", NOTATION)))
        box.add_widget(mk_button("📖  Грамматика", "#4CAF50",
                                 lambda e: self.show_toc("Грамматика", GRAMMAR)))
        box.add_widget(mk_button("📚  Лексика", "#FF5722",
                                 lambda e: self.show_toc("Лексика", LEXICON)))
        self._add_scroll(box)

    # ---------- СПИСОК ТЕМ ----------
    def show_toc(self, title, data, *args):
        self._clear()
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6),
                        size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        box.add_widget(mk_button("← Назад", "#455A64",
                                 lambda e: self.show_home(), height=44))
        box.add_widget(mk_label(title, size=22, bold=True, height=40))

        for i, (name, _) in enumerate(data):
            box.add_widget(mk_button(name, "#607D8B",
                                     lambda e, idx=i, d=data, t=title:
                                     self.show_topic(d[idx][0], d[idx][1], d, t),
                                     height=50))
        self._add_scroll(box)

    # ---------- СОДЕРЖИМОЕ ТЕМЫ ----------
    def show_topic(self, title, content, sections, section_title, *args):
        self._clear()
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6),
                        size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        box.add_widget(mk_button("← Назад", "#455A64",
                                 lambda e: self.show_toc(section_title, sections),
                                 height=44))
        box.add_widget(mk_label(title, size=18, bold=True, height=40))

        for line in content:
            if isinstance(line, tuple):
                cells = [str(c) for c in line]
                text = f"{cells[0]}: " + "  ".join(cells[1:])
                box.add_widget(mk_label(text, size=14, color="#1B5E20"))
            else:
                box.add_widget(mk_label(line, size=14))
        self._add_scroll(box)


if __name__ == "__main__":
    VeljanoApp().run()
