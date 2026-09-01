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
