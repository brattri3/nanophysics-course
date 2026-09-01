import React from 'react';
import { FlaskConical, Calendar, Clock, CheckCircle2, ChevronRight, AlertTriangle } from 'lucide-react';
import { FULL_SCHEDULE, ScheduleItem } from '../data/scheduleData';

interface LabsViewProps {
  onSelectItem: (item: ScheduleItem) => void;
}

export const LabsView: React.FC<LabsViewProps> = ({ onSelectItem }) => {
  const labs = FULL_SCHEDULE.filter((item) => item.type === 'lab');

  return (
    <div className="space-y-6">
      <div className="bg-amber-50/50 p-5 rounded-2xl border border-amber-200/80 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-amber-950 flex items-center gap-2">
            <FlaskConical className="w-5 h-5 text-amber-700" />
            Лабораторный практикум (Семестр 4)
          </h2>
          <p className="text-xs text-amber-900/80 mt-1 max-w-2xl">
            17 аудиторных занятий (34 академических часа) — каждую среду на 3 паре (13:00–14:30).
            Практикум включает 9 лабораторных работ по синтезу наноматериалов, микроскопии и спектроскопии.
          </p>
        </div>
        <div className="text-xs font-semibold text-amber-900 bg-white px-3.5 py-2 rounded-xl border border-amber-200 shadow-2xs self-start sm:self-auto">
          Всего: 9 работ / 34 часа
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {labs.map((lab, idx) => (
          <div
            key={lab.id}
            onClick={() => onSelectItem(lab)}
            className="group bg-white p-5 rounded-2xl border border-neutral-200 hover:border-amber-300 hover:shadow-xs transition-all cursor-pointer flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-[11px] font-bold text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-200/60">
                  {lab.workNumber || `Занятие ${idx + 1}`}
                </span>
                <div className="flex items-center gap-1.5 text-xs text-neutral-500">
                  <Calendar className="w-3.5 h-3.5 text-neutral-400" />
                  <span>{lab.date} (Неделя {lab.weekNumber})</span>
                </div>
              </div>

              <h3 className="text-sm font-bold text-neutral-900 group-hover:text-amber-700 transition-colors leading-snug mt-1">
                {lab.title}
              </h3>
              <p className="text-xs text-neutral-600 mt-1.5 leading-relaxed line-clamp-2">
                {lab.subtitle}
              </p>

              {lab.equipmentOrLiterature && (
                <div className="mt-3 p-2.5 bg-neutral-50 rounded-xl border border-neutral-200 text-[11px] text-neutral-700">
                  <span className="font-semibold text-neutral-900">Оборудование: </span>
                  <span className="line-clamp-2">{lab.equipmentOrLiterature}</span>
                </div>
              )}
            </div>

            <div className="mt-4 pt-3 border-t border-neutral-100 flex items-center justify-between text-xs text-neutral-500">
              <span className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5" /> 13:00 — 14:30 (2 ч.)
              </span>
              <span className="font-semibold text-amber-700 flex items-center gap-0.5 group-hover:translate-x-0.5 transition-transform">
                Методические указания <ChevronRight className="w-3.5 h-3.5" />
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
