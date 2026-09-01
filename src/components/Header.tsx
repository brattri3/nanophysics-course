import React from 'react';
import {
  GraduationCap,
  Calendar,
  Clock,
  BookOpen,
  FlaskConical,
  Award,
  MapPin,
  Users,
} from 'lucide-react';
import { COURSE_SUMMARY } from '../data/scheduleData';

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b border-neutral-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        
        {/* Academic badges */}
        <div className="flex flex-wrap items-center gap-2 mb-4">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-neutral-100 text-neutral-800 text-xs font-semibold rounded-md border border-neutral-200">
            <GraduationCap className="w-3.5 h-3.5 text-blue-700" />
            <span>{COURSE_SUMMARY.university} • {COURSE_SUMMARY.department}</span>
          </div>
          <div className="inline-flex items-center gap-1 px-2.5 py-1 bg-blue-50 text-blue-800 text-xs font-medium rounded-md border border-blue-200">
            <span>Направление: {COURSE_SUMMARY.code} {COURSE_SUMMARY.specialty}</span>
          </div>
          <div className="inline-flex items-center gap-1 px-2.5 py-1 bg-amber-50 text-amber-800 text-xs font-medium rounded-md border border-amber-200">
            <Users className="w-3.5 h-3.5 text-amber-700" />
            <span>Группа: {COURSE_SUMMARY.group}</span>
          </div>
          <div className="inline-flex items-center gap-1 px-2.5 py-1 bg-purple-50 text-purple-800 text-xs font-medium rounded-md border border-purple-200">
            <MapPin className="w-3.5 h-3.5 text-purple-700" />
            <span>{COURSE_SUMMARY.auditory} ({COURSE_SUMMARY.building})</span>
          </div>
        </div>

        {/* Main Title & Subtitle */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl lg:text-4xl font-serif text-neutral-950 font-bold tracking-tight">
              {COURSE_SUMMARY.title}
            </h1>
            <p className="text-sm sm:text-base text-neutral-600 mt-2 max-w-3xl leading-relaxed">
              Календарно-тематический план и учебно-методический комплекс на <span className="font-semibold text-neutral-900">{COURSE_SUMMARY.term}</span> ({COURSE_SUMMARY.semester} семестр).
              Преподаватель: <span className="font-semibold text-neutral-900">{COURSE_SUMMARY.instructor}</span>.
            </p>
          </div>

          <div className="shrink-0 bg-neutral-50 px-4 py-3 rounded-xl border border-neutral-200 text-right md:text-left">
            <div className="text-xs text-neutral-500 font-medium">Форма итогового контроля</div>
            <div className="text-sm sm:text-base font-bold text-neutral-900 flex items-center gap-1.5 mt-0.5">
              <Award className="w-4 h-4 text-emerald-600" />
              {COURSE_SUMMARY.controlType}
            </div>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mt-6 pt-6 border-t border-neutral-100">
          
          <div className="bg-neutral-50 p-3.5 sm:p-4 rounded-xl border border-neutral-200/80">
            <div className="flex items-center gap-2 text-neutral-500 text-xs font-medium">
              <Calendar className="w-4 h-4 text-neutral-700" />
              <span>Всего занятий</span>
            </div>
            <div className="text-xl sm:text-2xl font-bold text-neutral-900 mt-1.5">
              26 <span className="text-xs font-normal text-neutral-500">пар / 52 ч</span>
            </div>
            <div className="text-[11px] text-neutral-500 mt-1">Каждую среду (сентябрь–декабрь)</div>
          </div>

          <div className="bg-blue-50/60 p-3.5 sm:p-4 rounded-xl border border-blue-100">
            <div className="flex items-center gap-2 text-blue-800 text-xs font-medium">
              <BookOpen className="w-4 h-4 text-blue-700" />
              <span>Лекции</span>
            </div>
            <div className="text-xl sm:text-2xl font-bold text-blue-950 mt-1.5">
              9 <span className="text-xs font-normal text-blue-700">тем / 18 ч</span>
            </div>
            <div className="text-[11px] text-blue-700 mt-1">1 пара (09:30–11:00, нечет. нед.)</div>
          </div>

          <div className="bg-amber-50/60 p-3.5 sm:p-4 rounded-xl border border-amber-100">
            <div className="flex items-center gap-2 text-amber-800 text-xs font-medium">
              <FlaskConical className="w-4 h-4 text-amber-700" />
              <span>Лабораторные</span>
            </div>
            <div className="text-xl sm:text-2xl font-bold text-amber-950 mt-1.5">
              17 <span className="text-xs font-normal text-amber-700">пар / 34 ч</span>
            </div>
            <div className="text-[11px] text-amber-700 mt-1">3 пара (13:00–14:30, еженедельно)</div>
          </div>

          <div className="bg-emerald-50/60 p-3.5 sm:p-4 rounded-xl border border-emerald-100">
            <div className="flex items-center gap-2 text-emerald-800 text-xs font-medium">
              <Clock className="w-4 h-4 text-emerald-700" />
              <span>Общая трудоемкость</span>
            </div>
            <div className="text-xl sm:text-2xl font-bold text-emerald-950 mt-1.5">
              108 <span className="text-xs font-normal text-emerald-700">акад. часов</span>
            </div>
            <div className="text-[11px] text-emerald-700 mt-1">3 зачетные единицы (ЗЕТ)</div>
          </div>

        </div>

      </div>
    </header>
  );
};
