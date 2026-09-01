import React from 'react';
import { BookOpen, Calendar, Clock, CheckCircle2, ChevronRight, Play } from 'lucide-react';
import { FULL_SCHEDULE, ScheduleItem } from '../data/scheduleData';

interface LecturesViewProps {
  onSelectItem: (item: ScheduleItem) => void;
  onStartPresentation: (id: string) => void;
}

export const LecturesView: React.FC<LecturesViewProps> = ({ onSelectItem, onStartPresentation }) => {
  const lectures = FULL_SCHEDULE.filter((item) => item.type === 'lecture');

  return (
    <div className="space-y-6">
      <div className="bg-blue-50/50 p-5 rounded-2xl border border-blue-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-blue-950 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-blue-700" />
            Теоретический курс лекций (Семестр 4)
          </h2>
          <p className="text-xs text-blue-800/80 mt-1 max-w-2xl">
            9 лекций (18 академических часов), проводятся по нечетным неделям (1 пара: 09:30–11:00 в ауд. 31-04а).
            Охватывают 4 ключевых раздела РПД.
          </p>
        </div>
        <div className="text-xs font-semibold text-blue-900 bg-white px-3.5 py-2 rounded-xl border border-blue-200 shadow-2xs self-start sm:self-auto">
          Всего: 9 тем / 18 часов
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {lectures.map((lec, idx) => (
          <div
            key={lec.id}
            onClick={() => onSelectItem(lec)}
            className="group bg-white p-5 rounded-2xl border border-neutral-200 hover:border-blue-300 hover:shadow-xs transition-all cursor-pointer flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-[11px] font-bold text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200/60">
                  {lec.rpdSection || `Лекция ${idx + 1}`}
                </span>
                <div className="flex items-center gap-1.5 text-xs text-neutral-500">
                  <Calendar className="w-3.5 h-3.5 text-neutral-400" />
                  <span>{lec.date} (Нед. {lec.weekNumber})</span>
                </div>
              </div>

              <h3 className="text-sm font-bold text-neutral-900 group-hover:text-blue-600 transition-colors leading-snug mt-1">
                {lec.title}
              </h3>
              <p className="text-xs text-neutral-600 mt-1.5 leading-relaxed line-clamp-3">
                {lec.description}
              </p>

              <div className="mt-3 pt-3 border-t border-neutral-100 space-y-1.5">
                {lec.topics.slice(0, 3).map((topic, tIdx) => (
                  <div key={tIdx} className="flex items-start gap-2 text-xs text-neutral-700">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                    <span className="line-clamp-1">{topic}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-neutral-100 flex items-center justify-between text-xs text-neutral-500">
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" /> 09:30 — 11:00 (2 ч.)
              </span>
              
              <div className="flex items-center gap-3">
                {idx === 0 && (
                  <button 
                    onClick={(e) => { e.stopPropagation(); onStartPresentation('lec1'); }}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-600 text-white hover:bg-emerald-700 transition-colors shadow-xs"
                  >
                    <Play className="w-3.5 h-3.5 fill-current" />
                    Запустить презентацию
                  </button>
                )}
                
                <span className="font-semibold text-blue-600 flex items-center gap-0.5 group-hover:translate-x-0.5 transition-transform">
                  Тезисы <ChevronRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
