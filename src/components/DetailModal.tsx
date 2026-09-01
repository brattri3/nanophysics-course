import React from 'react';
import {
  X,
  Calendar,
  Clock,
  MapPin,
  BookOpen,
  FlaskConical,
  CheckCircle2,
  BookmarkCheck,
  GraduationCap,
} from 'lucide-react';
import { ScheduleItem } from '../data/scheduleData';

interface DetailModalProps {
  item: ScheduleItem | null;
  onClose: () => void;
}

export const DetailModal: React.FC<DetailModalProps> = ({ item, onClose }) => {
  if (!item) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-neutral-950/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div
        className="bg-white w-full max-w-2xl rounded-2xl shadow-xl border border-neutral-200 overflow-hidden animate-in fade-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-start justify-between p-6 border-b border-neutral-100 bg-neutral-50/50">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span
                className={`text-xs font-bold uppercase tracking-wider px-2.5 py-1 rounded-md ${
                  item.type === 'lecture'
                    ? 'bg-blue-100 text-blue-900 border border-blue-200'
                    : 'bg-amber-100 text-amber-900 border border-amber-200'
                }`}
              >
                {item.type === 'lecture' ? 'Лекционное занятие' : 'Лабораторная работа'}
              </span>
              <span className="text-xs font-medium text-neutral-600 bg-neutral-200/70 px-2 py-0.5 rounded">
                Занятие №{item.sessionNumber} • Неделя {item.weekNumber} ({item.isOddWeek ? 'Верхняя/Нечетная' : 'Нижняя/Четная'})
              </span>
              <span className="text-xs font-medium text-neutral-600 bg-neutral-200/70 px-2 py-0.5 rounded">
                Пара {item.pairNumber} ({item.time})
              </span>
            </div>
            <h2 className="text-lg sm:text-xl font-bold text-neutral-900 leading-snug">
              {item.title}
            </h2>
            <p className="text-sm text-neutral-600 mt-1">{item.subtitle}</p>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-neutral-400 hover:text-neutral-700 hover:bg-neutral-100 rounded-lg transition-colors ml-4 shrink-0"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-5 max-h-[70vh] overflow-y-auto">
          
          {/* Metadata chips */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 p-3.5 bg-neutral-50 rounded-xl border border-neutral-200 text-xs">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-neutral-500 shrink-0" />
              <div>
                <div className="text-neutral-500">Дата проведения</div>
                <div className="font-semibold text-neutral-900">{item.date}</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-neutral-500 shrink-0" />
              <div>
                <div className="text-neutral-500">Время и объем</div>
                <div className="font-semibold text-neutral-900">{item.time} ({item.durationHours} ч.)</div>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-neutral-500 shrink-0" />
              <div>
                <div className="text-neutral-500">Аудитория</div>
                <div className="font-semibold text-neutral-900">{item.auditory}</div>
              </div>
            </div>
          </div>

          {/* Detailed Description */}
          <div>
            <h3 className="text-xs uppercase font-bold text-neutral-400 tracking-wider mb-2">
              Аннотация и цели занятия
            </h3>
            <p className="text-sm text-neutral-700 leading-relaxed bg-white p-3.5 rounded-xl border border-neutral-200">
              {item.description}
            </p>
          </div>

          {/* Detailed Topics List */}
          <div>
            <h3 className="text-xs uppercase font-bold text-neutral-400 tracking-wider mb-2">
              Рассматриваемые вопросы и этапы
            </h3>
            <ul className="space-y-2">
              {item.topics.map((t, idx) => (
                <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-neutral-800">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                  <span>{t}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Equipment / References */}
          {item.equipmentOrLiterature && (
            <div className="p-3.5 bg-blue-50/50 rounded-xl border border-blue-100 text-xs sm:text-sm text-blue-950">
              <div className="font-semibold flex items-center gap-1.5 text-blue-900 mb-1">
                {item.type === 'lecture' ? (
                  <BookOpen className="w-4 h-4 text-blue-700" />
                ) : (
                  <FlaskConical className="w-4 h-4 text-blue-700" />
                )}
                <span>{item.type === 'lecture' ? 'Рекомендованная литература:' : 'Оборудование и реактивы:'}</span>
              </div>
              <p className="text-blue-900/90 leading-relaxed">{item.equipmentOrLiterature}</p>
            </div>
          )}

          {/* Competencies */}
          <div className="flex items-center gap-2 pt-2 border-t border-neutral-100">
            <GraduationCap className="w-4 h-4 text-neutral-400 shrink-0" />
            <span className="text-xs text-neutral-500 font-medium">Формируемые компетенции:</span>
            <div className="flex flex-wrap gap-1.5">
              {item.competencies.map((comp) => (
                <span
                  key={comp}
                  className="px-2 py-0.5 bg-neutral-100 border border-neutral-200 text-neutral-800 text-[11px] font-semibold rounded"
                >
                  {comp}
                </span>
              ))}
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="p-4 border-t border-neutral-100 bg-neutral-50/50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-neutral-900 hover:bg-neutral-800 text-white text-xs font-semibold rounded-xl transition-colors"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>
  );
};
