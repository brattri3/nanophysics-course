import React from 'react';
import { SlideViewer } from './SlideViewer';
import { GibbsThomsonWidget, DensityOfStatesWidget } from './InteractiveWidgets';
import { MathView } from './MathView';
import { Sparkles, Layers, Box, Cpu, ChevronRight, Scaling, Atom, Maximize, Activity, Zap, CheckCircle2 } from 'lucide-react';

// SLIDE 1: COVER
const CoverSlide = () => (
  <div className="flex flex-col items-center justify-center h-full text-center space-y-6 my-auto py-4">
    <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center rotate-45 shadow-[0_0_40px_rgba(16,185,129,0.3)]">
      <div className="w-6 h-6 sm:w-8 sm:h-8 border-2 border-white/90 rounded-sm -rotate-45" />
    </div>
    
    <div className="space-y-4">
      <span className="text-xs sm:text-sm font-mono tracking-widest text-emerald-400 uppercase">
        Лекция №1 • 02.09.2026 • 2 академических часа (90 мин)
      </span>
      <h1 className="text-3xl sm:text-5xl md:text-6xl font-bold font-['Newsreader'] text-white tracking-tight leading-tight max-w-4xl">
        Введение в физику нанотехнологий: <br className="hidden sm:inline" />
        <span className="text-emerald-400">Масштабы, размерные эффекты и мезоскопика</span>
      </h1>
    </div>
    
    <div className="w-24 h-1.5 bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full" />
    
    <div className="text-sm sm:text-base text-neutral-400 space-y-1">
      <p className="font-semibold text-neutral-300">Дисциплина: «Физические основы нанотехнологий» (03.03.01)</p>
      <p>ГУАП, Институт ФПТИ • Кафедра №3 • Группа м431к</p>
    </div>
  </div>
);

// SLIDE 2: DEFINITIONS & PARADOX
const DefinitionsSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Раздел 1 • Концептуальный базис
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Что такое нанотехнологии?
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="space-y-4">
        <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 h-full flex flex-col justify-center">
          <h3 className="text-base font-bold text-emerald-400 mb-2 border-b border-emerald-900/50 pb-2 flex items-center gap-2">
            <Layers className="w-4 h-4" /> Метрологическое определение (ISO/TS 80004)
          </h3>
          <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
            Совокупность методов и приемов контролируемого создания и модификации объектов с размерами в диапазоне <strong>1–100 нм</strong>, обладающих принципиально новыми физико-химическими свойствами за счет проявления <strong>размерных эффектов</strong>.
          </p>
        </div>
      </div>
      <div className="space-y-4">
        <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 h-full flex flex-col justify-center">
          <h3 className="text-base font-bold text-emerald-400 mb-2 border-b border-emerald-900/50 pb-2 flex items-center gap-2">
            <Atom className="w-4 h-4" /> Концепция Э. Дрекслера (Bottom-Up)
          </h3>
          <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
            Конструирование вещества методом <strong>«снизу-вверх»</strong> (атом за атомом и молекула за молекулой) с использованием молекулярных наномашин и позиционной сборки.
          </p>
        </div>
      </div>
    </div>

    <div className="bg-emerald-950/30 p-4 rounded-2xl border border-emerald-800/50 flex items-start gap-4 shadow-[0_0_30px_rgba(16,185,129,0.05)]">
      <Maximize className="w-7 h-7 text-emerald-400 shrink-0 mt-0.5" />
      <div>
        <h4 className="text-sm font-bold text-white">Мезоскопический парадокс: Нано — это маленькое или большое?</h4>
        <p className="text-xs text-neutral-300 mt-1 leading-relaxed">
          Нанообъекты не относятся к микромиру отдельных атомов. Наночастица $R=10$ нм содержит свыше $10^5$ атомов и электронов. Это <strong>мезоскопическая физика</strong>: объект слишком мал для чисто классической термодинамики, но слишком сложен для простого квантового уравнения Шрёдингера одного электрона.
        </p>
      </div>
    </div>
  </div>
);

// SLIDE 3: HISTORY & MILESTONES
const HistoryScaleSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div className="flex justify-between items-end">
      <div>
        <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
          Историческая ретроспектива
        </span>
        <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
          Генезис нанотехнологий
        </h2>
      </div>
      <div className="hidden md:flex items-center gap-2 bg-blue-950/40 border border-blue-800/50 px-3 py-1.5 rounded-xl text-blue-300">
        <Cpu className="w-4 h-4" />
        <span className="text-xs font-bold font-mono">Современный техпроцесс: &lt; 3 нм (GAAFET)</span>
      </div>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
      <div className="bg-neutral-950/70 p-4 rounded-xl border border-neutral-800 flex flex-col justify-center">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold px-2.5 py-0.5 rounded bg-indigo-950 border border-indigo-700 text-indigo-300 font-mono">1959</span>
          <span className="text-xs text-neutral-400">Ричард Фейнман (Caltech)</span>
        </div>
        <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
          Лекция <em>«There's Plenty of Room at the Bottom»</em>: теоретическое предсказание прямой манипуляции атомами, атомной записи информации и синтеза субмикронных устройств.
        </p>
      </div>

      <div className="bg-neutral-950/70 p-4 rounded-xl border border-neutral-800 flex flex-col justify-center">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold px-2.5 py-0.5 rounded bg-emerald-950 border border-emerald-700 text-emerald-300 font-mono">1981 / 1986</span>
          <span className="text-xs text-neutral-400">Бинниг и Рорер (IBM Zurich)</span>
        </div>
        <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
          Изобретение <strong>Сканирующего туннельного микроскопа (СТМ)</strong> и <strong>АСМ</strong>. Человечество впервые получило «глаза и руки» для визуализации и перемещения одиночных атомов (Нобелевская премия 1986).
        </p>
      </div>

      <div className="bg-neutral-950/70 p-4 rounded-xl border border-neutral-800 flex flex-col justify-center">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold px-2.5 py-0.5 rounded bg-amber-950 border border-amber-700 text-amber-300 font-mono">1985 / 1991</span>
          <span className="text-xs text-neutral-400">Крото, Смолли / Иидзима</span>
        </div>
        <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
          Открытие аллотропных форм углерода пониженной размерности: фуллеренов $C_{60}$ (0D) и углеродных нанотрубок (1D).
        </p>
      </div>

      <div className="bg-neutral-950/70 p-4 rounded-xl border border-neutral-800 flex flex-col justify-center">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold px-2.5 py-0.5 rounded bg-cyan-950 border border-cyan-700 text-cyan-300 font-mono">2004</span>
          <span className="text-xs text-neutral-400">Гейм и Новоселов</span>
        </div>
        <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed">
          Выделение <strong>графена</strong> — первого истинно двумерного (2D) кристаллического материала толщиной в один атом углерода (Нобелевская премия 2010).
        </p>
      </div>
    </div>
  </div>
);

// SLIDE 4: SURFACE-TO-VOLUME SCALING
const SurfaceScalingSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Геометрия и термодинамика
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Доминирование поверхности: Парадокс масштабирования $S/V$
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1 items-stretch">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-neutral-800 pb-2">
          Математический вывод доли поверхностных атомов
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Для сферической наночастицы радиуса $R$ с моноатомным поверхностным слоем толщиной $a$:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl text-center border border-neutral-800">
          <MathView math="\alpha(R) = \frac{N_{\text{surf}}}{N_{\text{total}}} \approx \frac{V_{\text{surf}}}{V_{\text{total}}} = \frac{4\pi R^2 a}{\frac{4}{3}\pi R^3} = \frac{3a}{R}" />
        </div>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Удельная площадь поверхности порошка из сферических частиц плотностью $\rho$:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl text-center border border-neutral-800">
          <MathView math="S_{\text{уд}} = \frac{S_{\text{total}}}{m} = \frac{3}{\rho R}" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between">
        <h3 className="text-sm font-bold text-white border-b border-neutral-800 pb-2 flex items-center justify-between">
          <span>Сравнение масштабов (1 грамм Au)</span>
          <span className="text-xs font-mono text-emerald-400 font-normal">$\rho = 19.3\text{ г/см}^3$</span>
        </h3>
        
        <div className="space-y-2.5 my-auto text-xs">
          <div className="flex justify-between items-center p-2.5 rounded-lg bg-neutral-900/60 border border-neutral-800/80">
            <span className="text-neutral-400">Макросфера ($R = 2.3$ мм):</span>
            <span className="font-mono text-white font-bold">$S = 0.66\text{ см}^2$, $\alpha \approx 0.0001\%$</span>
          </div>
          <div className="flex justify-between items-center p-2.5 rounded-lg bg-neutral-900/60 border border-neutral-800/80">
            <span className="text-neutral-400">Микрочастицы ($R = 1$ мкм):</span>
            <span className="font-mono text-white font-bold">$S = 0.16\text{ м}^2$, $\alpha \approx 0.09\%$</span>
          </div>
          <div className="flex justify-between items-center p-2.5 rounded-lg bg-emerald-950/40 border border-emerald-800/60">
            <span className="text-emerald-300 font-semibold">Наночастицы ($R = 2$ нм):</span>
            <span className="font-mono text-emerald-400 font-bold">$S = 78\text{ м}^2$, $\alpha \approx 45\%$</span>
          </div>
        </div>

        <div className="text-[11px] text-neutral-400 italic bg-neutral-900/30 p-2 rounded-lg border border-neutral-800/40">
          * Избыточная энергия Гиббса $G_s = \sigma S$ делает наночастицы сверхреакционноспособными катализаторами.
        </div>
      </div>
    </div>
  </div>
);

// SLIDE 5: GIBBS-THOMSON INTERACTIVE
const GibbsThomsonSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-4">
    <GibbsThomsonWidget />
  </div>
);

// SLIDE 6: CHARACTERISTIC LENGTH SCALES
const ScalesSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Квантовая физика и кинетика
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Характеристические физические длины
      </h2>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 flex-1">
      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2 flex flex-col justify-between">
        <div>
          <h3 className="text-sm font-bold text-emerald-400 flex items-center justify-between">
            <span>1. Длина волны де Бройля ($\lambda_{dB}$)</span>
            <span className="text-xs font-mono text-neutral-400 font-normal">Квантование</span>
          </h3>
          <div className="my-2 bg-neutral-900/80 p-2 rounded text-center text-xs">
            <MathView math="\lambda_{dB} = \frac{h}{p} = \frac{h}{\sqrt{2m^* E_F}}" />
          </div>
          <p className="text-xs text-neutral-300 leading-relaxed">
            В металлах $\lambda_{dB} \le 0.5$ нм. В полупроводниках (GaAs, InSb, $m^* \ll m_0$) $\lambda_{dB} \approx 20–50$ нм. При $L \le \lambda_{dB}$ спектр становится дискретным.
          </p>
        </div>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2 flex flex-col justify-between">
        <div>
          <h3 className="text-sm font-bold text-emerald-400 flex items-center justify-between">
            <span>2. Длина свободного пробега ($l_e$)</span>
            <span className="text-xs font-mono text-neutral-400 font-normal">Баллистика</span>
          </h3>
          <div className="my-2 bg-neutral-900/80 p-2 rounded text-center text-xs">
            <MathView math="l_e = v_F \cdot \tau_e" />
          </div>
          <p className="text-xs text-neutral-300 leading-relaxed">
            Расстояние между упругими столкновениями. При $L \le l_e$ электрон пролетает проводник без рассеяния — возникает <strong>баллистический транспорт</strong>.
          </p>
        </div>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2 flex flex-col justify-between">
        <div>
          <h3 className="text-sm font-bold text-emerald-400 flex items-center justify-between">
            <span>3. Экситонный радиус Бора ($a_{ex}$)</span>
            <span className="text-xs font-mono text-neutral-400 font-normal">Квантовые точки</span>
          </h3>
          <div className="my-2 bg-neutral-900/80 p-2 rounded text-center text-xs">
            <MathView math="a_{ex} = \frac{4\pi \varepsilon \varepsilon_0 \hbar^2}{\mu e^2}, \quad \mu = \left(\frac{1}{m_e^*} + \frac{1}{m_h^*}\right)^{-1}" />
          </div>
          <p className="text-xs text-neutral-300 leading-relaxed">
            Размер связанной пары электрон-дырка. При $R \le a_{ex}$ запрещенная зона квантовой точки увеличивается (эффект Бруса).
          </p>
        </div>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2 flex flex-col justify-between">
        <div>
          <h3 className="text-sm font-bold text-emerald-400 flex items-center justify-between">
            <span>4. Длина фазовой когерентности ($l_\phi$)</span>
            <span className="text-xs font-mono text-neutral-400 font-normal">Интерференция</span>
          </h3>
          <div className="my-2 bg-neutral-900/80 p-2 rounded text-center text-xs">
            <MathView math="l_\phi = v_F \cdot \tau_{\text{inelastic}} \gg l_e \text{ (при низких T)}" />
          </div>
          <p className="text-xs text-neutral-300 leading-relaxed">
            Расстояние сохранения фазы волновой функции. При $L \le l_\phi$ наблюдаются квантовые интерференционные эффекты (эффект Ааронова-Бома).
          </p>
        </div>
      </div>
    </div>
  </div>
);

// SLIDE 7: TRANSPORT REGIMES & LANDAUER
const TransportSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Квантовая кинетика
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Смена режимов переноса: Формула Ландауэра
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1 items-stretch">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-neutral-300 border-b border-neutral-800 pb-2">
          Диффузный режим ($L \gg l_e$)
        </h3>
        <p className="text-xs text-neutral-400">Классический транспорт с многократным рассеянием электронов:</p>
        <div className="bg-neutral-900/80 p-3 rounded-xl text-center border border-neutral-800">
          <MathView math="\vec{j} = \sigma \vec{E}, \quad R = \rho \frac{L}{S}" />
        </div>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Сопротивление прямо пропорционально длине проводника $L$ (закон Ома). Рассеяние рассеивает энергию в тепло (джоулевы потери).
        </p>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-emerald-800/60 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-emerald-900/50 pb-2">
          Баллистический режим ($L \le l_e$)
        </h3>
        <p className="text-xs text-neutral-400">Транспорт без рассеяния (формула Ландауэра–Бюттикера):</p>
        <div className="bg-neutral-900/80 p-3 rounded-xl text-center border border-neutral-800 text-emerald-300">
          <MathView math="G = \frac{2e^2}{h} \sum_{n=1}^{M} T_n \quad \Longrightarrow \quad R_{\text{quant}} = \frac{h}{2e^2 M} \approx \frac{12.9\text{ кОм}}{M}" />
        </div>
        <p className="text-xs text-neutral-300 leading-relaxed">
          <strong>Фундаментальный парадокс:</strong> Сопротивление баллистического нанопроводника <strong>не зависит от его длины</strong> $L$, а определяется квантовым контактным сопротивлением $h/2e^2 \approx 12.9$ кОм на моду.
        </p>
      </div>
    </div>
  </div>
);

// SLIDE 8: CLASSIFICATION (3D -> 2D -> 1D -> 0D)
const ClassificationSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Классификация наноструктур
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Размерное квантование: 3D $\rightarrow$ 2D $\rightarrow$ 1D $\rightarrow$ 0D
      </h2>
    </div>

    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 flex-1">
      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 flex flex-col justify-between">
        <div>
          <span className="text-xs font-mono font-bold text-neutral-400 bg-neutral-900 px-2 py-0.5 rounded">3D Объем</span>
          <h3 className="text-sm font-bold text-white mt-2">Объемный кристалл</h3>
          <p className="text-[11px] text-neutral-400 mt-1">3 степени свободы движения. Нет квантового ограничения.</p>
        </div>
        <div className="bg-neutral-900/60 p-2 rounded text-center text-xs font-mono text-emerald-300">
          <MathView math="g(E) \propto \sqrt{E}" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 flex flex-col justify-between">
        <div>
          <span className="text-xs font-mono font-bold text-teal-400 bg-teal-950 px-2 py-0.5 rounded">2D Пленка</span>
          <h3 className="text-sm font-bold text-white mt-2">Квантовая яма</h3>
          <p className="text-[11px] text-neutral-400 mt-1">Ограничение по 1 оси ($z$). 2DEG в гетероструктурах, графен, $MoS_2$.</p>
        </div>
        <div className="bg-neutral-900/60 p-2 rounded text-center text-xs font-mono text-teal-300">
          <MathView math="g(E) \propto \sum \Theta(E - E_n)" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 flex flex-col justify-between">
        <div>
          <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded">1D Нить</span>
          <h3 className="text-sm font-bold text-white mt-2">Квантовая проволока</h3>
          <p className="text-[11px] text-neutral-400 mt-1">Ограничение по 2 осям ($x,y$). УНТ, нановискеры, нанопровода Si.</p>
        </div>
        <div className="bg-neutral-900/60 p-2 rounded text-center text-xs font-mono text-cyan-300">
          <MathView math="g(E) \propto \sum \frac{1}{\sqrt{E - E_n}}" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-emerald-800/60 flex flex-col justify-between">
        <div>
          <span className="text-xs font-mono font-bold text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded">0D Точка</span>
          <h3 className="text-sm font-bold text-white mt-2">Квантовая точка</h3>
          <p className="text-[11px] text-neutral-400 mt-1">Ограничение по 3 осям ($x,y,z$). «Искусственный атом», фуллерены.</p>
        </div>
        <div className="bg-neutral-900/60 p-2 rounded text-center text-xs font-mono text-emerald-300">
          <MathView math="g(E) \propto \sum \delta(E - E_n)" />
        </div>
      </div>
    </div>
  </div>
);

// SLIDE 9: DENSITY OF STATES INTERACTIVE
const DensityOfStatesSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-4">
    <DensityOfStatesWidget />
  </div>
);

// SLIDE 10: SUMMARY & LAB LINK
const SummarySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Итоги лекции и лабораторный практикум
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Ключевые выводы и мостик к Лабораторной работе №1
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-neutral-800 pb-2">
          Резюме Лекции №1
        </h3>
        <ul className="text-xs text-neutral-300 space-y-2.5">
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Геометрический фактор:</strong> При <MathView math="R \le 10\text{ нм}" /> доля поверхностных атомов <MathView math="\alpha(R) \sim 1/R" /> достигает десятков процентов, определяя избыточную энергию Гиббса и падение температуры плавления.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Квантовый фактор:</strong> При сопоставлении размеров с <MathView math="\lambda_{dB}" /> и <MathView math="a_{ex}" /> спектр электронов квантуется от параболы (3D) к ступеням (2D) и дельта-пикам (0D).</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Транспортный фактор:</strong> При <MathView math="L \le l_e" /> перенос становится баллистическим с квантованной проводимостью <MathView math="G = \frac{2e^2}{h} M" />.</span>
          </li>
        </ul>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-emerald-800/60 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-white border-b border-emerald-900/50 pb-2 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-emerald-400" />
          Связь с Лабораторной работой №1
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          <strong>Тема ЛР-1: «Получение наночастиц серебра методом химического восстановления».</strong>
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs space-y-1.5 text-neutral-300">
          <p>• На практике исследуем коллоидный синтез наночастиц Ag (<MathView math="R \sim 5\text{--}20\text{ нм}" />).</p>
          <p>• Наблюдаем изменение оптических свойств: спектр поглощения плазмонного резонанса (<MathView math="\lambda_{\text{LSPR}} \approx 400\text{--}420\text{ нм}" />).</p>
          <p>• Применим теорию ДЛФО для стабилизации наночастиц цитратом натрия.</p>
        </div>
      </div>
    </div>
  </div>
);

// MAIN EXPORT
export const Lecture1: React.FC = () => {
  const slides = [
    <CoverSlide key="1" />,
    <DefinitionsSlide key="2" />,
    <HistoryScaleSlide key="3" />,
    <SurfaceScalingSlide key="4" />,
    <GibbsThomsonSlide key="5" />,
    <ScalesSlide key="6" />,
    <TransportSlide key="7" />,
    <ClassificationSlide key="8" />,
    <DensityOfStatesSlide key="9" />,
    <SummarySlide key="10" />
  ];

  return <SlideViewer slides={slides} courseTitle="Физические основы нанотехнологий • Лекция №1" />;
};
