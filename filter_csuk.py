#!/usr/bin/env python3
import argparse
import re, sys
from collections import Counter


# Čech can be a surname or Česká XY a company name, which could be left untranslated in uk
VARIOUS = r'''(?i)če(sk|št[ií]|ši|ch[^r]) = (?i)че(ськ|х)|če(sk|ch) = cs-uk
(?i)ukrajin = (?i)україн = both
CZK = Czech sentences should use koruna/Kč, not CZK = cs-uk
Kč = крон|Кч|CZK = cs-uk
korun[^nkd][^v] = крон|Кч|CZK|винчик|корон = cs-uk
гриве?н|(?i)грн = hřive?n|UAH = uk-cs
(www[.]|http)[^ ]+[.]cz = (www[.]|http)[^ ]+[.]cz = cs-uk
(www[.]|http)[^ ]+[.]ua = (www[.]|http)[^ ]+[.]ua = cs-uk
@[^ ]+[.]cz = @[^ ]+[.]cz = cs-uk
@[^ ]+[.]ua = @[^ ]+[.]ua = cs-uk'''

# Následující seznamy jde editovat online zde
# https://docs.google.com/spreadsheets/d/1Mubm8fbGbwDqmIL8uHg3kMhLXbA2U5Dn6TMyyKzMm8s/edit?usp=sharing

CZ_CITIES = r'''Pra(h[ayu]|ze|hou|žsk|žan) = Пра[гз]
Brn([oau]|em|ěnsk|ě[ ,.]) = Брн
Ostrav = Острав
Plz(eň|n[ěií]) = Пль?зе?н
Libere?c = Лібере?ц
Olomouc = Оломоуц
Česk[^ ]+ Budějovic = Чеськ[^ ]+ Будейовиц
Ústím? nad Labem = Усті-над-Лаб
Hrade?ce?m? Králové = Граде?це?м?-Кралове
Pardubic = Пардуб[иі]ц
Zlín = Злін
Havířov = Гавіржов
Klad(n[oau]|nem|ensk) = Кладн
Most = Мост|[Мм]іст|Most
Opav = Опав
Frýd(ek|ku|kem)-Míst(ek|ku|kem) = Фріде?к
Karvin = Карвін
Jihlav = Їглав
Teplic = Тепл[иі]ц
Děčín = Дечин
Karlov[^ ]+ Var = Карлов[^ ]+ Вар
Chomutov = Хомутов
Jablone?ce?m? nad Nisou = Яблоне?ц
Mlad[^ ]+ Boleslav = Млад[^ ]+ Болеслав
Přerov = Пршеров
Prostějov = Простейов
Česk[^ ]+ Líp = Чеськ[^ ]+ Лип
Třebíč = Тршебич
Třine?c = Тржине?ц
Tábor = [Тт]аб[оi]р
Znojm = Знойм
Příbram = Пржибрам
Cheb = Хеб
Kolín[^s] = Колін
Trutnov = Трутнов'''

UA_CITIES = r'''Ки[їє]в = Kyj[ei]v
Харк[іо]в = Chark[oi]v
Дніпр = Dn[iě]pr
Одес = Od[ěe]s
Донецьк = Doněck
Запоріжж = Záporož
Льв[іо]в = Lv[oi]v
Крив[^ ]+ Р[іо]г = Kriv[^ ]+ R
Миколаїв[^н] = Mykolajiv
Маріупол = Mariupol
Луганськ = Luhansk
Макіївк = Makijivk
Вінниц = Vinn?[yi]c
Сімферопол = Simferopol
Севастопол = Sevastopol
Херсон = Cherson
Полтав = Poltav
Чернігів = Černihiv|Černigov
Черкас = Čerkas
Сум(и|ах) = Sum
Горлівк = Horlivk
Житомир = Žytomyr|Žitomír
Кам'янськ = Kamjansk
Кропивницьк = Kropyvnyck
Хмельницьк = Chmelnyck
Рівн(е|ого|ому|им) = R[io]vn
Чернів = Čern[io]vi?c
Кременчук = Kremenčuk
Тернопіл = Ternopil
Івано-Франківськ = Ivano-Frankivsk
Луцьк = Luck
Біл[^ ]+ Церкв = Bil[^ ]+ Cerkv
Краматорськ = Kramatorsk
Мелітопол = Melitopol
Керч = Kerč
Нікопол = Nikopol
Слов'янськ = Slovjansk
Бердянськ = Berďansk
Сєвєродонецьк = Sjevjerodoneck
Алчевськ = Alčevsk
Павлоград = Pavlohrad
Ужгород = Užhorod
Лисичанськ = Lysyčansk
Євпаторі = Jevpatori
Єнакієв = Jenakijev
Кам'яне[^ ]+-Подільськ = Kamene?c Podolsk
Костянтинівк = Kosťantynivk
Хрустальний = Chrustalnyj
Конотоп = Konotop
Кадіївк = Kadijivk
Уман = Uma[ňn]
Бердичів = Berdyčiv
Шостк = Šostk
Бровар = Brovar
Ізмаїл = Izmajil
Бахмут = Bachmut
Мукачев = Mukačev
Ялт = Jalt
Дрогобич = Drohobyč
Ніжин = Nižyn
Феодосі = Feodosi
Довжанськ = Dovžansk
Новомосковськ = Novomoskovsk
Чистяков = Čisťakov
Червоноград = Červonohrad
Первомайськ = Pervomajsk
Сміл[^и] = Smil
Покровськ = Pokrovsk
Калуш = Kaluš
Коростен = Koroste[ňn]
Ковел = Kovel
Рубіжн = Rubižn
Прилук = Pryluk
Дружківк = Družkivk
Харцизьк = Charcyzk
Лозов = Lozov
Антрацит = Antracyt
Стрий[^нк] = Stryj
Коломи = Kolomyj
Шахтарськ = Šachtarsk
Сніжн = Snižn
Новоград-Волинськ = Novohrad-Volynsk
Енергодар = Enerhodar
Ізюм = Izjum
Мирноград = Myrnohrad
Брянк = Brjank
Чорноморськ = Čornomorsk
Бориспіл = Boryspil
Нововолинськ = Novovolynsk
Ровеньк = Roveňk
Жовт[^ ]+ Вод = Žovt[^ ]+ Vod
Лубн = Lubn
Нов[^ ]+ Каховк = Nov[^ ]+ Kachovk
Фастів = Fastiv
Білгород-Дністровськ = Bilhorod-Dnistrovsk
Горішні Плавн = Horišni Plavn
Сорокин = Sorokyn
Ромни = Romny
Охтирка = Ochtyrka
Світловодськ = Svitlovodsk
Марганець = Marhanec
Шепетівка = Šepet[io]vka
Покров = Pokrov
Торецьк = Toreck
Джанкой = Džankoj
Первомайськ = Pervomajsk
Миргород = Myrhorod
Вознесенськ = Voznesensk
Подільськ = Podilsk
Ірпінь = Irpiň
Васильків = Vasylkiv
Дубно = Dubno
Вараш = Varaš
Володимир[^о] = Volodymyr|Vladimír
Каховка = Kachovka
Южноукраїнськ = Južnoukrajinsk
Борислав = Boryslav
Ясинувата = Jasynuvata
Жмеринка = Žmerynka
Авдіївка = Avdijivka
Чугуїв = Čuhujiv
Самбір = Sambir
Токмак = Tokmak
Боярка = Bojarka
Глухів = Hluchiv
Добропілля = Dobropillja
Старокостянтинів = Starokosťantyniv
Голубівка = Holubivka
Вишневе = Vyšneve
Нетішин = Netišyn
Славута = Slavuta
Могилів-Подільський = Mohyliv-Podilskyj
Обухів = Obuchiv
Первомайський = Pervomajskyj
Куп'янськ = Kupjansk
Балаклія = Balaklija
Синельникове = Synelnykove
Переяслав = Perejaslav
Алушта = Alušta
Трускавець = Truskavec
Красноперекопськ = Krasnoperekopsk
Хрестівка = Chrestivka
Костопіль = Kostopil
Дебальцеве = Debalceve
Перевальськ = Perevalsk
Саки = Saky
Знам'янка = Znamjanka
Тернівка = Ternivka
Першотравенськ = Peršotravensk
Хуст = Chust
Чортків = Čortkiv
Лебедин = Lebedyn
Золотоноша = Zolotonoša
Буча = Buča
Новий Розділ = Novyj Rozdil
Лиман = Lyman
Сарни = Sarny
Малин = Malyn
Хмільник = Chmilnyk
Бахчисарай = Bachčisaraj
Селидове = Selydove
Берегове = Berehovo
Канів = Kaniv
Козятин = Kozjatyn|K[oa]zat[íi]n
Новояворівськ = Novojavorivsk
Коростишів = Korostyšiv
Попасна = Popasna
Виноградів = Vynohradiv
Гайсин = Hajsyn
Молодогвардійськ = Molodohvardijsk
Кролевець = Krolevec
Мерефа = Merefa
Волноваха = Volnovacha
Здолбунів = Zdolbuniv
Кремінна = Kreminna
Славутич = Slavutyč
Докучаєвськ = Dokučajivsk
Люботин = Ljubotyn
Олешки = Olešky
Южне = Južne
Армянськ = Armjansk
Вільногірськ = Vilnohirsk
Яготин = Jahotyn
Суходільськ = Suchodilsk
Золочів = Zoločiv
Тростянець = Trosťanec
Броди = Brody
Полонне = Polonne
Вишгород = Vyšhorod
Гадяч = Haďač
Красноград = Krasnohrad
Кілія = Kilija
Старобільськ = Starobilsk
Ладижин = Ladyžyn
Амвросіївка = Amvrosijivka
Кременець = Kremenec
Генічеськ = Heničesk
Сокаль = Sokal
Курахове = Kurachove
Дніпрорудне = Dniprorudne
Волочиськ = Voločysk
Надвірна = Nadvirna
Стебник = Stebnyk
Вовчанськ = Vovčansk
Красилів = Krasyliv
П'ятихатки = Pjatychatky
Рені = Reni
Бахмач = Bachmač
Дергачі = Derhači
Ватутіне = Vatutine
Калинівка = Kalynivka
Балта = Balta
Звенигородка = Zvenyhorodka
Зугрес = Zuhres
Скадовськ = Skadovsk
Сватове = Svatove
Шпола = Špola
Новоукраїнка = Novoukrajinka
Корсунь-Шевченківський = Korsuň-Ševčenkivskyj
Лутугине = Lutuhyne
Білогірськ = Bilohirsk
Долинська = Dolynska
Ізяслав = Izjaslav
Білопілля = Bilopillja
Богодухів = Bohoduchiv
Сквира = Skvyra
Карлівка = Karlivka
Оріхів = Orichiv
Білозерське = Bilozerske
Бунге = Bunhe
Підгородне = Pidhorodne
Роздільна = Rozdilna
Городок = Horodok
Вознесенівка = Voznesenivka
Іловайськ = Ilovajsk
Бережани = Berežany
Новогродівка = Novohrodivka
Вугледар = Vuhledar
Березань = Berezaň
Путивль = Putyvl
Болград = Bolhrad
Свалява = Svaljava
Богуслав = Bohuslav
Гуляйполе = Huljajpole
Зміїв = Zmijiv
Овруч = Ovruč
Верхньодніпровськ = Verchňodniprovsk
Очаків = Očakiv
Красногорівка = Krasnohorivka
Ківерці = Kiverci
Пирятин = Pyrjatyn
Миколаївка = Mykolajivka
Часів Яр = Časiv Jar
Вільнянськ = Vilňansk
Дунаївці = Dunajivci
Апостолове = Apostolove
Тальне = Talne
Арциз = Arcyz
Новий Буг = Novyj Buh
Тульчин = Tulčyn
Гайворон = Hajvoron
Городок = Horodok
Гола Пристань = Hola Prystaň
Носівка = Nosivka
Жашків = Žaškiv
Городище = Horodyšče
Василівка = Vasylivka
Кам'янка-Дніпровська = Kamjanka-Dniprovska
Петрово-Красносілля = Petrovo-Krasnosillja
Берислав = Beryslav
Снігурівка = Snihurivka
Радомишль = Radomyšl
Рахів = Rachov
Новгород-Сіверський = Novhorod-Siverskyj
Кам'янка = Kamjanka
Тетіїв = Tetijiv
Острог = Ostroh
Зеленодольськ = Zelenodolsk
Боково-Хрустальне = Bokovo-Chrustalne
Хорол = Chorol
Сторожинець = Storožynec
Судак = Sudak
Сіверськ = Siversk
Корюківка = Korjukivka
Біляївка = Biljajivka
Гірник = Hirnyk
Українка = Ukrajinka
Нов[^ ]+ Одес = Nov[^ ]+ Od[ěe]s
Городня = Horodňa
Кагарлик = Kaharlyk
Жданівка = Ždanivka
Березне = Berezne
Теребовля = Terebovlja
Винники = Vynnyky
Рожище = Rožyšče
Яворів = Javoriv
Жовква = Žovkva
Тараща = Tarašča
Миронівка = Myronivka
Бершадь = Beršaď
Українськ = Ukrajinsk
Збараж = Zbaraž
Новомиргород = Novomyrhorod
Узин = Uzyn
Світлодарськ = Svitlodarsk
Соледар = Soledar
Баштанка = Baštanka
Мала Виска = Mala Vyska
Ірміно = Irmino
Барвінкове = Barvinkove
Приморськ = Prymorsk
Мена = Mena
Глобине = Hlobyne
Гнівань = Hnivaň
Кальміуське = Kalmiuske
Ічня = Ičňa
Новоазовськ = Novoazovsk
Баранівка = Baranivka
Бучач = Bučač
Лохвиця = Lochvycja
Сновськ = Snovsk
Бобринець = Bobrynec
Немирів = Nemyriv
Кобеляки = Kobeljaky
Родинське = Rodynske
Чигирин = Čyhyryn
Бобровиця = Bobrovycja
Соснівка = Sosnivka
Жидачів = Žydačiv
Ямпіль = Jampil
Моспине = Mospyne
Борзна = Borzna
Щолкіне = Ščolkine
Буринь = Buryn
Кам'янка-Бузька = Kamjanka-Buzka
Гребінка = Hrebinka
Христинівка = Chrystynivka
Гірське = Hirske
Таврійськ = Tavrijsk
Борщів = Borščiv
Зимогір'я = Zymohirja
Хотин = Chotyn
Іллінці = Illinci
Помічна = Pomična
Олевськ = Olevsk
Камінь-Каширський = Kamiň-Kašyrskyj
Татарбунари = Tatarbunary
Погребище = Pohrebyšče
Мар'їнка = Marjinka
Болехів = Bolechiv
Інкерман = Inkerman
Зіньків = Ziňkiv
Ходорів = Chodoriv
Снятин = Sňatyn
Деражня = Deražňa
Любомль = Ljuboml
Валки = Valky
Новодністровськ = Novodnistrovsk
Радивилів = Radyvyliv
Вуглегірськ = Vuhlehirsk
Сокиряни = Sokyrjany
Верхівцеве = Verchivceve
Заліщики = Zališčyky
Старий Крим = Staryj Krym
Білицьке = Bilycke
Перещепине = Pereščepyne
Андрушівка = Andrušivka
Пустомити = Pustomyty
Городенка = Horodenka
Тисмениця = Tysmenycja
Тячів = Ťačiv
Семенівка = Semenivka
Дубровиця = Dubrovycja
Кодима = Kodyma
Іршава = Iršava
Березівка = Berezivka
Ананьїв = Anaňjiv
Монастирище = Monastyryšče
Решетилівка = Rešetylivka
Липовець = Lypovec
Вилкове = Vylkove
Радехів = Radechiv
Мостиська = Mostyska
Кипуче = Kypuče
Новодружеськ = Novodružesk
Заводське = Zavodske
Алупка = Alupka
Горохів = Horochiv
Привілля = Pryvillja
Чоп = Čop
Заставна = Zastavna
Зоринськ = Zorynsk
Тлумач = Tlumač
Теплодар = Teplodar
Ланівці = Lanivci
Буськ = Busk
Корець = Korec
Рогатин = Rohatyn
Південне = Pivdenne
Дубляни = Dubljany
Ржищів = Ržyščiv
Новоселиця = Novoselycja
Ворожба = Vorožba
Косів = Kosiv
Почаїв = Počajiv
Рава-Руська = Rava-Ruska
Молочанськ = Moločansk
Яремче = Jaremče
Турка = Turka
Кіцмань = Kicmaň
Перемишляни = Peremyšljany
Благовіщенське = Blahoviščenske
Середина-Буда = Seredyna-Buda
Хоростків = Chorostkiv
Остер[^і] = Oster
Шаргород = Šarhorod
Перечин = Perečín
Олександрівськ = Oleksandrivsk
Копичинці = Kopyčynci
Сколе = Skole
Залізне = Zalizne
Судова Вишня = Sudova Vyšňa
Галич = Halyč
Моршин = Moršyn
Чуднів = Čudniv
Монастириська = Monastyryska
Міусинськ = Miusynsk
Вашківці = Vaškivci
Великі Мости = Velyki Mosty
Дружба = Družba
Старий Самбір = Staryj Sambir
Шумськ = Šumsk
Святогірськ = Svjatohirsk
Алмазна = Almazna
Вижниця = Vyžnycja
Добромиль = Dobromyl
Рудки = Rudky
Хирів = Chyriv
Скалат = Skalat
Комарно = Komarno
Бібрка = Bibrka
Новий Калинів = Novyj Kalyniv
Глиняни = Hlyňany
Підгайці = Pidhajci
Батурин = Baturyn
Белз = Belz
Устилуг = Ustyluh
Герца = Herca
Берестечко = Berestečko
Угнів = Uhniv
Чорнобил = Černobyl
Прип'ят = Pripja[ťt]'''


def get_rules(various=True, cz_cities=True, ua_cities=True):
    rules = []
    if various:
        for rule in VARIOUS.split('\n'):
            cs_pat, uk_pat, direction = rule.split(' = ')
            rules.append((re.compile(cs_pat), re.compile(uk_pat), direction))

    if cz_cities:
        for rule in CZ_CITIES.split('\n'):
            # Let's allow Czech cities untranslated (kept in Latin script) in the Ukrainian translations.
            cs_pat, uk_pat = rule.split(' = ')
            rules.append((re.compile(cs_pat), re.compile(uk_pat + '|' + cs_pat), 'cs-uk'))

    if ua_cities:
        for rule in UA_CITIES.split('\n'):
            try:
                uk_pat, cs_pat = rule.split(' = ')
            except ValueError:
                print(f"SPLIT {rule}", file=sys.stderr)
            # Одеського = oděsského, může být malé písmeno
            rules.append((re.compile('(?i)'+cs_pat), re.compile(uk_pat), 'uk-cs'))

    return rules


def is_wrong(line, n_line, stats, wrong, rules):
    try:
        cs, uk = line.strip().split('\t')
    except ValueError:
        print(f"SPLIT ERR (line={n_line}): " + line, file=sys.stderr)
        return True
    for cs_pat, uk_pat, direction in rules:
        if direction != 'uk-cs' and cs_pat.search(cs):
            stats[cs_pat.pattern] += 1
            stats['CS-ALL'] += 1
            if not uk_pat.search(uk):
                wrong[cs_pat.pattern] += 1
                wrong['CS-ALL'] += 1
                return True
        if direction != 'cs-uk' and uk_pat.search(uk):
            stats[uk_pat.pattern] += 1
            stats['UK-ALL'] += 1
            if not cs_pat.search(cs):
                wrong[uk_pat.pattern] += 1
                wrong['UK-ALL'] += 1
                return True
    return False


def main():
    parser = argparse.ArgumentParser(
        description='Filter out wrong translations. Usage: paste my.cs my.uk | ./filter_csuk.py > my.filtered.tsv')
    parser.add_argument(
        '-v', '--verbose', type=int, default=None,
        help='number of lines to print on stderr with the top patterns')
    parser.add_argument(
        '-r', '--reverse', action="store_true", default=False,
        help="If set, prints the failing pairs instead of the correct ones.")
    args = parser.parse_args()

    rules = get_rules()

    stats, wrong = Counter(), Counter()
    n_line, wlines = 0, 0
    for line in sys.stdin:
        n_line += 1
        if is_wrong(line, n_line, stats, wrong, rules):
            wlines += 1
            if args.reverse:
                print(line, end="")
        elif not args.reverse:
            print(line, end="")

    for pat, wcount in wrong.most_common(args.verbose):
        print(f"{pat:>40} ={stats[pat]:6}  WRONG={wcount:5}  ({100*wcount/stats[pat]:5.1f}%)", file=sys.stderr)
    print(f"Deleted {wlines:,} ({100*wlines/n_line:.2f}%) lines out of {n_line:,}.", file=sys.stderr)


if __name__ == "__main__":
    main()
