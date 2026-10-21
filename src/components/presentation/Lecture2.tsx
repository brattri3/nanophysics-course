import React from 'react';
import { SlideViewer } from './SlideViewer';
import { NucleationWidget, PhaseDiagramWidget } from './InteractiveWidgets';
import { MathView } from './MathView';
import { Sparkles, Layers, Box, Cpu, ChevronRight, Scaling, Atom, Maximize, Activity, Zap, CheckCircle2, Flame, RefreshCw, Gauge } from 'lucide-react';

// SLIDE 1: COVER
const CoverSlide = () => (
  <div className="flex flex-col items-center justify-center h-full text-center space-y-6 my-auto py-4">
    <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-2xl bg-gradient-to-tr from-amber-500 to-emerald-400 flex items-center justify-center rotate-45 shadow-[0_0_40px_rgba(245,158,11,0.25)]">
      <Flame className="w-8 h-8 text-neutral-950 -rotate-45" />
    </div>

    <div className="space-y-4">
      <span className="text-xs sm:text-sm font-mono tracking-widest text-amber-400 uppercase">
        Лекция №2 • 16.09.2026 • 2 академических часа (90 мин)
      </span>
      <h1 className="text-3xl sm:text-5xl md:text-6xl font-bold font-['Newsreader'] text-white tracking-tight leading-tight max-w-4xl">
        Особенности термодинамики наноструктур: <br className="hidden sm:inline" />
        <span className="text-amber-400">Фазы, нуклеация и размерное плавление</span>
      </h1>
    </div>

    <div className="w-24 h-1.5 bg-gradient-to-r from-amber-500 to-emerald-400 rounded-full" />

    <div className="text-sm sm:text-base text-neutral-400 space-y-1">
      <p className="font-semibold text-neutral-300">Дисциплина: «Физические основы нанотехнологий» (03.03.01)</p>
      <p>ГУАП, Институт ФПТИ • Кафедра №3 • Группа м431к</p>
    </div>
  </div>
);

// SLIDE 2: SMALL SYSTEMS THERMODYNAMICS (HILL'S FORMALISM)
const SmallSystemsSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-amber-400 bg-amber-950/60 border border-amber-800/60 px-3 py-1 rounded">
        Раздел 2 • Нанотермодинамика
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Почему классическая термодинамика требует пересмотра?
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <div>
          <h3 className="text-sm font-bold text-neutral-300 border-b border-neutral-800 pb-2 flex items-center gap-2">
            <Box className="w-4 h-4 text-neutral-400" /> Классический макромир ($N \to \infty$)
          </h3>
          <ul className="text-xs sm:text-sm text-neutral-300 mt-3 space-y-2">
            <li>• Потенциалы экстенсивны: $G(\lambda N) = \lambda G(N)$.</li>
            <li>• Поверхностная энергия пренебрежимо мала ($G_{surf} / G_{vol} \sim N^{-1/3} \to 0$).</li>
            <li>• Химический потенциал $\mu_0$ не зависит от геометрии образца.</li>
          </ul>
        </div>
        <div className="bg-neutral-900/60 p-2.5 rounded-xl border border-neutral-800 text-center text-xs font-mono text-neutral-400">
          <MathView math="dG = -S dT + V dP + \mu_0 dN" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-amber-800/60 flex flex-col justify-between space-y-3">
        <div>
          <h3 className="text-sm font-bold text-amber-400 border-b border-amber-900/50 pb-2 flex items-center gap-2">
            <Sparkles className="w-4 h-4" /> Наномасштаб: формализм Т. Хилла (10²–10⁶ атомов)
          </h3>
          <ul className="text-xs sm:text-sm text-neutral-300 mt-3 space-y-2">
            <li>• Доля поверхностных связей достигает <strong>10–60%</strong>.</li>
            <li>• Вводится работа образования межфазной границы <MathView math="\sigma dA" />.</li>
            <li>• Химический потенциал зависит от кривизны: <MathView math="\mu(r) = \mu_0 + \frac{2\sigma \Omega}{r}" />.</li>
          </ul>
        </div>
        <div className="bg-neutral-900/60 p-2.5 rounded-xl border border-neutral-800 text-center text-xs font-mono text-amber-300">
          <MathView math="dG = -S dT + V dP + \mu dN + \sigma dA" />
        </div>
      </div>
    </div>

    <div className="bg-amber-950/30 p-4 rounded-2xl border border-amber-800/50 flex items-start gap-4">
      <Maximize className="w-6 h-6 text-amber-400 shrink-0 mt-0.5" />
      <p className="text-xs text-neutral-300 leading-relaxed">
        <strong>Ключевой вывод нанотермодинамики:</strong> В наночастицах свободная энергия Гиббса аддитивно складывается из объемного и поверхностного вкладов: <MathView math="G(r) = N \mu_0 + 4\pi r^2 \sigma" />, что радикально меняет температуры фазовых переходов и устойчивость фаз.
      </p>
    </div>
  </div>
);

// SLIDE 3: NUCLEATION THEORY (GIBBS-VOLMER)
const NucleationTheorySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Фазообразование • Теория Гиббса–Фольмера
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Баланс свободной энергии при гомогенной нуклеации
      </h2>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-rose-900/50 flex flex-col justify-between">
        <div>
          <span className="text-xs font-mono font-bold text-rose-400 bg-rose-950/80 px-2 py-0.5 rounded">
            Объемный вклад $\Delta G_{vol} &lt; 0$
          </span>
          <h3 className="text-sm sm:text-base font-bold text-white mt-2">Движущая сила кристаллизации</h3>
          <p className="text-xs text-neutral-300 mt-2 leading-relaxed">
            При переохлаждении расплава на $\Delta T = T_m - T$ твердая фаза выгоднее жидкой. Выигрыш энергии пропорционален <strong>объему</strong> зародыша ($\sim r^3$).
          </p>
        </div>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-rose-300">
          <MathView math="\Delta G_{vol}(r) = - \frac{4}{3}\pi r^3 \Delta g_v = - \frac{4}{3}\pi r^3 \frac{\Delta H_v \Delta T}{T_m}" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-teal-900/50 flex flex-col justify-between">
        <div>
          <span className="text-xs font-mono font-bold text-teal-400 bg-teal-950/80 px-2 py-0.5 rounded">
            Поверхностный барьер $\Delta G_{surf} &gt; 0$
          </span>
          <h3 className="text-sm sm:text-base font-bold text-white mt-2">Затраты на создание границы раздела</h3>
          <p className="text-xs text-neutral-300 mt-2 leading-relaxed">
            Создание новой межфазной границы твердое тело–расплав требует затраты работы, пропорциональной <strong>площади поверхности</strong> ($\sim r^2$).
          </p>
        </div>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-teal-300">
          <MathView math="\Delta G_{surf}(r) = 4\pi r^2 \sigma_{sl}" />
        </div>
      </div>
    </div>

    <div className="bg-neutral-950/90 p-4 rounded-2xl border border-emerald-800/60 flex items-center justify-between gap-4">
      <div className="space-y-1">
        <span className="text-xs text-emerald-400 font-bold uppercase tracking-wider">Полное уравнение нуклеации</span>
        <p className="text-xs text-neutral-300">Суммарная функция имеет четко выраженный максимум при критическом радиусе $r^*$.</p>
      </div>
      <div className="bg-neutral-900 px-4 py-2 rounded-xl border border-neutral-800 text-xs sm:text-sm font-mono text-emerald-300">
        <MathView math="\Delta G(r) = - \frac{4}{3}\pi r^3 \Delta g_v + 4\pi r^2 \sigma" />
      </div>
    </div>
  </div>
);

// SLIDE 4: CRITICAL RADIUS & ACTIVATION BARRIER
const CriticalRadiusSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Математический вывод
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Критический радиус $r^*$ и высота барьера $\Delta G^*$
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-emerald-900/50 pb-2">
          1. Условие экстремума $d\Delta G / dr = 0$
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Дифференцируя свободную энергию Гиббса по радиусу зародыша:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-emerald-300">
          <MathView math="\frac{d\Delta G}{dr} = - 4\pi r^2 \Delta g_v + 8\pi r \sigma = 0" />
        </div>
        <p className="text-xs text-neutral-300">
          Получаем формулу **критического радиуса зародыша**:
        </p>
        <div className="bg-emerald-950/40 p-3 rounded-xl border border-emerald-800/80 text-center text-sm font-mono text-white">
          <MathView math="r^* = \frac{2\sigma}{\Delta g_v} = \frac{2\sigma T_m}{\Delta H_v \cdot \Delta T}" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-amber-400 border-b border-amber-900/50 pb-2">
          2. Высота активационного барьера $\Delta G(r^*)$
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Подставляя значение $r^*$ в исходное уравнение $\Delta G(r)$:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-amber-300">
          <MathView math="\Delta G^* = \frac{1}{3} \cdot 4\pi (r^*)^2 \sigma = \frac{16\pi \sigma^3}{3 (\Delta g_v)^2}" />
        </div>
        <p className="text-xs text-neutral-300">
          Через степень переохлаждения расплава $\Delta T$:
        </p>
        <div className="bg-amber-950/40 p-3 rounded-xl border border-amber-800/80 text-center text-sm font-mono text-white">
          <MathView math="\Delta G^* = \frac{16\pi \sigma^3 T_m^2}{3 (\Delta H_v)^2 (\Delta T)^2}" />
        </div>
      </div>
    </div>

    <div className="grid grid-cols-2 gap-3 text-xs">
      <div className="bg-neutral-950 p-3 rounded-xl border border-neutral-800 text-neutral-400">
        • <MathView math="r < r^*" />: <MathView math="\frac{d\Delta G}{dr} > 0" /> <span className="text-rose-400 font-semibold">(субкритический зародыш растворяется)</span>
      </div>
      <div className="bg-neutral-950 p-3 rounded-xl border border-neutral-800 text-neutral-400">
        • <MathView math="r > r^*" />: <MathView math="\frac{d\Delta G}{dr} < 0" /> <span className="text-emerald-400 font-semibold">(стабильный необратимый рост фазы)</span>
      </div>
    </div>
  </div>
);

// SLIDE 5: NUCLEATION SIMULATOR
const NucleationSimulatorSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-4">
    <NucleationWidget />
  </div>
);

// SLIDE 6: KINETICS & TAMMAN CURVES
const TammanKineticsSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-cyan-400 bg-cyan-950/60 border border-cyan-800/60 px-3 py-1 rounded">
        Кинетика кристаллизации
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Скорость нуклеации $I(T)$ и кривые Таммана
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-cyan-400 border-b border-cyan-900/50 pb-2">
          Двухфакторное уравнение скорости зародышеобразования
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Стационарная скорость нуклеации $I$ (число зародышей в 1 м³ за 1 с) определяется произведением <strong>термодинамической вероятности</strong> преодоления барьера $\Delta G^*$ и <strong>кинетической подвижности атомов</strong>:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-cyan-300">
          <MathView math="I(T) = I_0 \cdot \exp\left(-\frac{\Delta G^*(T)}{k_B T}\right) \cdot \exp\left(-\frac{E_a}{k_B T}\right)" />
        </div>
        <p className="text-xs text-neutral-400">
          где $E_a$ — энергия активации диффузионного скачка атома через границу фаз.
        </p>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-white border-b border-neutral-800 pb-2">
          Три температурных диапазона (Кривая Таммана)
        </h3>
        <ul className="text-xs text-neutral-300 space-y-2">
          <li className="p-2 bg-neutral-900/60 rounded-lg border border-neutral-800">
            <span className="font-bold text-amber-400 block">1. Малое переохлаждение ($T \approx T_m$):</span>
            <MathView math="\Delta G^* \to \infty \Longrightarrow I \approx 0" /> (зародыши не образуются).
          </li>
          <li className="p-2 bg-emerald-950/40 rounded-lg border border-emerald-800/40">
            <span className="font-bold text-emerald-400 block">2. Оптимум (максимум скорости <MathView math="I_{\max}" />):</span>
            Баланс между снижением барьера $\Delta G^*$ и сохранением диффузии. Формируются <strong>нанокристаллы</strong>.
          </li>
          <li className="p-2 bg-blue-950/40 rounded-lg border border-blue-800/40">
            <span className="font-bold text-blue-400 block">3. Сверхбыстрая закалка ($T \to 0$):</span>
            Диффузия «заморожена» (<MathView math="\exp(-E_a/kT) \to 0" />). Образуются <strong>металлические стекла и аморфные нанопленки</strong>.
          </li>
        </ul>
      </div>
    </div>
  </div>
);

// SLIDE 7: GIBBS-THOMSON MELTING POINT DEPRESSION
const GibbsThomsonSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-amber-400 bg-amber-950/60 border border-amber-800/60 px-3 py-1 rounded">
        Размерные фазовые переходы
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Размерное падение температуры плавления $T_m(r)$
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-amber-400 border-b border-amber-900/50 pb-2">
          Термодинамический вывод уравнения Гиббса–Томсона
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Условие равновесия нанокристалла с расплавом: $\mu_s(r, T) = \mu_l(T)$.
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-neutral-300">
          <MathView math="\mu_{s,\infty}(T) + \frac{2\sigma_{sl}\Omega}{r} = \mu_{l,\infty}(T)" />
        </div>
        <p className="text-xs text-neutral-300">
          Линеаризуя разность потенциалов <MathView math="\Delta \mu = \frac{\Delta H_{melt}}{T_{m,\infty}}(T_{m,\infty} - T)" />, получаем:
        </p>
        <div className="bg-amber-950/40 p-3 rounded-xl border border-amber-800/80 text-center text-sm font-mono text-amber-300">
          <MathView math="T_m(r) = T_{m,\infty} \left( 1 - \frac{2\sigma_{sl} \Omega}{\Delta H_{melt} \cdot r} \right) = T_{m,\infty} \left( 1 - \frac{C_{GT}}{r} \right)" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-teal-400 border-b border-teal-900/50 pb-2">
          Модель жидкой оболочки (*Liquid Skin Model*)
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Плавление начинается с поверхности: при $T &lt; T_m(r)$ образуется квазижидкий монослой толщиной <MathView math="d_0 \approx 1\text{--}2" /> атома.
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-center text-xs font-mono text-teal-300">
          <MathView math="T_m(r) = T_{m,\infty} \left( 1 - \frac{2\Omega}{\Delta H (r - d_0)} \left[ \sigma_{sl} + (\sigma_s - \sigma_l)\left(1 - \frac{d_0}{r}\right) \right] \right)" />
        </div>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs space-y-1 text-neutral-300">
          <p className="font-semibold text-white">Пример золота (Au, <MathView math="T_{m,\infty} = 1064^\circ\text{C}" />):</p>
          <p>• <MathView math="r = 10\text{ нм} \Longrightarrow T_m \approx 820^\circ\text{C}" /></p>
          <p>• <MathView math="r = 2\text{ нм} \Longrightarrow T_m \approx 300\text{--}350^\circ\text{C}" /> (жидкое при низком нагреве!)</p>
        </div>
      </div>
    </div>
  </div>
);

// SLIDE 8: NANO PHASE DIAGRAM & EUTECTIC
const PhaseDiagramSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-4">
    <PhaseDiagramWidget />
  </div>
);

// SLIDE 9: METASTABLE NANO-PHASES STABILIZATION
const MetastablePhasesSlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Полиморфизм наноматериалов
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Стабилизация метастабильных нанофаз: парадокс Al₂O₃ и ZrO₂
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-emerald-900/50 pb-2">
          Инверсия фазовой стабильности в Al₂O₃
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          В объеме корунд <MathView math="\alpha\text{-}\text{Al}_2\text{O}_3" /> термодинамически стабилен при всех $T$. Однако поверхностная энергия фаз существенно различается:
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs font-mono space-y-1">
          <p className="text-rose-400">• <MathView math="\sigma_\alpha(\text{корунд}) \approx 2.6\text{ Дж/м}^2" /></p>
          <p className="text-emerald-400">• <MathView math="\sigma_\gamma(\text{кубическая}) \approx 1.6\text{ Дж/м}^2" /></p>
        </div>
        <p className="text-xs text-neutral-300">
          При $r &lt; 13$ нм поверхностный выигрыш $\gamma$-фазы перевешивает объемный проигрыш $\Delta G_{vol}$:
        </p>
        <div className="bg-emerald-950/40 p-2.5 rounded-xl border border-emerald-800/60 text-center text-xs font-mono text-emerald-300">
          <MathView math="r_{\text{cross}} = \frac{3(\sigma_\alpha - \sigma_\gamma)}{\rho (\Delta g_{\alpha} - \Delta g_{\gamma})} \approx 13\text{ нм}" />
        </div>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-amber-400 border-b border-amber-900/50 pb-2">
          Беспримесная стабилизация тетрагонального ZrO₂
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          Диоксид циркония в макрообъеме при комнатной температуре находится в моноклинной фазе. Тетрагональная фаза требует нагрева свыше 1170 °C.
        </p>
        <div className="bg-amber-950/30 p-3 rounded-xl border border-amber-800/50 text-xs text-neutral-200 leading-relaxed">
          <strong>В нанокристаллах ($r &lt; 10$ нм):</strong> Высокотемпературная тетрагональная фаза стабильна при нормальных условиях <strong>без легирования оксидом иттрия</strong> Y₂O₃!
        </div>
        <div className="bg-neutral-900/80 p-2.5 rounded-xl border border-neutral-800 text-center text-xs font-mono text-amber-300">
          <MathView math="G_{\text{tetr}}(r) < G_{\text{monocl}}(r) \quad \text{при } r < r_{\text{crit}}" />
        </div>
      </div>
    </div>
  </div>
);

// SLIDE 10: SUMMARY & NEXT LECTURE PREVIEW
const SummarySlide = () => (
  <div className="h-full flex flex-col justify-between space-y-5">
    <div>
      <span className="text-xs font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-3 py-1 rounded">
        Итоги лекции
      </span>
      <h2 className="text-2xl sm:text-4xl font-['Newsreader'] font-bold text-white mt-2">
        Ключевые выводы и мостик к Лекции №3
      </h2>
    </div>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 flex-1">
      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-neutral-800 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-emerald-400 border-b border-neutral-800 pb-2">
          Резюме Лекции №2
        </h3>
        <ul className="text-xs text-neutral-300 space-y-2.5">
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Формализм Хилла:</strong> В малых системах <MathView math="dG" /> содержит поверхностный дифференциал <MathView math="\sigma dA" />, делающий химический потенциал размерно-зависимым <MathView math="\mu(r)" />.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Зародышеобразование:</strong> Критический радиус <MathView math="r^* = 2\sigma/\Delta g_v" /> обратно пропорционален переохлаждению <MathView math="\Delta T" />, а барьер <MathView math="\Delta G^* \propto 1/(\Delta T)^2" />.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span><strong>Размерное плавление:</strong> <MathView math="T_m(r) = T_{m,\infty}(1 - C_{GT}/r)" /> обеспечивает спекание нанопаст при температурах в разы ниже точки плавления слитка.</span>
          </li>
        </ul>
      </div>

      <div className="bg-neutral-950/80 p-5 rounded-2xl border border-amber-800/60 flex flex-col justify-between space-y-3">
        <h3 className="text-sm font-bold text-white border-b border-amber-900/50 pb-2 flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-amber-400" />
          Анонс Лекции №3 (30.09.2026)
        </h3>
        <p className="text-xs text-neutral-300 leading-relaxed">
          <strong>Тема: «Термодинамика дисперсных систем, коллоидные растворы и двойной электрический слой».</strong>
        </p>
        <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs space-y-1.5 text-neutral-300">
          <p>• Строение мицеллы и модели двойного электрического слоя (Гельмгольц, Гуи–Чепмен, Штерн).</p>
          <p>• Электрокинетический дзета-потенциал ($\zeta$) и методы его измерения.</p>
          <p>• Теория агрегативной устойчивости коллоидов ДЛФО и правило Шульце–Гарди.</p>
        </div>
      </div>
    </div>
  </div>
);

// BOARD PLAN & NOTES CONTENT FOR LECTURE 2
const Lecture2Notes = () => (
  <div className="space-y-6 text-xs sm:text-sm leading-relaxed">
    <div className="border-b border-neutral-800 pb-4">
      <span className="text-xs font-mono text-amber-400 font-bold uppercase tracking-wider">План работы у доски и академический конспект</span>
      <h2 className="text-xl font-bold font-['Newsreader'] text-white mt-1">Лекция №2: Особенности термодинамики наноструктур и нуклеация</h2>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-amber-400 border-b border-neutral-800 pb-1">ДОСКА 1: Теория нуклеации Гиббса–Фольмера</h3>
        <p className="text-neutral-300">• Конкуренция объемного выигрыша и поверхностного барьера:</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-amber-300">
          <MathView math="\Delta G(r) = - \frac{4}{3}\pi r^3 \Delta g_v + 4\pi r^2 \sigma" />
        </div>
        <p className="text-neutral-400 text-xs">Критический радиус: <MathView math="r^* = \frac{2\sigma}{\Delta g_v} = \frac{2\sigma T_m}{\Delta H_v \Delta T}" /></p>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-emerald-400 border-b border-neutral-800 pb-1">ДОСКА 2: Высота барьера $\Delta G^*$</h3>
        <p className="text-neutral-300">• Работа образования критического зародыша:</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-emerald-300">
          <MathView math="\Delta G^* = \frac{16\pi \sigma^3}{3 (\Delta g_v)^2} = \frac{16\pi \sigma^3 T_m^2}{3 (\Delta H_v)^2 (\Delta T)^2}" />
        </div>
        <p className="text-neutral-400 text-xs">При глубоком переохлаждении $\Delta G^* \to 0$, скорость нуклеации лимитируется диффузией $E_a$.</p>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-teal-400 border-b border-neutral-800 pb-1">ДОСКА 3: Уравнение Гиббса–Томсона</h3>
        <p className="text-neutral-300">• Размерная зависимость плавления твердой сферы:</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-teal-300">
          <MathView math="T_m(r) = T_{m,\infty} \left( 1 - \frac{2\sigma_{sl} \Omega}{\Delta H_{melt} r} \right)" />
        </div>
        <p className="text-neutral-400 text-xs">Характеристический параметр <MathView math="C_{GT} \approx 1.5\text{--}2.5\text{ нм}" />.</p>
      </div>

      <div className="bg-neutral-950/80 p-4 rounded-xl border border-neutral-800 space-y-2">
        <h3 className="font-bold text-cyan-400 border-b border-neutral-800 pb-1">ДОСКА 4: Правило фаз Гиббса для нанодисперсий</h3>
        <p className="text-neutral-300">• Включение кривизны как термодинамической переменной:</p>
        <div className="bg-neutral-900/80 p-2 rounded text-center font-mono text-cyan-300">
          <MathView math="f = k - \phi + 2 + \sum_{i=1}^{\phi} \xi_i" />
        </div>
        <p className="text-neutral-400 text-xs">Смещение эвтектических точек, стабилизация $\gamma$-фазы Al₂O₃ ($r &lt; 13$ нм) и тетрагонального ZrO₂ ($r &lt; 10$ нм).</p>
      </div>
    </div>
  </div>
);

// MAIN EXPORT
export const Lecture2: React.FC<{ onClose: () => void }> = ({ onClose }) => {
  const slides = [
    <CoverSlide key="1" />,
    <SmallSystemsSlide key="2" />,
    <NucleationTheorySlide key="3" />,
    <CriticalRadiusSlide key="4" />,
    <NucleationSimulatorSlide key="5" />,
    <TammanKineticsSlide key="6" />,
    <GibbsThomsonSlide key="7" />,
    <PhaseDiagramSlide key="8" />,
    <MetastablePhasesSlide key="9" />,
    <SummarySlide key="10" />
  ];

  return (
    <SlideViewer 
      slides={slides} 
      title="Физические основы нанотехнологий • Лекция №2: Термодинамика наноструктур" 
      onClose={onClose}
      notesContent={<Lecture2Notes />}
    />
  );
};

