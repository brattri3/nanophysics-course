import React, { useState } from 'react';
import {
  FileText,
  BookOpen,
  CalendarCheck,
  ShieldAlert,
  Layers,
  Sparkles,
  ChevronRight,
  BookMarked,
  Library,
  ListTree,
  FlaskConical
} from 'lucide-react';

interface BookItem {
  id: string;
  title: string;
  author: string;
  publisher: string;
  year: string;
  path: string;
  badge: string;
  badgeColor: string;
  description: string;
}

const BOOKS: BookItem[] = [
  {
    id: 'kuznetsov',
    title: 'Основы нанотехнологии',
    author: 'Кузнецов Н.Т., Новоторцев В.М., Жабрев В.А., Марголин В.И.',
    publisher: 'М.: БИНОМ. Лаборатория знаний',
    year: '2017',
    path: '/course_materials/literature/Кузнецов_Основы_нанотехнологии.pdf',
    badge: 'Базовый учебник',
    badgeColor: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    description: 'Фундаментальный учебник по нанотехнологиям: размерные эффекты, термодинамика зародышеобразования, механизмы роста пленок, квантовые низкоразмерные структуры, плазмоника, углеродные наноструктуры и приборы наноэлектроники.'
  },
  {
    id: 'summ-1',
    title: 'Основы коллоидной химии (Часть 1)',
    author: 'Сумм Б.Д.',
    publisher: 'М.: Академия',
    year: '2007',
    path: '/course_materials/literature/Сумм_Основы_коллоидной_химии_ч1.pdf',
    badge: 'Поверхностные явления',
    badgeColor: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    description: 'Свободная поверхностная энергия, капиллярные явления, давление Лапласа, формула Кельвина-Томсона, уравнение Юнга (смачивание), теория мономолекулярной адсорбции Ленгмюра и полимолекулярной адсорбции БЭТ.'
  },
  {
    id: 'summ-2',
    title: 'Основы коллоидной химии (Часть 2)',
    author: 'Сумм Б.Д.',
    publisher: 'М.: Академия',
    year: '2007',
    path: '/course_materials/literature/Сумм_Основы_коллоидной_химии_ч2.pdf',
    badge: 'ДЭС и ДЛФО',
    badgeColor: 'bg-teal-50 text-teal-700 border-teal-200',
    description: 'Строение двойного электрического слоя (ДЭС), электрокинетические явления и дзета-потенциал, теория устойчивости и коагуляции коллоидов (ДЛФО), правило Шульце-Гарди, мицеллообразование и критическая концентрация мицелл (ККМ).'
  },
  {
    id: 'polenov',
    title: 'Физико-химические основы нанотехнологий',
    author: 'Поленов В.С.',
    publisher: 'СПб.: ГУАП',
    year: '2018',
    path: '/course_materials/literature/Поленов_ФХОНТ.pdf',
    badge: 'Учебное пособие ГУАП',
    badgeColor: 'bg-purple-50 text-purple-700 border-purple-200',
    description: 'Учебное пособие профильной кафедры: термодинамика малых частиц, размерные фазовые переходы, капиллярные явления, коллоидный синтез наночастиц и размерные зависимости физических свойств.'
  },
  {
    id: 'guap-lectures',
    title: 'Курс лекций «Физические основы нанотехнологий»',
    author: 'Кафедра физики ГУАП',
    publisher: 'СПб.: ГУАП',
    year: '2019',
    path: '/course_materials/literature/222000.62 Курс лекций.pdf',
    badge: 'Конспект лекций',
    badgeColor: 'bg-amber-50 text-amber-700 border-amber-200',
    description: 'Зонная теория низкоразмерных структур (2D, 1D, 0D), баллистический транспорт, формула Ландауэра, квантовый эффект Холла, фотонные кристаллы, зондовая микроскопия (АСМ, СТМ) и наноэлектроника.'
  }
];

interface LectureIndexItem {
  number: string;
  date: string;
  title: string;
  kuznetsov: string;
  summ: string;
  polenov: string;
  guap: string;
  keyTopics: string;
}

const LECTURE_INDEX: LectureIndexItem[] = [
  {
    number: 'Лекция 1',
    date: '02.09.2026',
    title: 'Введение в нанотехнологии. Основные понятия и масштабы',
    kuznetsov: 'Глава 1 (§1.1–§1.3, история, классификация 3D–0D, мезоскопический масштаб)',
    summ: 'Введение (дисперсность и классификация)',
    polenov: 'Введение, Гл. 1 (§1.1)',
    guap: 'Лекция 1 (Задачи физики наносистем)',
    keyTopics: 'Масштабы 1–100 нм, 0D (квантовые точки), 1D (нити), 2D (ямы), 3D (нанокомпозиты), закон Мура.'
  },
  {
    number: 'Лекция 2',
    date: '16.09.2026',
    title: 'Особенности термодинамики наноструктур: фазы и плавление',
    kuznetsov: 'Глава 2 (§2.1–§2.3, размерные фазовые переходы); Глава 3 (§3.1, зародышеобразование)',
    summ: 'Часть 1: Гл. 1 (§1.1–§1.3, поверхностная энергия Гиббса)',
    polenov: 'Глава 1 (§1.2–§1.4), Глава 2 (§2.1–§2.3)',
    guap: 'Лекция 2 (Термодинамика наносостояния)',
    keyTopics: 'Правило фаз Гиббса, критический радиус зародыша (Гиббс-Фольмер), формула Томсона для температуры плавления.'
  },
  {
    number: 'Лекция 3',
    date: '30.09.2026',
    title: 'Дисперсные системы, золи, гели и двойной электрический слой',
    kuznetsov: 'Глава 3 (§3.3–§3.4, коллоидный и золь-гель синтез)',
    summ: 'Часть 2: Гл. 3 (§3.1–§3.5, стр. 55–82, ДЭС); Гл. 4 (стр. 83–105, ДЛФО); Гл. 5 (стр. 106–122, мицеллы)',
    polenov: 'Глава 3 (§3.1–§3.3, золи, гели, строение мицелл)',
    guap: 'Лекция 3 (Коллоидные наносистемы)',
    keyTopics: 'Строение мицеллы, дзета-потенциал, потенциал протекания, теория ДЛФО, порог коагуляции, правило Шульце-Гарди.'
  },
  {
    number: 'Лекция 4',
    date: '14.10.2026',
    title: 'Поверхностные явления, адсорбция и механизмы роста нанопленок',
    kuznetsov: 'Глава 4 (§4.1–§4.4, модели Франка-ван дер Мерве, Фольмера-Вебера, Странского-Крастанова)',
    summ: 'Часть 1: Гл. 1 (§1.4–§1.8, стр. 15–35, Лаплас, Кельвин, Юнг); Гл. 2 (§2.1–§2.4, стр. 36–54, Ленгмюр, БЭТ)',
    polenov: 'Глава 1 (§1.3, §1.5, капиллярность и адсорбция)',
    guap: 'Лекция 4 (Тонкопленочные технологии)',
    keyTopics: 'Давление Лапласа, уравнение Кельвина, изотермы Ленгмюра и БЭТ, эпитаксиальный рост, квантовые точки.'
  },
  {
    number: 'Лекция 5',
    date: '28.10.2026',
    title: 'Кристаллическая решетка, дефекты и механика наноматериалов',
    kuznetsov: 'Глава 2 (§2.4–§2.6, дефекты кристаллической решетки, механические свойства)',
    summ: '—',
    polenov: 'Глава 4 (§4.1–§4.3, структура нанокристаллов и зернограничные дефекты)',
    guap: 'Лекция 5 (Дефекты и механические свойства наноматериалов)',
    keyTopics: 'Дислокации, границы зерен, закон Холла-Петча и его инверсия, эффект памяти формы (нитинол).'
  },
  {
    number: 'Лекция 6',
    date: '11.11.2026',
    title: 'Электрофизические свойства: зонная теория и гетероструктуры',
    kuznetsov: 'Глава 5 (§5.1–§5.3, электронная структура и зонный спектр нанополупроводников)',
    summ: '—',
    polenov: 'Глава 4 (§4.4–§4.5, электрофизика наноструктур)',
    guap: 'Лекции 2–3 (Зонная теория, гетеропереходы, 2D-электронный газ)',
    keyTopics: 'Плотность состояний g(E), треугольная квантовая яма, 2DEG на AlGaAs/GaAs, HEMT-транзисторы.'
  },
  {
    number: 'Лекция 7',
    date: '25.11.2026',
    title: 'Квантово-размерные эффекты и квантовый транспорт',
    kuznetsov: 'Глава 5 (§5.4–§5.7, квантово-размерные эффекты, баллистический транспорт, кулоновская блокада)',
    summ: '—',
    polenov: 'Глава 5 (§5.1–§5.3, квантовый транспорт)',
    guap: 'Лекции 4–6 (Квантовые ямы, нити, точки, формула Ландауэра)',
    keyTopics: 'Длина волны де Бройля, квантовый точечный контакт, квантование проводимости (2e²/h), кулоновская блокада.'
  },
  {
    number: 'Лекция 8',
    date: '09.12.2026',
    title: 'Оптические и магнитные свойства: плазмоны, экситоны, магнетизм',
    kuznetsov: 'Глава 6 (§6.1–§6.5, плазмоны, экситоны, фотонные кристаллы); Гл. 5 (§5.8, суперпарамагнетизм)',
    summ: '—',
    polenov: 'Главы 4–5 (Оптика и магнетизм наносистем)',
    guap: 'Лекции 7–8 (Плазмоника, фотонные кристаллы)',
    keyTopics: 'Локализованный плазмонный резонанс, теория Ми, уравнение Бруса, экситоны в квантовых точках, суперпарамагнетизм, GMR.'
  },
  {
    number: 'Лекция 9',
    date: '23.12.2026',
    title: 'Низкоразмерные системы в электронике, спинтронике и углеродные структуры',
    kuznetsov: 'Глава 7 (§7.1–§7.6, фуллерены, УНТ, графен, наноэлектроника); Гл. 5 (§5.9, РТД)',
    summ: '—',
    polenov: 'Глава 5 (§5.4–§5.6, углеродные наноструктуры)',
    guap: 'Лекция 9 (Приборы наноэлектроники, графен)',
    keyTopics: 'Резонансно-туннельный диод (РТД), спинтроника, хиральность нанотрубок, конус Дирака в графене, теория перколяции.'
  }
];

interface LabIndexItem {
  number: string;
  title: string;
  kuznetsov: string;
  summ: string;
  polenov: string;
  guap: string;
}

const LAB_INDEX: LabIndexItem[] = [
  {
    number: 'ЛР №1',
    title: 'Получение наночастиц серебра (Синтез и оптический анализ)',
    kuznetsov: 'Глава 3 (§3.2–§3.3, химическое восстановление Ag); Глава 6 (§6.1, плазмонный пик)',
    summ: 'Часть 2: Глава 4 (стр. 83–95, кинетика агрегации и полимерная стабилизация ПВП)',
    polenov: 'Глава 3 (§3.2, синтез наночастиц серебра)',
    guap: 'Метод. указания к ЛР 1'
  },
  {
    number: 'ЛР №2',
    title: 'Синтез и оптика наночастиц золота методом Туркевича',
    kuznetsov: 'Глава 6 (§6.1–§6.2, плазмонный резонанс и теория Ми для золота ~520 нм)',
    summ: 'Часть 2: Глава 4 (стр. 90–95, цитратная стабилизация)',
    polenov: 'Глава 3 (§3.3, синтез нанозолота)',
    guap: 'Метод. указания к ЛР 2'
  },
  {
    number: 'ЛР №3',
    title: 'Коагуляция золя Fe(OH)₃ и проверка правила Шульце–Гарди',
    kuznetsov: 'Глава 3 (§3.3, коагуляция гидрофобных золей)',
    summ: 'Часть 2: Гл. 3 (стр. 55–75, ДЭС и дзета-потенциал); Гл. 4 (стр. 96–105, порог коагуляции, Шульце-Гарди z⁶)',
    polenov: 'Глава 3 (§3.1, гидролиз и коагуляция Fe(OH)₃)',
    guap: 'Метод. указания к ЛР 3'
  },
  {
    number: 'ЛР №4',
    title: 'Получение пористого кремния методом анодного травления',
    kuznetsov: 'Глава 4 (§4.3, электрохимическое наноструктурирование полупроводников)',
    summ: 'Часть 1: Гл. 2 (поверхностная пористость)',
    polenov: 'Глава 3 (§3.4, электрохимические методы)',
    guap: 'Метод. указания к ЛР 4'
  },
  {
    number: 'ЛР №5',
    title: 'Формирование нанопористого оксида алюминия Al₂O₃',
    kuznetsov: 'Глава 4 (§4.4, матричный темплатный синтез наномембран Al₂O₃)',
    summ: 'Часть 1: Гл. 1 (капиллярные эффекты в порах)',
    polenov: 'Глава 3 (§3.5, анодный оксид алюминия)',
    guap: 'Метод. указания к ЛР 5'
  },
  {
    number: 'ЛР №6',
    title: 'Атомно-силовая микроскопия (АСМ / СЗМ)',
    kuznetsov: 'Глава 1 (§1.4, принципы сканирующей зондовой микроскопии, кантилеверы, режимы)',
    summ: '—',
    polenov: 'Глава 4 (§4.2, методы исследования рельефа)',
    guap: 'Приложение «Методы СЗМ: АСМ и СТМ»'
  },
  {
    number: 'ЛР №7',
    title: 'Фотонные кристаллы и оптические наноструктуры',
    kuznetsov: 'Глава 6 (§6.4–§6.5, искусственные опалы, брэгговская дифракция, стоп-зона)',
    summ: '—',
    polenov: 'Глава 4 (§4.6, оптика фотонных кристаллов)',
    guap: 'Лекция 8 (Фотонные запрещенные зоны)'
  },
  {
    number: 'ЛР №8',
    title: 'Фотолюминесценция в наноструктурах оксида цинка (ZnO)',
    kuznetsov: 'Глава 6 (§6.3, люминесценция полупроводниковых нанокристаллов, экситонная и дефектная)',
    summ: '—',
    polenov: 'Глава 4 (§4.7, спектроскопия излучения)',
    guap: 'Лекция 7 (Экситонные процессы в широкозонных полупроводниках)'
  },
  {
    number: 'ЛР №9',
    title: 'Магнитооптический эффект Керра (MOKE) в наноферромагнетиках',
    kuznetsov: 'Глава 5 (§5.8, магнитные наноструктуры, доменные границы, петли гистерезиса)',
    summ: '—',
    polenov: 'Глава 5 (§5.2, магнитные нанопленки)',
    guap: 'Лекция 9 (Магнитооптика и спинтроника)'
  }
];

export const MaterialsView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'books' | 'lectureIndex' | 'labIndex'>('books');

  return (
    <div className="space-y-6">
      
      {/* Overview banner */}
      <div className="bg-emerald-50/50 p-5 rounded-2xl border border-emerald-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-emerald-950 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-emerald-700" />
            Учебно-методическая база и предметный указатель литературы
          </h2>
          <p className="text-xs text-emerald-900/80 mt-1 max-w-2xl">
            Все утвержденные документы, РПД, календарный план, оцифрованные базовые учебники (Кузнецов, Сумм, Поленов, ГУАП) и детальный тематический указатель параграфов к 9 лекциям и 9 лабораторным работам.
          </p>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          <span className="text-xs font-semibold px-3 py-1.5 rounded-xl bg-white border border-emerald-200 text-emerald-900 shadow-2xs">
            5 PDF-источников
          </span>
        </div>
      </div>

      {/* Navigation tabs */}
      <div className="flex items-center gap-2 border-b border-neutral-200 pb-2">
        <button
          onClick={() => setActiveTab('books')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'books'
              ? 'bg-emerald-700 text-white shadow-2xs'
              : 'text-neutral-600 hover:bg-neutral-100'
          }`}
        >
          <Library className="w-4 h-4" />
          Учебные пособия и документы ({BOOKS.length + 2})
        </button>
        <button
          onClick={() => setActiveTab('lectureIndex')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'lectureIndex'
              ? 'bg-emerald-700 text-white shadow-2xs'
              : 'text-neutral-600 hover:bg-neutral-100'
          }`}
        >
          <ListTree className="w-4 h-4" />
          Указатель к 9 лекциям (Параграфы)
        </button>
        <button
          onClick={() => setActiveTab('labIndex')}
          className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
            activeTab === 'labIndex'
              ? 'bg-emerald-700 text-white shadow-2xs'
              : 'text-neutral-600 hover:bg-neutral-100'
          }`}
        >
          <FlaskConical className="w-4 h-4" />
          Указатель к 9 лабораторным работам
        </button>
      </div>

      {/* TAB 1: BOOKS & DOCUMENTS */}
      {activeTab === 'books' && (
        <div className="space-y-4">
          
          {/* Key Program Documents */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* RPD Markdown Card */}
            <div className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-2xs space-y-3">
              <div className="flex items-start justify-between gap-3">
                <div className="w-10 h-10 rounded-xl bg-emerald-100/70 border border-emerald-200 flex items-center justify-center text-emerald-800 shrink-0">
                  <FileText className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                  Оцифровано (Markdown)
                </span>
              </div>

              <div>
                <h3 className="text-sm font-bold text-neutral-900">
                  Рабочая программа дисциплины (РПД)
                </h3>
                <p className="text-xs text-neutral-600 mt-1 leading-relaxed">
                  Полный текст программы: цели дисциплины, матрица компетенций (ОПК-1, ОПК-3, ОПК-5, ОПК-6, ПК-3), структура часов, тематический план 12 разделов, 18 лабораторных работ, банк расчетных задач и зачетных вопросов.
                </p>
              </div>

              <div className="pt-2 flex items-center justify-between text-xs text-neutral-500 font-mono">
                <span>/course_materials/rpd.md</span>
              </div>
            </div>

            {/* Calendar-Thematic Plan Card */}
            <div className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-2xs space-y-3">
              <div className="flex items-start justify-between gap-3">
                <div className="w-10 h-10 rounded-xl bg-blue-100/70 border border-blue-200 flex items-center justify-center text-blue-800 shrink-0">
                  <CalendarCheck className="w-5 h-5" />
                </div>
                <span className="text-[11px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">
                  Календарный план
                </span>
              </div>

              <div>
                <h3 className="text-sm font-bold text-neutral-900">
                  Календарно-тематический план (Осень 2026)
                </h3>
                <p className="text-xs text-neutral-600 mt-1 leading-relaxed">
                  Точная синхронизация тем РПД с реальным расписанием занятий группы м431к: 9 лекционных пар по нечетным неделям и 17 лабораторных занятий еженедельно с датами и номерами аудиторий.
                </p>
              </div>

              <div className="pt-2 flex items-center justify-between text-xs text-neutral-500 font-mono">
                <span>/course_materials/semester_4/calendar_thematic_plan.md</span>
              </div>
            </div>
          </div>

          <div className="pt-2">
            <h3 className="text-sm font-bold text-neutral-900 flex items-center gap-2 mb-3">
              <BookMarked className="w-4 h-4 text-emerald-700" />
              Оцифрованные учебные издания в папке <code>/course_materials/literature/</code>
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {BOOKS.map((book) => (
                <div key={book.id} className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-2xs space-y-3 flex flex-col justify-between">
                  <div className="space-y-2.5">
                    <div className="flex items-start justify-between gap-2">
                      <span className={`text-[11px] font-bold px-2 py-0.5 rounded border ${book.badgeColor}`}>
                        {book.badge}
                      </span>
                      <span className="text-[11px] text-neutral-400 font-mono">{book.year}</span>
                    </div>

                    <div>
                      <h4 className="text-sm font-bold text-neutral-900 leading-snug">{book.title}</h4>
                      <p className="text-xs font-medium text-emerald-800 mt-0.5">{book.author}</p>
                      <p className="text-[11px] text-neutral-400">{book.publisher}</p>
                    </div>

                    <p className="text-xs text-neutral-600 leading-relaxed">
                      {book.description}
                    </p>
                  </div>

                  <div className="pt-2 border-t border-neutral-100 flex items-center justify-between text-[11px] text-neutral-500 font-mono truncate">
                    <span className="truncate">{book.path}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* TAB 2: LECTURE LITERATURE INDEX */}
      {activeTab === 'lectureIndex' && (
        <div className="space-y-4">
          <div className="bg-white p-4 rounded-2xl border border-neutral-200 text-xs text-neutral-700 leading-relaxed">
            Ниже приведен постраничный и поглавный указатель учебной литературы к каждой из <strong>9 лекций</strong> 4-го семестра (по нечетным неделям). Все материалы доступны в папке <code>/course_materials/literature/</code>.
          </div>

          <div className="space-y-3">
            {LECTURE_INDEX.map((item, idx) => (
              <div key={idx} className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-2xs space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-neutral-100 pb-2.5">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-emerald-100 text-emerald-900 border border-emerald-200">
                      {item.number}
                    </span>
                    <h3 className="text-sm font-bold text-neutral-900">
                      {item.title}
                    </h3>
                  </div>
                  <span className="text-xs font-mono text-neutral-500">{item.date}</span>
                </div>

                <div className="text-xs text-neutral-600 bg-neutral-50 p-2.5 rounded-xl border border-neutral-150">
                  <span className="font-semibold text-neutral-800">Ключевые концепции: </span>
                  {item.keyTopics}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 text-xs">
                  <div className="p-2.5 rounded-xl bg-indigo-50/50 border border-indigo-150">
                    <span className="font-bold text-indigo-900 block mb-1">📘 [Кузнецов и др.]</span>
                    <p className="text-neutral-700 leading-relaxed">{item.kuznetsov}</p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-emerald-50/50 border border-emerald-150">
                    <span className="font-bold text-emerald-900 block mb-1">📗 [Сумм Б.Д.]</span>
                    <p className="text-neutral-700 leading-relaxed">{item.summ}</p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-purple-50/50 border border-purple-150">
                    <span className="font-bold text-purple-900 block mb-1">📕 [Поленов В.С. ФХОНТ]</span>
                    <p className="text-neutral-700 leading-relaxed">{item.polenov}</p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-amber-50/50 border border-amber-150">
                    <span className="font-bold text-amber-900 block mb-1">📙 [Курс лекций ГУАП]</span>
                    <p className="text-neutral-700 leading-relaxed">{item.guap}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 3: LAB LITERATURE INDEX */}
      {activeTab === 'labIndex' && (
        <div className="space-y-4">
          <div className="bg-white p-4 rounded-2xl border border-neutral-200 text-xs text-neutral-700 leading-relaxed">
            Ниже приведен указатель глав и разделов для теоретической подготовки и защиты отчетов по <strong>9 лабораторным работам</strong> (17 занятий, еженедельно).
          </div>

          <div className="space-y-3">
            {LAB_INDEX.map((lab, idx) => (
              <div key={idx} className="bg-white p-5 rounded-2xl border border-neutral-200 shadow-2xs space-y-3">
                <div className="flex items-center gap-2 border-b border-neutral-100 pb-2.5">
                  <span className="text-xs font-bold px-2.5 py-1 rounded-lg bg-teal-100 text-teal-900 border border-teal-200">
                    {lab.number}
                  </span>
                  <h3 className="text-sm font-bold text-neutral-900">
                    {lab.title}
                  </h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 text-xs">
                  <div className="p-2.5 rounded-xl bg-indigo-50/50 border border-indigo-150">
                    <span className="font-bold text-indigo-900 block mb-1">📘 [Кузнецов и др.]</span>
                    <p className="text-neutral-700 leading-relaxed">{lab.kuznetsov}</p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-emerald-50/50 border border-emerald-150">
                    <span className="font-bold text-emerald-900 block mb-1">📗 [Сумм Б.Д.]</span>
                    <p className="text-neutral-700 leading-relaxed">{lab.summ}</p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-purple-50/50 border border-purple-150">
                    <span className="font-bold text-purple-900 block mb-1">📕 [Поленов В.С. ФХОНТ]</span>
                    <p className="text-neutral-700 leading-relaxed">{lab.polenov}</p>
                  </div>

                  <div className="p-2.5 rounded-xl bg-amber-50/50 border border-amber-150">
                    <span className="font-bold text-amber-900 block mb-1">📙 [Методические материалы ГУАП]</span>
                    <p className="text-neutral-700 leading-relaxed">{lab.guap}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Control criteria and requirements */}
      <div className="bg-neutral-50 p-5 rounded-2xl border border-neutral-200 space-y-3">
        <h3 className="text-sm font-bold text-neutral-900 flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-amber-600" />
          Требования к защите лабораторных работ и допуску к дифференцированному зачету
        </h3>
        <ul className="text-xs text-neutral-700 space-y-1.5 list-disc list-inside leading-relaxed">
          <li>Оформление отчета по каждой лабораторной работе в соответствии со стандартом ГОСТ 7.32 (титульный лист, цель, схема установки, таблицы экспериментальных данных, графики, расчет погрешностей, вывод).</li>
          <li>Выполнение индивидуальных расчетных задач по теме работы с обоснованием из литературы.</li>
          <li>Устная защита отчета и ответы на контрольные вопросы по методике и теоретическим основам.</li>
          <li>Для получения допуска к дифференцированному зачету необходимо защитить все 9 лабораторных работ 4-го семестра.</li>
        </ul>
      </div>

    </div>
  );
};
