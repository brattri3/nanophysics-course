import React, { useState, useMemo } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, ReferenceDot } from 'recharts';
import { MathView } from './MathView';

// WIDGET 1: GIBBS-THOMSON (MELTING POINT DEPRESSION)
export const GibbsThomsonWidget: React.FC = () => {
  const [radius, setRadius] = useState<number>(4);

  // Constants for Gold (Au)
  const Tmb = 1337; // Bulk melting temp (K)
  const C = 1.8; // Gibbs-Thomson slope parameter

  const calculateTm = (r: number) => {
    return Math.max(300, Tmb * (1 - C / r));
  };

  const chartData = useMemo(() => {
    const data = [];
    for (let r = 1.5; r <= 25; r += 0.5) {
      data.push({
        radius: r,
        temperature: calculateTm(r)
      });
    }
    return data;
  }, []);

  const currentTm = calculateTm(radius);

  return (
    <div className="flex flex-col lg:flex-row gap-6 w-full h-full items-stretch justify-between">
      {/* Left side: Controls and explanation */}
      <div className="flex-1 space-y-4 flex flex-col justify-between">
        <div>
          <span className="text-[11px] font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-2 py-0.5 rounded">
            Интерактивный симулятор
          </span>
          <h3 className="text-lg sm:text-2xl font-bold font-['Newsreader'] text-white mt-2 leading-snug">
            Размерное падение температуры плавления
          </h3>
          <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed mt-2">
            В наночастицах доля поверхностных атомов со свободной энергией достигает десятков процентов. 
            По уравнению <strong>Гиббса–Томсона</strong> кристаллическая решетка теряет устойчивость при температурах намного ниже температуры плавления массивного слитка.
          </p>
          
          <div className="mt-3 bg-neutral-950/70 border border-neutral-800 p-3 rounded-xl text-xs sm:text-sm text-emerald-300 text-center">
            <MathView math="T_m(r) = T_{\text{bulk}} \cdot \left(1 - \frac{2\sigma_{sl} \Omega}{\Delta H_{\text{melt}} r}\right)" />
          </div>
        </div>

        {/* Interactive Controls Card */}
        <div className="bg-neutral-950/60 border border-neutral-800 rounded-xl p-4 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs font-semibold text-neutral-400">Радиус наночастицы Au (r):</span>
            <span className="text-lg font-bold text-white font-mono">{radius.toFixed(1)} <span className="text-xs text-neutral-400">нм</span></span>
          </div>
          
          <input 
            type="range" 
            min="1.5" 
            max="25" 
            step="0.5" 
            value={radius} 
            onChange={(e) => setRadius(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 h-2 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
          />

          <div className="flex justify-between items-center pt-2 border-t border-neutral-800 text-xs">
            <span className="text-neutral-400">Температура плавления:</span>
            <span className="text-base sm:text-lg font-bold text-emerald-400 font-mono">
              {Math.round(currentTm)} K <span className="text-xs text-neutral-400 font-normal">({Math.round(currentTm - 273.15)} °C)</span>
            </span>
          </div>
        </div>
      </div>

      {/* Right side: Chart */}
      <div className="flex-1 min-h-[220px] sm:min-h-[260px] lg:h-full w-full bg-neutral-950/60 rounded-xl border border-neutral-800 p-2 sm:p-4 flex flex-col">
        <div className="text-[11px] text-neutral-400 font-medium mb-1 px-2 flex justify-between items-center">
          <span>Кривая плавления нанозолота T_m(r)</span>
          <span className="text-emerald-400 font-mono">Слиток: 1337 K (1064 °C)</span>
        </div>
        
        <div className="flex-1 w-full min-h-[180px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 10, bottom: 10, left: -10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
              <XAxis 
                dataKey="radius" 
                stroke="#525252" 
                tick={{fill: '#a3a3a3', fontSize: 11}}
                unit=" нм"
              />
              <YAxis 
                domain={[300, 1400]} 
                stroke="#525252" 
                tick={{fill: '#a3a3a3', fontSize: 11}}
                unit=" K"
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#171717', borderColor: '#404040', color: '#fff', borderRadius: '8px', fontSize: '12px' }}
                itemStyle={{ color: '#34d399' }}
                formatter={(value: number) => [`${Math.round(value)} K (${Math.round(value - 273.15)} °C)`, 'T плавления']}
                labelFormatter={(label: any) => `Радиус r: ${label} нм`}
              />
              <ReferenceLine y={1337} stroke="#525252" strokeDasharray="3 3" />
              <Line 
                type="monotone" 
                dataKey="temperature" 
                stroke="#10b981" 
                strokeWidth={2.5}
                dot={false}
                animationDuration={200}
              />
              <ReferenceDot x={radius} y={currentTm} r={5} fill="#ffffff" stroke="#10b981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

// WIDGET 2: DENSITY OF STATES (3D -> 2D -> 1D -> 0D)
export const DensityOfStatesWidget: React.FC = () => {
  const [dim, setDim] = useState<'3D' | '2D' | '1D' | '0D'>('2D');

  const chartData = useMemo(() => {
    const data = [];
    const stepLevels = [1, 2.5, 4.5, 7];

    for (let e = 0.1; e <= 8.5; e += 0.1) {
      let g = 0;
      if (dim === '3D') {
        g = Math.sqrt(e) * 1.5;
      } else if (dim === '2D') {
        // Step function
        g = stepLevels.filter(lvl => e >= lvl).length * 1.2;
      } else if (dim === '1D') {
        // 1/sqrt(E - En) singularities
        g = stepLevels.reduce((acc, lvl) => {
          if (e >= lvl) {
            const diff = e - lvl;
            return acc + Math.min(4, 0.7 / Math.sqrt(Math.max(0.04, diff)));
          }
          return acc;
        }, 0);
      } else if (dim === '0D') {
        // Delta peaks
        const nearPeak = stepLevels.some(lvl => Math.abs(e - lvl) < 0.15);
        g = nearPeak ? 4.5 : 0;
      }

      data.push({
        energy: parseFloat(e.toFixed(1)),
        dos: parseFloat(g.toFixed(2))
      });
    }
    return data;
  }, [dim]);

  const formulas: Record<string, string> = {
    '3D': 'g_{3D}(E) = \\frac{1}{2\\pi^2} \\left(\\frac{2m^*}{\\hbar^2}\\right)^{3/2} \\sqrt{E}',
    '2D': 'g_{2D}(E) = \\frac{m^*}{\\pi\\hbar^2} \\sum_{n} \\Theta(E - E_n)',
    '1D': 'g_{1D}(E) = \\frac{\\sqrt{2m^*}}{\\pi\\hbar} \\sum_{n} \\frac{1}{\\sqrt{E - E_n}}',
    '0D': 'g_{0D}(E) = 2 \\sum_{n} \\delta(E - E_n)'
  };

  const descriptions: Record<string, string> = {
    '3D': 'Объемный материал: квазинепрерывный параболический спектр плотности состояний.',
    '2D': 'Квантовая яма (2DEG, графен): ступенчатый спектр; каждая ступень соответствует новому уровню размерного квантования.',
    '1D': 'Квантовая нить (УНТ, нанопроволока): сингулярности Ван Хова с резким ростом g(E) на порогах подзон.',
    '0D': 'Квантовая точка (нанокластер): полностью дискретный атомоподобный спектр (дельта-пики).'
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 w-full h-full items-stretch justify-between">
      {/* Left side: Controls and explanation */}
      <div className="flex-1 space-y-4 flex flex-col justify-between">
        <div>
          <span className="text-[11px] font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-2 py-0.5 rounded">
            Квантовое ограничение
          </span>
          <h3 className="text-lg sm:text-2xl font-bold font-['Newsreader'] text-white mt-2 leading-snug">
            Плотность электронных состояний g(E)
          </h3>
          <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed mt-2">
            {descriptions[dim]}
          </p>
          
          <div className="mt-3 bg-neutral-950/70 border border-neutral-800 p-3 rounded-xl text-xs sm:text-sm text-emerald-300 text-center">
            <MathView math={formulas[dim]} />
          </div>
        </div>

        {/* Dimension Selector */}
        <div className="bg-neutral-950/60 border border-neutral-800 rounded-xl p-4 space-y-3">
          <span className="text-xs font-semibold text-neutral-400 block mb-2">Выберите размерность системы:</span>
          <div className="grid grid-cols-4 gap-2">
            {(['3D', '2D', '1D', '0D'] as const).map((d) => (
              <button
                key={d}
                onClick={() => setDim(d)}
                className={`py-2 px-3 rounded-lg text-xs font-bold font-mono transition-all ${
                  dim === d 
                    ? 'bg-emerald-500 text-neutral-950 shadow-[0_0_15px_rgba(16,185,129,0.4)]' 
                    : 'bg-neutral-900 text-neutral-400 hover:bg-neutral-800 hover:text-white border border-neutral-800'
                }`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Right side: Chart */}
      <div className="flex-1 min-h-[220px] sm:min-h-[260px] lg:h-full w-full bg-neutral-950/60 rounded-xl border border-neutral-800 p-2 sm:p-4 flex flex-col">
        <div className="text-[11px] text-neutral-400 font-medium mb-1 px-2 flex justify-between items-center">
          <span>Спектр плотности состояний g(E) [{dim}]</span>
          <span className="text-emerald-400 font-mono">Размерность: {dim}</span>
        </div>
        
        <div className="flex-1 w-full min-h-[180px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 10, bottom: 10, left: -10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
              <XAxis 
                dataKey="energy" 
                stroke="#525252" 
                tick={{fill: '#a3a3a3', fontSize: 11}}
                unit=" эВ"
              />
              <YAxis 
                domain={[0, 5]} 
                stroke="#525252" 
                tick={{fill: '#a3a3a3', fontSize: 11}}
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#171717', borderColor: '#404040', color: '#fff', borderRadius: '8px', fontSize: '12px' }}
                itemStyle={{ color: '#34d399' }}
                formatter={(value: number) => [`${value} отн. ед.`, 'g(E)']}
                labelFormatter={(label: any) => `Энергия: ${label} эВ`}
              />
              <Line 
                type={dim === '2D' ? 'stepAfter' : 'monotone'} 
                dataKey="dos" 
                stroke="#10b981" 
                strokeWidth={2.5}
                dot={false}
                animationDuration={250}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

// MATERIAL PRESETS FOR NUCLEATION
interface MaterialNucleationPreset {
  name: string;
  symbol: string;
  Tm: number; // K
  sigma: number; // J/m^2
  dH: number; // J/m^3 (Volumetric latent heat of fusion)
  atomVol: number; // m^3
  defaultDeltaT: number;
}

const MATERIAL_PRESETS: Record<string, MaterialNucleationPreset> = {
  Au: {
    name: 'Золото',
    symbol: 'Au',
    Tm: 1337,
    sigma: 0.27,
    dH: 1.27e9,
    atomVol: 1.7e-29,
    defaultDeltaT: 50,
  },
  Ag: {
    name: 'Серебро',
    symbol: 'Ag',
    Tm: 1235,
    sigma: 0.17,
    dH: 1.09e9,
    atomVol: 1.7e-29,
    defaultDeltaT: 40,
  },
  Si: {
    name: 'Кремний',
    symbol: 'Si',
    Tm: 1687,
    sigma: 0.35,
    dH: 4.15e9,
    atomVol: 2.0e-29,
    defaultDeltaT: 70,
  },
  H2O: {
    name: 'Вода / Лед',
    symbol: 'H2O',
    Tm: 273.15,
    sigma: 0.03,
    dH: 3.34e8,
    atomVol: 3.25e-29,
    defaultDeltaT: 15,
  },
};

// WIDGET 3: NUCLEATION SIMULATOR (GIBBS-VOLMER THEORY)
export const NucleationWidget: React.FC = () => {
  const [materialKey, setMaterialKey] = useState<string>('Au');
  const [deltaT, setDeltaT] = useState<number>(50); // Supercooling (K)
  const [sigmaFactor, setSigmaFactor] = useState<number>(1.0); // Surface tension scale

  const mat = MATERIAL_PRESETS[materialKey] || MATERIAL_PRESETS.Au;
  const currentSigma = mat.sigma * sigmaFactor;

  // Volumetric driving force: Delta g_v = (Delta H_v * Delta T) / T_m (J/m^3)
  const deltaGv = (mat.dH * deltaT) / mat.Tm;

  // Critical radius: r* = 2 * sigma / delta_g_v (meters -> nm)
  const rStarMeters = (2 * currentSigma) / deltaGv;
  const rStarNm = rStarMeters * 1e9;

  // Barrier height: Delta G* = (16 * pi * sigma^3) / (3 * delta_g_v^2) (Joules -> eV)
  const deltaGStarJoules = (16 * Math.PI * Math.pow(currentSigma, 3)) / (3 * Math.pow(deltaGv, 2));
  const deltaGStarEv = deltaGStarJoules / 1.602e-19;

  // Number of atoms in critical nucleus: N* = (4/3 * pi * r*^3) / Omega
  const nAtoms = Math.round(((4 / 3) * Math.PI * Math.pow(rStarMeters, 3)) / mat.atomVol);

  // Generate chart data up to 2.5 * r*
  const maxR = Math.max(2.5, rStarNm * 2.2);
  const stepR = maxR / 50;

  const chartData = useMemo(() => {
    const data = [];
    for (let rNm = 0.05; rNm <= maxR; rNm += stepR) {
      const rM = rNm * 1e-9;
      // Delta G_vol = - (4/3) * pi * r^3 * deltaGv
      const gVolJ = - (4 / 3) * Math.PI * Math.pow(rM, 3) * deltaGv;
      // Delta G_surf = 4 * pi * r^2 * sigma
      const gSurfJ = 4 * Math.PI * Math.pow(rM, 2) * currentSigma;
      // Total Delta G
      const gTotalJ = gVolJ + gSurfJ;

      data.push({
        radius: parseFloat(rNm.toFixed(2)),
        deltaGTotal: parseFloat((gTotalJ / 1.602e-19).toFixed(1)),
        deltaGSurf: parseFloat((gSurfJ / 1.602e-19).toFixed(1)),
        deltaGVol: parseFloat((gVolJ / 1.602e-19).toFixed(1)),
      });
    }
    return data;
  }, [deltaGv, currentSigma, maxR, stepR]);

  return (
    <div className="flex flex-col lg:flex-row gap-6 w-full h-full items-stretch justify-between">
      {/* Left Column: Controls & Metrics */}
      <div className="flex-1 space-y-4 flex flex-col justify-between">
        <div>
          <span className="text-[11px] font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-2 py-0.5 rounded">
            Интерактивный симулятор нуклеации
          </span>
          <h3 className="text-lg sm:text-2xl font-bold font-['Newsreader'] text-white mt-2 leading-snug">
            Критический зародыш и термодинамический барьер $\Delta G(r)$
          </h3>
          <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed mt-1">
            Конкуренция объемного выигрыша энергии ($\Delta G_{vol} \propto -r^3$) и поверхностного барьера ($\Delta G_{surf} \propto r^2$).
          </p>

          <div className="mt-2.5 bg-neutral-950/70 border border-neutral-800 p-2.5 rounded-xl text-xs sm:text-sm text-emerald-300 text-center">
            <MathView math="\Delta G(r) = - \frac{4}{3}\pi r^3 \frac{\Delta H_v \Delta T}{T_m} + 4\pi r^2 \sigma" />
          </div>
        </div>

        {/* Controls Card */}
        <div className="bg-neutral-950/60 border border-neutral-800 rounded-xl p-3.5 space-y-3">
          {/* Material Presets */}
          <div>
            <span className="text-[11px] font-semibold text-neutral-400 block mb-1.5">Материал фазы:</span>
            <div className="grid grid-cols-4 gap-1.5">
              {Object.entries(MATERIAL_PRESETS).map(([k, v]) => (
                <button
                  key={k}
                  onClick={() => {
                    setMaterialKey(k);
                    setDeltaT(v.defaultDeltaT);
                    setSigmaFactor(1.0);
                  }}
                  className={`py-1.5 px-2 rounded-lg text-xs font-bold font-mono transition-all ${
                    materialKey === k
                      ? 'bg-emerald-500 text-neutral-950 shadow-[0_0_15px_rgba(16,185,129,0.4)]'
                      : 'bg-neutral-900 text-neutral-400 hover:bg-neutral-800 hover:text-white border border-neutral-800'
                  }`}
                >
                  {v.symbol} ({v.name.split(' ')[0]})
                </button>
              ))}
            </div>
          </div>

          {/* Supercooling Slider */}
          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs">
              <span className="text-neutral-400">Переохлаждение расплава ($\Delta T$):</span>
              <span className="font-bold text-white font-mono">{deltaT} K <span className="text-neutral-500 text-[11px]">({((deltaT / mat.Tm) * 100).toFixed(1)}% от $T_m$)</span></span>
            </div>
            <input
              type="range"
              min={Math.max(5, Math.round(mat.Tm * 0.01))}
              max={Math.round(mat.Tm * 0.25)}
              step={1}
              value={deltaT}
              onChange={(e) => setDeltaT(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 h-1.5 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          {/* Surface Tension Scale */}
          <div className="space-y-1">
            <div className="flex justify-between items-center text-xs">
              <span className="text-neutral-400">Поверхностная энергия ($\sigma$):</span>
              <span className="font-bold text-teal-400 font-mono">{(currentSigma).toFixed(3)} Дж/м²</span>
            </div>
            <input
              type="range"
              min={0.5}
              max={1.8}
              step={0.05}
              value={sigmaFactor}
              onChange={(e) => setSigmaFactor(parseFloat(e.target.value))}
              className="w-full accent-teal-500 h-1.5 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          {/* Calculated KPIs */}
          <div className="grid grid-cols-3 gap-2 pt-2 border-t border-neutral-800/80 text-center">
            <div className="bg-neutral-900/80 p-2 rounded-lg border border-neutral-800">
              <span className="text-[10px] text-neutral-400 block">Критич. радиус $r^*$</span>
              <span className="text-sm sm:text-base font-bold text-emerald-400 font-mono">
                {rStarNm.toFixed(2)} <span className="text-[10px] text-neutral-400 font-normal">нм</span>
              </span>
            </div>
            <div className="bg-neutral-900/80 p-2 rounded-lg border border-neutral-800">
              <span className="text-[10px] text-neutral-400 block">Барьер $\Delta G^*$</span>
              <span className="text-sm sm:text-base font-bold text-amber-400 font-mono">
                {deltaGStarEv > 1000 ? (deltaGStarEv / 1000).toFixed(1) + ' кэВ' : deltaGStarEv.toFixed(1) + ' эВ'}
              </span>
            </div>
            <div className="bg-neutral-900/80 p-2 rounded-lg border border-neutral-800">
              <span className="text-[10px] text-neutral-400 block">Атомов в $r^*$ ($N^*$)</span>
              <span className="text-sm sm:text-base font-bold text-teal-300 font-mono">
                {nAtoms > 1e6 ? (nAtoms / 1e6).toFixed(1) + 'M' : nAtoms.toLocaleString('ru-RU')}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Column: Interactive Recharts Graph */}
      <div className="flex-1 min-h-[240px] sm:min-h-[280px] lg:h-full w-full bg-neutral-950/60 rounded-xl border border-neutral-800 p-2 sm:p-4 flex flex-col justify-between">
        <div className="text-[11px] text-neutral-400 font-medium mb-1 px-2 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-emerald-400 inline-block"></span> $\Delta G(r)$</span>
            <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-teal-400 inline-block border-b border-dashed"></span> $\Delta G_{surf}$</span>
            <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-rose-400 inline-block border-b border-dashed"></span> $\Delta G_{vol}$</span>
          </div>
          <span className="text-emerald-400 font-mono text-[11px]">$r^* = {rStarNm.toFixed(2)}$ нм</span>
        </div>

        <div className="flex-1 w-full min-h-[200px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 10, right: 10, bottom: 10, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
              <XAxis
                dataKey="radius"
                stroke="#525252"
                tick={{ fill: '#a3a3a3', fontSize: 11 }}
                unit=" нм"
              />
              <YAxis
                stroke="#525252"
                tick={{ fill: '#a3a3a3', fontSize: 11 }}
                unit=" эВ"
              />
              <Tooltip
                contentStyle={{ backgroundColor: '#171717', borderColor: '#404040', color: '#fff', borderRadius: '8px', fontSize: '12px' }}
                itemStyle={{ color: '#34d399' }}
                formatter={(value: number, name: string) => {
                  if (name === 'deltaGTotal') return [`${value} эВ`, 'Полная энергия ΔG(r)'];
                  if (name === 'deltaGSurf') return [`+${value} эВ`, 'Поверхностная ΔG_surf'];
                  if (name === 'deltaGVol') return [`${value} эВ`, 'Объемная ΔG_vol'];
                  return [value, name];
                }}
                labelFormatter={(label: any) => `Радиус зародыша r: ${label} нм`}
              />
              <ReferenceLine y={0} stroke="#737373" strokeDasharray="2 2" />
              <ReferenceLine x={parseFloat(rStarNm.toFixed(2))} stroke="#10b981" strokeDasharray="3 3" />
              <Line
                type="monotone"
                dataKey="deltaGSurf"
                stroke="#2dd4bf"
                strokeDasharray="4 4"
                strokeWidth={1.5}
                dot={false}
                name="deltaGSurf"
              />
              <Line
                type="monotone"
                dataKey="deltaGVol"
                stroke="#f43f5e"
                strokeDasharray="4 4"
                strokeWidth={1.5}
                dot={false}
                name="deltaGVol"
              />
              <Line
                type="monotone"
                dataKey="deltaGTotal"
                stroke="#10b981"
                strokeWidth={3}
                dot={false}
                animationDuration={250}
                name="deltaGTotal"
              />
              <ReferenceDot
                x={parseFloat(rStarNm.toFixed(2))}
                y={parseFloat(deltaGStarEv.toFixed(1))}
                r={6}
                fill="#ffffff"
                stroke="#10b981"
                strokeWidth={2.5}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-2 text-[11px] text-neutral-400 bg-neutral-900/60 p-2 rounded-lg border border-neutral-800 flex justify-between">
          <span>При $r &lt; r^*$: кластер растворяется (<MathView math="\frac{d\Delta G}{dr} > 0" />)</span>
          <span className="text-emerald-400 font-semibold">При $r &gt; r^*$: необратимый рост (<MathView math="\frac{d\Delta G}{dr} < 0" />)</span>
        </div>
      </div>
    </div>
  );
};

// WIDGET 4: NANO PHASE DIAGRAM & SIZE-DEPENDENT EUTECTIC
export const PhaseDiagramWidget: React.FC = () => {
  const [particleRadius, setParticleRadius] = useState<number>(3);

  // Eutectic system Au-Si (Bulk eutectic at 363 °C, 19 at.% Si)
  const bulkTe = 363; // °C
  const bulkCe = 19; // at. % Si
  const bulkTmAu = 1064; // °C
  const bulkTmSi = 1414; // °C

  // Size dependent depressions
  const deltaTe = (120 / particleRadius);
  const nanoTe = Math.max(120, Math.round(bulkTe - deltaTe));
  const nanoTmAu = Math.max(300, Math.round(bulkTmAu - 350 / particleRadius));
  const nanoTmSi = Math.max(400, Math.round(bulkTmSi - 400 / particleRadius));

  return (
    <div className="flex flex-col lg:flex-row gap-6 w-full h-full items-stretch justify-between">
      <div className="flex-1 space-y-4 flex flex-col justify-between">
        <div>
          <span className="text-[11px] font-bold tracking-wider uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-800/60 px-2 py-0.5 rounded">
            Термодинамика нанофаз
          </span>
          <h3 className="text-lg sm:text-2xl font-bold font-['Newsreader'] text-white mt-2 leading-snug">
            Размерная модификация фазовых диаграмм (Au–Si)
          </h3>
          <p className="text-xs sm:text-sm text-neutral-300 leading-relaxed mt-2">
            В нанодисперсиях правило фаз Гиббса включает кривизну поверхности как термодинамическую переменную ($f = k - \phi + 2 + \sum \xi_i$).
            Это приводит к глубокому снижению эвтектической температуры $T_E(r)$ и сдвигу линий ликвидуса.
          </p>

          <div className="mt-3 bg-neutral-950/70 border border-neutral-800 p-3 rounded-xl text-xs sm:text-sm text-emerald-300 text-center">
            <MathView math="T_E(r) = T_{E,\infty} \cdot \left(1 - \frac{\alpha_{eff}}{r}\right), \quad f = k - \phi + 3" />
          </div>
        </div>

        {/* Interactive Size Slider */}
        <div className="bg-neutral-950/60 border border-neutral-800 rounded-xl p-4 space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-xs font-semibold text-neutral-400">Размер нанозерен системы (r):</span>
            <span className="text-lg font-bold text-white font-mono">{particleRadius.toFixed(1)} <span className="text-xs text-neutral-400">нм</span></span>
          </div>

          <input
            type="range"
            min="1.5"
            max="20"
            step="0.5"
            value={particleRadius}
            onChange={(e) => setParticleRadius(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 h-2 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
          />

          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-neutral-800 text-xs">
            <div className="bg-neutral-900/80 p-2 rounded-lg border border-neutral-800">
              <span className="text-neutral-400 block text-[10px]">Эвтектика $T_E(r)$:</span>
              <span className="text-sm font-bold text-emerald-400 font-mono">{nanoTe} °C</span>
              <span className="text-neutral-500 text-[10px] block">Слиток: {bulkTe} °C (сдвиг -{Math.round(deltaTe)} °C)</span>
            </div>
            <div className="bg-neutral-900/80 p-2 rounded-lg border border-neutral-800">
              <span className="text-neutral-400 block text-[10px]">$T_m$ нанозолота:</span>
              <span className="text-sm font-bold text-amber-400 font-mono">{nanoTmAu} °C</span>
              <span className="text-neutral-500 text-[10px] block">Слиток: {bulkTmAu} °C</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Column: Comparative Visual Card */}
      <div className="flex-1 bg-neutral-950/60 rounded-xl border border-neutral-800 p-4 flex flex-col justify-between space-y-3">
        <h4 className="text-xs font-bold text-white uppercase tracking-wider text-neutral-400 border-b border-neutral-800 pb-2">
          Эффекты нанотермодинамики в материаловедении
        </h4>

        <div className="space-y-2.5 text-xs text-neutral-300">
          <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800">
            <span className="font-bold text-emerald-400 block mb-1">1. Каталитический рост нанопроволок (VLS-механизм):</span>
            Снижение эвтектики Au–Si до ~{nanoTe} °C позволяет выращивать кремниевые нановискеры при низких температурах из жидкой капли нанозолота.
          </div>

          <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800">
            <span className="font-bold text-teal-400 block mb-1">2. Стабилизация метастабильных нанофаз:</span>
            При $r &lt; 13$ нм фаза $\gamma$-Al₂O₃ становится стабильнее корунда $\alpha$-Al₂O₃ из-за низкой удельной поверхностной энергии (<MathView math="\sigma_\gamma = 1.6" /> против <MathView math="\sigma_\alpha = 2.6\text{ Дж/м}^2" />).
          </div>

          <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800">
            <span className="font-bold text-amber-400 block mb-1">3. Низкотемпературное наноспекание:</span>
            Высокая подвижность поверхностных атомов обеспечивает диффузионное спекание нанопорошков металлов при температурах <MathView math="(0.2\text{--}0.4)\,T_{m,\text{bulk}}" />.
          </div>
        </div>
      </div>
    </div>
  );
};

// WIDGET 5: DLVO THEORY INTERACTIVE SIMULATOR
export const DLFOWidget: React.FC = () => {
  const [valency, setValency] = useState<number>(1); // z = 1 (NaCl), 2 (Na2SO4), 3 (K3Fe(CN)6)
  const [concentration, setConcentration] = useState<number>(10); // mM (0.5 to 100 mM)
  const [surfacePotential, setSurfacePotential] = useState<number>(40); // mV
  const [hamakerExponent, setHamakerExponent] = useState<number>(1.2); // x 10^-19 J

  const particleRadius = 15; // nm

  // Physical constants
  const eps0 = 8.854e-12;
  const epsR = 78.5; // Water at 298 K
  const kB = 1.38e-23;
  const T = 298; // K
  const kBT = kB * T; // J (~4.11e-21 J)
  const elemQ = 1.602e-19;
  const NA = 6.022e23;

  // Ionic strength and Debye parameter
  // I = 0.5 * (c * z^2 + c * z) for symmetric 1:1, or consider z-counterion
  // kappa = sqrt(2 * z^2 * e^2 * c * NA / (eps * eps0 * kB * T))
  const concMolM3 = concentration; // mM = mol/m^3
  const kappaSq = (2 * Math.pow(valency, 2) * Math.pow(elemQ, 2) * concMolM3 * NA) / (epsR * eps0 * kBT);
  const kappaM = Math.sqrt(kappaSq); // 1/m
  const kappaNm = kappaM * 1e-9; // 1/nm
  const debyeLength = 1 / kappaNm; // nm

  const hamakerJ = hamakerExponent * 1e-19;
  const psi0Volts = surfacePotential * 1e-3;
  const radiusM = particleRadius * 1e-9;

  // Generate DLVO curve points
  const pointsCount = 70;
  const maxH = Math.min(10, Math.max(4, debyeLength * 3.5));
  const minH = 0.2; // nm
  const data: Array<{ h: number; uTotal: number; uVdw: number; uEl: number }> = [];

  let maxBarrierKbT = -Infinity;
  let maxBarrierH = 0;

  for (let i = 0; i <= pointsCount; i++) {
    const hNm = minH + (i / pointsCount) * (maxH - minH);
    const hM = hNm * 1e-9;

    // Van der Waals: U_vdW = - (A_H * R) / (12 * h)
    const uVdwJ = - (hamakerJ * radiusM) / (12 * hM);
    const uVdwKbT = uVdwJ / kBT;

    // Electrostatic: U_el = 2 * pi * eps * eps0 * R * psi0^2 * ln(1 + exp(-kappa * h))
    const expTerm = Math.exp(- kappaM * hM);
    const uElJ = 2 * Math.PI * epsR * eps0 * radiusM * Math.pow(psi0Volts, 2) * Math.log(1 + expTerm);
    const uElKbT = uElJ / kBT;

    const uTotalKbT = uVdwKbT + uElKbT;

    if (hNm > 0.4 && uTotalKbT > maxBarrierKbT) {
      maxBarrierKbT = uTotalKbT;
      maxBarrierH = hNm;
    }

    // Clamp for display
    data.push({
      h: parseFloat(hNm.toFixed(2)),
      uTotal: parseFloat(Math.max(-30, Math.min(40, uTotalKbT)).toFixed(2)),
      uVdw: parseFloat(Math.max(-30, Math.min(5, uVdwKbT)).toFixed(2)),
      uEl: parseFloat(Math.max(0, Math.min(40, uElKbT)).toFixed(2))
    });
  }

  const isStable = maxBarrierKbT > 15;
  const isThreshold = maxBarrierKbT >= 0 && maxBarrierKbT <= 15;
  const isFastCoagulation = maxBarrierKbT < 0;

  return (
    <div className="bg-neutral-900/90 border border-neutral-800 rounded-2xl p-4 sm:p-5 flex flex-col space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-neutral-800 pb-3">
        <div>
          <span className="text-xs font-mono text-emerald-400 uppercase tracking-widest font-bold">
            Интерактивная физическая симуляция • Теория ДЛФО
          </span>
          <h3 className="text-lg font-bold text-white font-['Newsreader']">
            Потенциальная кривая взаимодействия наночастиц: <MathView math="U_{\text{total}}(h) = U_{vdW}(h) + U_{el}(h)" />
          </h3>
        </div>
        <div className="flex items-center gap-2">
          {isStable && (
            <span className="text-xs px-3 py-1 bg-emerald-950/80 border border-emerald-700 text-emerald-300 rounded-full font-semibold">
              🟢 Агрегативно устойчив (<MathView math="U_{\max} > 15\ k_B T" />)
            </span>
          )}
          {isThreshold && (
            <span className="text-xs px-3 py-1 bg-amber-950/80 border border-amber-700 text-amber-300 rounded-full font-semibold">
              🟡 Медленная коагуляция (<MathView math="0 \le U_{\max} \le 15\ k_B T" />)
            </span>
          )}
          {isFastCoagulation && (
            <span className="text-xs px-3 py-1 bg-rose-950/80 border border-rose-700 text-rose-300 rounded-full font-semibold">
              🔴 Быстрая коагуляция (Барьер снят)
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-center">
        {/* Graph */}
        <div className="lg:col-span-7 bg-neutral-950/80 p-3 rounded-xl border border-neutral-800 flex flex-col">
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
                <XAxis 
                  dataKey="h" 
                  stroke="#737373" 
                  fontSize={10} 
                  label={{ value: 'Расстояние между поверхностями h (нм)', position: 'insideBottom', offset: -10, fill: '#a3a3a3', fontSize: 10 }} 
                />
                <YAxis 
                  stroke="#737373" 
                  fontSize={10} 
                  domain={[-25, 35]} 
                  label={{ value: 'Энергия U (k_B T)', angle: -90, position: 'insideLeft', fill: '#a3a3a3', fontSize: 10 }} 
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#171717', borderColor: '#404040', borderRadius: '0.75rem', fontSize: '11px' }} 
                  formatter={(val: number, name: string) => [
                    `${val} k_B T`,
                    name === 'uTotal' ? 'U_total (Сумма)' : name === 'uEl' ? 'U_el (Отталкивание ДЭС)' : 'U_vdW (Притяжение)'
                  ]}
                />
                <ReferenceLine y={0} stroke="#525252" strokeDasharray="2 2" />
                {maxBarrierKbT > 0 && (
                  <ReferenceLine x={parseFloat(maxBarrierH.toFixed(2))} stroke="#10b981" strokeDasharray="3 3" label={{ value: `U_max=${maxBarrierKbT.toFixed(1)} kT`, fill: '#10b981', fontSize: 10 }} />
                )}
                <Line type="monotone" dataKey="uEl" stroke="#38bdf8" strokeWidth={1.5} dot={false} strokeDasharray="4 4" />
                <Line type="monotone" dataKey="uVdw" stroke="#f43f5e" strokeWidth={1.5} dot={false} strokeDasharray="4 4" />
                <Line type="monotone" dataKey="uTotal" stroke="#10b981" strokeWidth={2.5} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="flex justify-between items-center text-[10px] text-neutral-400 mt-2 px-1">
            <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-emerald-500 inline-block" /> Суммарный потенциал <MathView math="U_{\text{total}}" /></span>
            <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-sky-400 inline-block" /> Электростатика <MathView math="U_{el}" /></span>
            <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-rose-500 inline-block" /> Ван-дер-Ваальс <MathView math="U_{vdW}" /></span>
          </div>
        </div>

        {/* Controls */}
        <div className="lg:col-span-5 bg-neutral-950/60 p-4 rounded-xl border border-neutral-800 space-y-3">
          {/* Valency selector */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-neutral-300 font-semibold">Заряд противоиона (Правило Шульце–Гарди):</span>
              <span className="text-emerald-400 font-mono font-bold">z = {valency}+</span>
            </div>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => setValency(1)}
                className={`py-1.5 px-2 rounded-lg text-xs font-mono font-bold transition-all ${valency === 1 ? 'bg-emerald-600 text-white shadow' : 'bg-neutral-800 text-neutral-300 hover:bg-neutral-700'}`}
              >
                z = 1 (NaCl)
              </button>
              <button
                onClick={() => setValency(2)}
                className={`py-1.5 px-2 rounded-lg text-xs font-mono font-bold transition-all ${valency === 2 ? 'bg-amber-600 text-white shadow' : 'bg-neutral-800 text-neutral-300 hover:bg-neutral-700'}`}
              >
                z = 2 (Na₂SO₄)
              </button>
              <button
                onClick={() => setValency(3)}
                className={`py-1.5 px-2 rounded-lg text-xs font-mono font-bold transition-all ${valency === 3 ? 'bg-rose-600 text-white shadow' : 'bg-neutral-800 text-neutral-300 hover:bg-neutral-700'}`}
              >
                z = 3 (K₃[Fe(CN)₆])
              </button>
            </div>
          </div>

          {/* Electrolyte Concentration */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-neutral-300">Концентрация электролита C:</span>
              <span className="text-white font-mono font-bold">{concentration.toFixed(1)} ммоль/л</span>
            </div>
            <input
              type="range"
              min="0.5"
              max="100"
              step="0.5"
              value={concentration}
              onChange={(e) => setConcentration(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 h-1.5 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          {/* Surface Potential */}
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-neutral-300">Потенциал поверхности <MathView math="\psi_0" /> (или <MathView math="\zeta" />):</span>
              <span className="text-sky-400 font-mono font-bold">{surfacePotential} мВ</span>
            </div>
            <input
              type="range"
              min="10"
              max="80"
              step="2"
              value={surfacePotential}
              onChange={(e) => setSurfacePotential(parseInt(e.target.value))}
              className="w-full accent-sky-500 h-1.5 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          {/* Computed Physical Parameters */}
          <div className="grid grid-cols-2 gap-2 pt-2 border-t border-neutral-800 text-[11px]">
            <div className="bg-neutral-900/80 p-2 rounded-lg border border-neutral-800">
              <span className="text-neutral-400 block text-[10px]">Дебаевская длина <MathView math="\kappa^{-1}" />:</span>
              <span className="text-emerald-400 font-mono font-bold">{debyeLength.toFixed(2)} нм</span>
            </div>
            <div className="bg-neutral-900/80 p-2 rounded-lg border border-neutral-800">
              <span className="text-neutral-400 block text-[10px]">Высота барьера <MathView math="U_{\max}" />:</span>
              <span className={`font-mono font-bold ${maxBarrierKbT > 15 ? 'text-emerald-400' : maxBarrierKbT > 0 ? 'text-amber-400' : 'text-rose-400'}`}>
                {maxBarrierKbT > 0 ? `${maxBarrierKbT.toFixed(1)} k_B T` : 'Снят (коагуляция)'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// WIDGET 6: ELECTRIC DOUBLE LAYER (EDL) STRUCTURE
export const EDLWidget: React.FC = () => {
  const [psi0, setPsi0] = useState<number>(60); // mV
  const [ionicStrength, setIonicStrength] = useState<number>(0.01); // M (0.001 to 0.1 M)

  const xStern = 0.4; // nm (Stern layer plane x1)
  const xSlip = 0.8; // nm (slipping plane)
  const psiStern = psi0 * 0.7; // ~70% potential at Stern plane

  // Debye length in water at 298 K: kappa^-1 = 0.304 / sqrt(I) nm for 1:1
  const debyeLength = 0.304 / Math.sqrt(ionicStrength); // nm

  // Generate potential profile points
  const points = [];
  for (let x = 0; x <= 4.0; x += 0.05) {
    let psi = 0;
    if (x <= xStern) {
      psi = psi0 - (psi0 - psiStern) * (x / xStern);
    } else {
      psi = psiStern * Math.exp(-(x - xStern) / debyeLength);
    }
    points.push({
      x: parseFloat(x.toFixed(2)),
      psi: parseFloat(psi.toFixed(1))
    });
  }

  const zetaPotential = (psiStern * Math.exp(-(xSlip - xStern) / debyeLength)).toFixed(1);

  return (
    <div className="bg-neutral-900/90 border border-neutral-800 rounded-2xl p-4 sm:p-5 flex flex-col space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-neutral-800 pb-3">
        <div>
          <span className="text-xs font-mono text-cyan-400 uppercase tracking-widest font-bold">
            Строение двойного электрического слоя (ДЭС)
          </span>
          <h3 className="text-lg font-bold text-white font-['Newsreader']">
            Модель Штерна–Грэма: плотный слой Штерна и диффузный слой Гуи
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs px-3 py-1 bg-cyan-950/80 border border-cyan-700 text-cyan-300 rounded-full font-semibold font-mono">
            Дзета-потенциал <MathView math="\zeta =" /> {zetaPotential} мВ
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-center">
        {/* Profile Chart */}
        <div className="lg:col-span-7 bg-neutral-950/80 p-3 rounded-xl border border-neutral-800 flex flex-col">
          <div className="h-56 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={points} margin={{ top: 10, right: 20, left: 0, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#262626" />
                <XAxis 
                  dataKey="x" 
                  stroke="#737373" 
                  fontSize={10} 
                  label={{ value: 'Расстояние от поверхности x (нм)', position: 'insideBottom', offset: -10, fill: '#a3a3a3', fontSize: 10 }} 
                />
                <YAxis 
                  stroke="#737373" 
                  fontSize={10} 
                  domain={[0, 100]} 
                  label={{ value: 'Потенциал ψ(x) (мВ)', angle: -90, position: 'insideLeft', fill: '#a3a3a3', fontSize: 10 }} 
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#171717', borderColor: '#404040', borderRadius: '0.75rem', fontSize: '11px' }} 
                  formatter={(val: number) => [`${val} мВ`, 'Потенциал ψ(x)']}
                />
                <ReferenceLine x={xStern} stroke="#f59e0b" strokeDasharray="3 3" label={{ value: 'Слой Штерна x₁', fill: '#f59e0b', fontSize: 10 }} />
                <ReferenceLine x={xSlip} stroke="#38bdf8" strokeDasharray="3 3" label={{ value: 'Плоскость скольжения (ζ)', fill: '#38bdf8', fontSize: 10 }} />
                <Line type="monotone" dataKey="psi" stroke="#06b6d4" strokeWidth={2.5} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="flex justify-between items-center text-[10px] text-neutral-400 mt-2 px-1">
            <span className="text-amber-400">0 &lt; x &lt; 0.4 нм: Плотный слой Штерна (линейное падение)</span>
            <span className="text-cyan-400">x &gt; 0.4 нм: Диффузный слой Гуи (<MathView math="\psi \propto e^{-\kappa x}" />)</span>
          </div>
        </div>

        {/* Controls and Explanations */}
        <div className="lg:col-span-5 bg-neutral-950/60 p-4 rounded-xl border border-neutral-800 space-y-3">
          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-neutral-300">Потенциал поверхности <MathView math="\psi_0" />:</span>
              <span className="text-white font-mono font-bold">{psi0} мВ</span>
            </div>
            <input
              type="range"
              min="20"
              max="100"
              step="5"
              value={psi0}
              onChange={(e) => setPsi0(parseInt(e.target.value))}
              className="w-full accent-cyan-500 h-1.5 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-neutral-300">Ионная сила раствора I:</span>
              <span className="text-emerald-400 font-mono font-bold">{ionicStrength.toFixed(3)} М</span>
            </div>
            <input
              type="range"
              min="0.001"
              max="0.1"
              step="0.002"
              value={ionicStrength}
              onChange={(e) => setIonicStrength(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 h-1.5 bg-neutral-800 rounded-lg appearance-none cursor-pointer"
            />
          </div>

          <div className="bg-neutral-900/80 p-3 rounded-xl border border-neutral-800 text-xs space-y-1.5 text-neutral-300">
            <div className="flex justify-between">
              <span className="text-neutral-400">Дебаевская толщина <MathView math="\kappa^{-1}" />:</span>
              <span className="font-mono font-bold text-white">{debyeLength.toFixed(2)} нм</span>
            </div>
            <div className="flex justify-between">
              <span className="text-neutral-400">Дзета-потенциал <MathView math="\zeta" />:</span>
              <span className="font-mono font-bold text-cyan-400">{zetaPotential} мВ</span>
            </div>
            <p className="text-[11px] text-neutral-400 border-t border-neutral-800 pt-1.5 mt-1 leading-relaxed">
              При росте ионной силы $I$ дебаевская длина сжимается (<MathView math="\kappa^{-1} \propto 1/\sqrt{I}" />), потенциал на плоскости скольжения <MathView math="\zeta" /> падает, что приводит к коагуляции.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};


