import React from 'react';
import { SlideViewer } from './SlideViewer';
import { DLFOWidget, EDLWidget } from './InteractiveWidgets';
import { MathView } from './MathView';
import { Sparkles, Layers, Box, Cpu, ChevronRight, Scaling, Atom, Maximize, Activity, Zap, CheckCircle2, ShieldAlert, Waves, RefreshCw } from 'lucide-react';

// SLIDE 1: COVER
const CoverSlide = () => (
  <div className="flex flex-col items-center justify-center h-full text-center space-y-6 my-auto py-4">
    <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-tr from-cyan-500 to-emerald-400 flex items-center justify-center rotate-45 shadow-[0_0_40px_rgba(6,182,212,0.25)]">
      <Waves className="w-8 h-8 text-neutral-950 -rotate-45" />
    </div>

    <div className="space-y-4">
      <span className="text-xs sm:text-sm font-mono tracking-widest text-cyan-400 uppercase">
        Лекция №3 • 30.09.2026 • 2 академических часа (90 мин)
      </span>
      <h1 className="text-3xl sm:text-5xl md:text-6xl font-bold font-['Newsreader'] text-white tracking-tight leading-tight max-w-4xl">
        Термодинамика дисперсных систем: <br className="hidden sm:inline" />
        <span className="text-cyan-400">Двойной электрический слой и теория ДЛФО</span>
      </h1>
    </div>

    <div className="w-24 h-1.5 bg-gradient-to-r from-cyan-500 to-emerald-400 rounded-full" />

    <div className="text-sm sm:text-base text-neutral-400 space-y-1">
      <p className="font-semibold text-neutral-300">Дисциплина: «Физические основы нанотехнологий» (03.03.01)</p>
      <p>ГУАП, Институт ФПТИ • Кафедра №3 • Группа м431к</p>
    </div>
  </div>
);

// SLIDE 2: CLASSIFICATION OF DISPERSE SYSTEMS
const ClassificationSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 px-3 py-1 rounded">
        Раздел 2 • Дисперсные наносистемы
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Классификация дисперсных систем и критерий Ребиндера
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-cyan-400 border-b border-cyan-900/50 pb-2">
          Шкала дисперсности по размеру фаз
        </h3>
        <ul className="text-xs sm:text-sm text-neutral-300 space-y-2.5">
          <li className="p-2 bg-neutral-900/60 rounded-lg border border-neutral-800">
            <strong>Истинные растворы (<MathView math="d < 1\text{ нм}" />):</strong> Гомогенные молекулярные/ионные смеси. Термодинамически равновесны.
          </li>
          <li className="p-2 bg-cyan-950/40 rounded-lg border border-cyan-800/50">
            <strong>Коллоидные нанодисперсии (<MathView math="1\text{--}100\text{ нм}" />):</strong> Микрогетерогенные системы, развитая межфазная граница. Оптический эффект Тиндаля, броуновское движение.
          </li>
          <li className="p-2 bg-neutral-900/60 rounded-lg border border-neutral-800">
            <strong>Грубодисперсные системы (<MathView math="d > 100\text{ нм}" />):</strong> Суспензии, эмульсии, порошки. Седиментационно неустойчивы.
          </li>
        </ul>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-emerald-900/50 pb-2">
          Лиофильные vs Лиофобные системы (Критерий Ребиндера)
        </h3>
        <div className="space-y-3 text-xs sm:text-sm text-neutral-300">
          <div className="bg-emerald-950/30 p-3 rounded-xl border border-emerald-800/40">
            <span className="font-bold text-emerald-300 block mb-1">Лиофильные (термодинамически стабильные):</span>
            Межфазное натяжение <MathView math="\sigma < \sigma_c \approx 10^{-2}\text{ мДж/м}^2" />. Энтропия компенсирует энергию: <MathView math="\Delta G = \Delta H - T\Delta S < 0" /> (самопроизвольное диспергирование, растворы ПАВ выше ККМ).
          </div>
          <div className="bg-rose-950/30 p-3 rounded-xl border border-rose-800/40">
            <span className="font-bold text-rose-300 block mb-1">Лиофобные (метастабильные):</span>
            Высокая поверхностная энергия <MathView math="\sigma \gg \sigma_c" />, <MathView math="G_s = \sigma A > 0" />. Стремятся к коагуляции. Требуют электростатической или стерической стабилизации (золи Au, Ag, оксидов).
          </div>
        </div>
      </div>
    </div>
  </div>
);

// SLIDE 3: COLLOIDAL MICELLE ANATOMY
const MicelleAnatomySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Строение наночастицы в растворе
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Анатомия коллоидной мицеллы гидрозоля
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-emerald-900/50 pb-2">
          Формула строения мицеллы золя Fe(OH)₃
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          При гидролизе <MathView math="\text{FeCl}_3" /> в избытке соли наночастица приобретает положительный заряд:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs font-mono text-center text-emerald-300">
          <MathView math="\{ m[\text{Fe(OH)}_3] \cdot n\text{FeO}^+ \cdot (n-x)\text{Cl}^- \}^{x+} \cdot x\text{Cl}^-" />
        </div>
        <div className="space-y-1 text-xs text-neutral-300">
          <p>• <strong>Ядро:</strong> <MathView math="m[\text{Fe(OH)}_3]" /> — агрегат из кристаллической решетки (10³–10⁵ молекул).</p>
          <p>• <strong>ПОИ (потенциалопределяющие):</strong> <MathView math="n\text{FeO}^+" /> хемосорбированы на ядре.</p>
          <p>• <strong>Адсорбционный слой:</strong> <MathView math="(n-x)\text{Cl}^-" /> связаны кулоновскими силами.</p>
          <p>• <strong>Гранула (коллоидная частица):</strong> заряд <MathView math="+x" />, перемещается при электрофорезе.</p>
          <p>• <strong>Диффузный слой:</strong> <MathView math="x\text{Cl}^-" /> экранируют заряд в растворе.</p>
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-amber-400 border-b border-amber-900/50 pb-2">
          Правило Панета–Фаянса адсорбции ионов
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          На поверхности твердого ядра преимущественно адсорбируются те ионы, которые входят в состав кристаллической решетки ядра или образуют с его ионами труднорастворимое соединение.
        </p>
        <div className="bg-amber-950/30 p-3 rounded-xl border border-amber-800/50 text-xs space-y-2 text-neutral-200">
          <p className="font-bold text-amber-400">Пример золя иодида серебра AgI:</p>
          <p>• При избытке <MathView math="\text{AgNO}_3" />: ПОИ = <MathView math="\text{Ag}^+" /> <span className="text-emerald-400">(положительный золь)</span></p>
          <p>• При избытке <MathView math="\text{KI}" />: ПОИ = <MathView math="\text{I}^-" /> <span className="text-rose-400">(отрицательный золь)</span></p>
        </div>
        <p className="text-xs text-neutral-400">
          Знак заряда определяет чувствительность к коагуляции катионами или анионами!
        </p>
      </div>
    </div>
  </div>
);

// SLIDE 4: EDL ELECTROSTATICS & POISSON-BOLTZMANN
const EDLTheorySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 px-3 py-1 rounded">
        Электростатика границы раздела
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Уравнение Пуассона–Больцмана и длина Дебая <MathView math="\kappa^{-1}" />
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-cyan-400 border-b border-cyan-900/50 pb-2">
          Вывод распределения потенциала в диффузном слое
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Уравнение Пуассона <MathView math="\frac{d^2\psi}{dx^2} = -\frac{\rho(x)}{\varepsilon\varepsilon_0}" /> и распределение Больцмана для плотности заряда <MathView math="\rho(x) = -2zec_0\sinh\left(\frac{ze\psi}{k_BT}\right)" />:
        </p>
        <div className="bg-neutral-900/80 p-2.5 rounded-xl border border-neutral-800 text-center text-xs font-mono text-cyan-300">
          <MathView math="\frac{d^2\psi}{dx^2} = \frac{2zec_0}{\varepsilon\varepsilon_0} \sinh\left(\frac{ze\psi}{k_BT}\right)" />
        </div>
        <p className="text-xs text-neutral-300">
          При <MathView math="ze\psi \ll k_BT" /> (приближение Дебая–Хюккеля): <MathView math="\frac{d^2\psi}{dx^2} = \kappa^2 \psi(x)" />
        </p>
        <div className="bg-cyan-950/40 p-2.5 rounded-xl border border-cyan-800/80 text-center text-xs font-mono text-white">
          <MathView math="\psi(x) = \psi_0 \exp(-\kappa x)" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-emerald-900/50 pb-2">
          Дебаевская длина экранирования <MathView math="\kappa^{-1}" />
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Характеристическая толщина диффузного экранирующего облака ионов:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-emerald-300">
          <MathView math="\kappa = \sqrt{\frac{2e^2 N_A I}{\varepsilon\varepsilon_0 k_B T}}, \quad d_{Debye} = \kappa^{-1} \propto \frac{1}{\sqrt{I}}" />
        </div>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs space-y-1 text-neutral-300">
          <p>• Чистая вода (<MathView math="I \approx 10^{-7}\text{ М}" />): <MathView math="\kappa^{-1} \approx 960\text{ нм}" /></p>
          <p>• Физиологический раствор (<MathView math="0.15\text{ М NaCl}" />): <MathView math="\kappa^{-1} \approx 0.8\text{ нм}" /></p>
          <p className="text-rose-400 font-semibold">• Сжатие ДЭС при росте солености — главная причина солевой коагуляции!</p>
        </div>
      </div>
    </div>
  </div>
);

// SLIDE 5: EDL SIMULATOR
const EDLSimulatorSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-4">
    <EDLWidget />
  </div>
);

// SLIDE 6: ZETA-POTENTIAL & ELECTROPHORESIS
const ZetaPotentialSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-amber-400 bg-amber-950/60 border border-amber-800/60 px-3 py-1 rounded">
        Электрокинетические явления
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Дзета-потенциал <MathView math="\zeta" /> и уравнение Смолуховского
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-amber-400 border-b border-amber-900/50 pb-2">
          Плоскость скольжения и электрокинетический потенциал
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          При движении частицы в жидкости гидратная оболочка движется вместе с ней. Потенциал на границе скольжения называется <strong><MathView math="\zeta" />-потенциалом</strong>:
        </p>
        <div className="bg-amber-950/40 p-3 rounded-xl border border-amber-800/80 text-center text-xs font-mono text-amber-300">
          <MathView math="\zeta = \psi(x_{slip}) < \psi_\delta < \psi_0" />
        </div>
        <div className="space-y-1.5 text-xs text-neutral-300">
          <p className="text-emerald-400 font-semibold">• <MathView math="|\zeta| \ge 30\text{ мВ}" />: Высокая устойчивость (электростатический барьер блокирует сближение).</p>
          <p className="text-rose-400 font-semibold">• <MathView math="|\zeta| < 15\text{--}20\text{ мВ}" />: Порог коагуляции (быстрое выпадение осадка).</p>
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-cyan-400 border-b border-cyan-900/50 pb-2">
          Уравнение Смолуховского (Электрофорез)
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Скорость перемещения наночастиц в постоянном электрическом поле напряженностью <MathView math="E" />:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-cyan-300">
          <MathView math="u_e = \frac{v}{E} = \frac{\varepsilon \varepsilon_0 \zeta}{\eta}" />
        </div>
        <p className="text-xs text-neutral-400">
          где <MathView math="u_e" /> — электрофоретическая подвижность, <MathView math="\eta" /> — динамическая вязкость растворителя. Метод лазерного доплеровского электрофореза (ELS) позволяет измерять <MathView math="\zeta" /> за 30 секунд.
        </p>
      </div>
    </div>
  </div>
);

// SLIDE 7: DLVO THEORY BALANCE
const DLVOTheorySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Теория устойчивости коллоидов
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Теория ДЛФО: суперпозиция сил Ван-дер-Ваальса и ДЭС
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-emerald-900/50 pb-2">
          Баланс потенциальной энергии взаимодействия
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Для двух сфер радиуса <MathView math="r" /> на расстоянии <MathView math="h" /> между поверхностями:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-emerald-300">
          <MathView math="U_{\text{total}}(h) = U_{vdW}(h) + U_{el}(h)" />
        </div>
        <div className="space-y-2 text-xs text-neutral-300">
          <p>• <strong>Ван-дер-Ваальс (<MathView math="U_{vdW} < 0" />):</strong> <MathView math="U_{vdW} = - \frac{A_H r}{12 h}" /> (притяжение, <MathView math="A_H \sim 10^{-19}\text{ Дж}" /> — константа Гамакера).</p>
          <p>• <strong>Электростатика ДЭС (<MathView math="U_{el} > 0" />):</strong> <MathView math="U_{el} = 2\pi\varepsilon\varepsilon_0 r \psi_0^2 \ln(1 + e^{-\kappa h})" /> (отталкивание).</p>
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-white border-b border-neutral-800 pb-2">
          Анатомия потенциальной кривой ДЛФО
        </h3>
        <ul className="text-xs text-neutral-300 space-y-2">
          <li className="p-2 bg-rose-950/30 rounded-lg border border-rose-900/40">
            <span className="font-bold text-rose-400 block">1. Первичный минимум (h &lt; 0.4 нм):</span>
            Глубокая потенциальная яма (<MathView math="U \to -\infty" />). Необратимая коагуляция и срастание зерен.
          </li>
          <li className="p-2 bg-emerald-950/30 rounded-lg border border-emerald-900/40">
            <span className="font-bold text-emerald-400 block">2. Барьер отталкивания U_max:</span>
            Если <MathView math="U_{\max} > 15\ k_B T" />, тепловые флуктуации не могут сблизить частицы — золь стабилен.
          </li>
          <li className="p-2 bg-blue-950/30 rounded-lg border border-blue-900/40">
            <span className="font-bold text-blue-400 block">3. Вторичный минимум (h ~ 2–5 κ⁻¹):</span>
            Неглубокий минимум (<MathView math="\sim 1\text{--}3\ k_B T" />). Обратимая флокуляция и тиксотропные гели.
          </li>
        </ul>
      </div>
    </div>
  </div>
);

// SLIDE 8: DLVO SIMULATOR
const DLVOSimulatorSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-4">
    <DLFOWidget />
  </div>
);

// SLIDE 9: SCHULZE-HARDY RULE DERIVATION
const SchulzeHardySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-rose-400 bg-rose-950/60 border border-rose-800/60 px-3 py-1 rounded">
        Коагуляция электролитами
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Правило Шульце–Гарди: строгий вывод закона <MathView math="z^{-6}" />
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-rose-400 border-b border-rose-900/50 pb-2">
          Условие критического порога коагуляции C_k
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Барьер отталкивания касается оси абсцисс (<MathView math="U_{\text{total}} = 0" /> и <MathView math="dU_{\text{total}}/dh = 0" />). Отсюда <MathView math="h_c = 1/\kappa_c" />:
        </p>
        <div className="bg-rose-950/40 p-3 rounded-xl border border-rose-800/80 text-center text-xs font-mono text-white">
          <MathView math="C_k = \frac{\text{const}}{z^6} \cdot \frac{(\varepsilon\varepsilon_0)^3 (k_B T)^5 \gamma^4}{e^2 A_H^2} \propto \frac{1}{z^6}" />
        </div>
        <p className="text-xs text-neutral-400">
          где <MathView math="z" /> — заряд противоиона, <MathView math="\gamma = \tanh\left(\frac{ze\psi_0}{4k_BT}\right)" />.
        </p>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-amber-400 border-b border-amber-900/50 pb-2">
          Экспериментальное соотношение порогов коагуляции
        </h3>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs font-mono text-center text-amber-300">
          <MathView math="C_k(1+) : C_k(2+) : C_k(3+) = \frac{1}{1^6} : \frac{1}{2^6} : \frac{1}{3^6} \approx 1000 : 15 : 1.4" />
        </div>
        <ul className="text-xs text-neutral-300 space-y-1.5">
          <li>• <MathView math="\text{NaCl}" /> (<MathView math="z=1" />): <MathView math="C_k \approx 50\text{ ммоль/л}" /></li>
          <li>• <MathView math="\text{Na}_2\text{SO}_4" /> (<MathView math="z=2" />): <MathView math="C_k \approx 0.8\text{ ммоль/л}" /> <span className="text-amber-400 font-semibold">(в ~60 раз эффективнее)</span></li>
          <li>• <MathView math="\text{K}_3[\text{Fe(CN)}_6]" /> (<MathView math="z=3" />): <MathView math="C_k \approx 0.08\text{ ммоль/л}" /> <span className="text-rose-400 font-semibold">(в ~700 раз эффективнее!)</span></li>
        </ul>
      </div>
    </div>
  </div>
);

// SLIDE 10: SUMMARY & PREVIEW
const SummarySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Итоги лекции
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Ключевые выводы и мостик к ЛР №2 и Лекции №4
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-neutral-800 pb-2">
          Резюме Лекции №3
        </h3>
        <ul className="text-xs text-neutral-300 space-y-2.5">
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Структура ДЭС:</strong> Состоит из плотного слоя Штерна (<MathView math="x < x_1" />) и диффузного слоя Гуи, толщина которого <MathView math="\kappa^{-1} \propto 1/\sqrt{I}" />.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Дзета-потенциал:</strong> Потенциал на плоскости скольжения <MathView math="\zeta \ge 30\text{ мВ}" /> гарантирует барьер отталкивания <MathView math="U_{\max} > 15\ k_B T" />.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Правило Шульце–Гарди:</strong> Порог коагуляции <MathView math="C_k \propto z^{-6}" /> определяет резкую чувствительность золей к поливалентным ионам.</span>
          </li>
        </ul>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-cyan-800/60 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-white border-b border-cyan-900/50 pb-2 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-cyan-400" />
          Анонс Лекции №4 (14.10.2026)
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          <strong>Тема: «Поверхностные явления, капиллярность и механизмы роста нанопленок».</strong>
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs space-y-1.5 text-neutral-300">
          <p>• Давление Лапласа и капиллярное давление в нанопорах.</p>
          <p>• Уравнение Кельвина (Томсона) для давления насыщенного пара над нанокаплями.</p>
          <p>• Механизмы эпитаксиального роста тонких пленок: Франка–ван дер Мерве, Фольмера–Вебера, Странского–Крастанова.</p>
        </div>
      </div>
    </div>
  </div>
);

// BOARD PLAN & NOTES CONTENT FOR LECTURE 3
const Lecture3Notes = () => (
  <div className="space-y-6 text-xs sm:text-sm leading-relaxed">
    <div className="border-b border-neutral-800 pb-4">
      <span className="text-xs font-mono text-cyan-400 font-bold uppercase tracking-wider">План работы у доски и академический конспект</span>
      <h2 className="text-xl font-bold font-['Newsreader'] text-white mt-1">Лекция №3: Термодинамика дисперсных систем, ДЭС и теория ДЛФО</h2>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-cyan-400 border-b border-neutral-800 pb-1">ДОСКА 1: Электростатика ДЭС и длина Дебая</h3>
        <p className="text-neutral-300">• Уравнение Пуассона–Больцмана:</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-cyan-300">
          <MathView math="\frac{d^2\psi}{dx^2} = \kappa^2 \psi(x) \quad \Longrightarrow \quad \psi(x) = \psi_0 e^{-\kappa x}" />
        </div>
        <p className="text-neutral-400 text-xs">Дебаевская толщина: <MathView math="\kappa^{-1} = \sqrt{\frac{\varepsilon\varepsilon_0 k_B T}{2 e^2 N_A I}} \propto \frac{1}{\sqrt{I}}" /></p>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-emerald-400 border-b border-neutral-800 pb-1">ДОСКА 2: Уравнение Смолуховского</h3>
        <p className="text-neutral-300">• Электрофоретическая подвижность наночастиц:</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-emerald-300">
          <MathView math="u_e = \frac{v}{E} = \frac{\varepsilon \varepsilon_0 \zeta}{\eta}" />
        </div>
        <p className="text-neutral-400 text-xs">Критерий агрегативной стабильности: <MathView math="|\zeta| \ge 30\text{ мВ}" />.</p>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-amber-400 border-b border-neutral-800 pb-1">ДОСКА 3: Баланс энергий теории ДЛФО</h3>
        <p className="text-neutral-300">• Суммарный потенциал взаимодействия:</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-amber-300">
          <MathView math="U_{\text{total}}(h) = - \frac{A_H r}{12 h} + 2\pi\varepsilon\varepsilon_0 r \psi_0^2 \ln(1 + e^{-\kappa h})" />
        </div>
        <p className="text-neutral-400 text-xs">Барьер отталкивания <MathView math="U_{\max}" /> при <MathView math="h \sim \kappa^{-1}" />.</p>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-rose-400 border-b border-neutral-800 pb-1">ДОСКА 4: Вывод правила Шульце–Гарди</h3>
        <p className="text-neutral-300">• Условие порога коагуляции (<MathView math="U=0, dU/dh=0 \Longrightarrow h_c = 1/\kappa_c" />):</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-rose-300">
          <MathView math="C_k \propto \frac{1}{z^6} \quad \Longrightarrow \quad C_k(1) : C_k(2) : C_k(3) = 1 : \frac{1}{64} : \frac{1}{729}" />
        </div>
        <p className="text-neutral-400 text-xs">Коагулирующую силу определяет заряд противоиона <MathView math="z" /> в 6-й степени.</p>
      </div>
    </div>
  </div>
);

// MAIN EXPORT
export const Lecture3: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const slides = [
    <CoverSlide key="1" />,
    <ClassificationSlide key="2" />,
    <MicelleAnatomySlide key="3" />,
    <EDLTheorySlide key="4" />,
    <EDLSimulatorSlide key="5" />,
    <ZetaPotentialSlide key="6" />,
    <DLVOTheorySlide key="7" />,
    <DLVOSimulatorSlide key="8" />,
    <SchulzeHardySlide key="9" />,
    <SummarySlide key="10" />
  ];

  return (
    <SlideViewer 
      slides={slides} 
      title="Физические основы нанотехнологий • Лекция №3: ДЭС и теория ДЛФО" 
      onClose={onClose}
      notesContent={<Lecture3Notes />}
    />
  );
};
