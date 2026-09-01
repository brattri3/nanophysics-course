import React, { useState, useMemo } from 'react';
import {
  Search,
  Filter,
  Calendar,
  Clock,
  BookOpen,
  FlaskConical,
  ChevronRight,
  Sparkles,
  MapPin,
} from 'lucide-react';
import { FULL_SCHEDULE, ScheduleItem } from '../data/scheduleData';

interface ScheduleTimelineProps {
  onSelectItem: (item: ScheduleItem) => void;
}

export const ScheduleTimeline: React.FC<ScheduleTimelineProps> = ({ onSelectItem }) => {
  const [typeFilter, setTypeFilter] = useState<'all' | 'lecture' | 'lab'>('all');
  const [monthFilter, setMonthFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const filteredItems = useMemo(() => {
    return FULL_SCHEDULE.filter((item) => {
      // Type match
      if (typeFilter !== 'all' && item.type !== typeFilter) {
        return false;
      }

      // Month match (date format: DD.MM.YYYY)
      if (monthFilter !== 'all') {
        const month = item.date.split('.')[1];
        if (month !== monthFilter) return false;
      }

      // Search match
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const inTitle = item.title.toLowerCase().includes(q);
        const inSubtitle = item.subtitle.toLowerCase().includes(q);
        const inDesc = item.description.toLowerCase().includes(q);
        const inTopics = item.topics.some((t) => t.toLowerCase().includes(q));
        const inDate = item.date.includes(q);
        if (!inTitle && !inSubtitle && !inDesc && !inTopics && !inDate) {
          return false;
        }
      }

      return true;
    });
  }, [typeFilter, monthFilter, searchQuery]);

  return (
    <div className="space-y-6">
      
      {/* Search and Filters Bar */}
      <div className="bg-white p-4 sm:p-5 rounded-2xl border border-neutral-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-neutral-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Поиск по теме, эффекту, веществу (например: плазмон, Ag, ZnO, АСМ)..."
            className="w-full pl-10 pr-4 py-2 bg-neutral-50 border border-neutral-200 rounded-xl text-xs sm:text-sm text-neutral-900 placeholder:text-neutral-400 focus:outline-hidden focus:ring-2 focus:ring-neutral-900/10 focus:border-neutral-400 transition-all"
          />
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-2.5">
          
          {/* Type Filter */}
          <div className="flex bg-neutral-100 p-1 rounded-xl">
            <button
              onClick={() => setTypeFilter('all')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                typeFilter === 'all'
                  ? 'bg-white text-neutral-900 shadow-xs'
                  : 'text-neutral-600 hover:text-neutral-900'
              }`}
            >
              Все ({FULL_SCHEDULE.length})
            </button>
            <button
              onClick={() => setTypeFilter('lecture')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                typeFilter === 'lecture'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-neutral-600 hover:text-neutral-900'
              }`}
            >
              Лекции (9)
            </button>
            <button
              onClick={() => setTypeFilter('lab')}
              className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                typeFilter === 'lab'
                  ? 'bg-amber-600 text-white shadow-xs'
                  : 'text-neutral-600 hover:text-neutral-900'
              }`}
            >
              Лабораторные (17)
            </button>
          </div>

          {/* Month Filter */}
          <select
            value={monthFilter}
            onChange={(e) => setMonthFilter(e.target.value)}
            className="px-3 py-1.5 bg-neutral-50 border border-neutral-200 rounded-xl text-xs font-medium text-neutral-800 focus:outline-hidden focus:ring-2 focus:ring-neutral-900/10"
          >
            <option value="all">Все месяцы</option>
            <option value="09">Сентябрь (6 пар)</option>
            <option value="10">Октябрь (8 пар)</option>
            <option value="11">Ноябрь (6 пар)</option>
            <option value="12">Декабрь (6 пар)</option>
          </select>

        </div>

      </div>

      {/* Schedule Items List */}
      <div className="space-y-3">
        {filteredItems.length === 0 ? (
          <div className="bg-white p-12 text-center rounded-2xl border border-neutral-200">
            <Filter className="w-8 h-8 text-neutral-400 mx-auto mb-3" />
            <h3 className="text-base font-semibold text-neutral-800">Занятий не найдено</h3>
            <p className="text-xs text-neutral-500 mt-1">
              Попробуйте изменить параметры поиска или сбросить фильтры.
            </p>
          </div>
        ) : (
          filteredItems.map((item) => (
            <div
              key={item.id}
              onClick={() => onSelectItem(item)}
              className="group bg-white p-4 sm:p-5 rounded-2xl border border-neutral-200 hover:border-neutral-300 hover:shadow-xs transition-all cursor-pointer flex flex-col lg:flex-row lg:items-center justify-between gap-4"
            >
              {/* Date & Week badge column */}
              <div className="flex sm:items-center gap-3 shrink-0">
                <div className="w-16 h-16 rounded-xl bg-neutral-50 border border-neutral-200/80 flex flex-col items-center justify-center text-center shrink-0">
                  <span className="text-[10px] uppercase font-bold text-neutral-400">
                    {item.date.split('.')[1] === '09'
                      ? 'СЕН'
                      : item.date.split('.')[1] === '10'
                      ? 'ОКТ'
                      : item.date.split('.')[1] === '11'
                      ? 'НОЯ'
                      : 'ДЕК'}
                  </span>
                  <span className="text-xl font-bold text-neutral-900 leading-none mt-0.5">
                    {item.date.split('.')[0]}
                  </span>
                  <span className="text-[9px] text-neutral-500 mt-0.5">2026</span>
                </div>

                <div>
                  <div className="flex flex-wrap items-center gap-1.5 mb-1">
                    <span
                      className={`text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md ${
                        item.type === 'lecture'
                          ? 'bg-blue-100 text-blue-900 border border-blue-200'
                          : 'bg-amber-100 text-amber-900 border border-amber-200'
                      }`}
                    >
                      {item.type === 'lecture' ? 'Лекция' : 'Лабораторная'}
                    </span>
                    <span className="text-[11px] text-neutral-500 font-medium">
                      Нед. {item.weekNumber} ({item.isOddWeek ? 'нечет./верх.' : 'чет./ниж.'})
                    </span>
                  </div>
                  
                  <div className="flex items-center gap-2 text-xs text-neutral-500">
                    <span className="flex items-center gap-1 font-medium text-neutral-700">
                      <Clock className="w-3.5 h-3.5 text-neutral-400" />
                      Пара {item.pairNumber} ({item.time})
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-1">
                      <MapPin className="w-3.5 h-3.5 text-neutral-400" />
                      {item.auditory}
                    </span>
                  </div>
                </div>
              </div>

              {/* Title & Description Column */}
              <div className="flex-1 lg:px-4 space-y-1">
                <h3 className="text-sm sm:text-base font-semibold text-neutral-950 group-hover:text-blue-600 transition-colors">
                  {item.title}
                </h3>
                <p className="text-xs text-neutral-600 line-clamp-2 leading-relaxed">
                  {item.subtitle} — {item.description}
                </p>
                <div className="flex flex-wrap gap-1.5 pt-1">
                  {item.topics.slice(0, 2).map((t, idx) => (
                    <span
                      key={idx}
                      className="text-[11px] bg-neutral-100 text-neutral-700 px-2 py-0.5 rounded border border-neutral-200/60"
                    >
                      {t.length > 55 ? t.slice(0, 55) + '...' : t}
                    </span>
                  ))}
                  {item.topics.length > 2 && (
                    <span className="text-[11px] text-neutral-400 self-center">
                      +{item.topics.length - 2} темы
                    </span>
                  )}
                </div>
              </div>

              {/* Right Action */}
              <div className="shrink-0 flex items-center justify-end sm:justify-start lg:justify-end">
                <span className="inline-flex items-center gap-1 text-xs font-semibold text-neutral-500 group-hover:text-blue-600 transition-colors">
                  Подробнее
                  <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
                </span>
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  );
};
