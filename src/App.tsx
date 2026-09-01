import React, { useState } from 'react';
import {
  CalendarDays,
  BookOpen,
  FlaskConical,
  Files,
  Sparkles,
  Info,
} from 'lucide-react';
import { Header } from './components/Header';
import { ScheduleTimeline } from './components/ScheduleTimeline';
import { LecturesView } from './components/LecturesView';
import { LabsView } from './components/LabsView';
import { MaterialsView } from './components/MaterialsView';
import { DetailModal } from './components/DetailModal';
import { ScheduleItem } from './data/scheduleData';
import { Lecture1 } from './components/presentation/Lecture1';

export default function App() {
  const [activeTab, setActiveTab] = useState<'schedule' | 'lectures' | 'labs' | 'materials'>('schedule');
  const [selectedItem, setSelectedItem] = useState<ScheduleItem | null>(null);
  const [activePresentation, setActivePresentation] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-neutral-100/70 text-neutral-900 font-sans flex flex-col">
      
      {activePresentation === 'lec1' && (
        <Lecture1 onClose={() => setActivePresentation(null)} />
      )}

      {/* Top Banner / Header */}
      <Header />

      {/* Main Navigation Tabs */}
      <div className="bg-white border-b border-neutral-200 sticky top-0 z-20 shadow-2xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-1 sm:space-x-4 overflow-x-auto py-2.5 no-scrollbar">
            
            <button
              id="tab-schedule-btn"
              onClick={() => setActiveTab('schedule')}
              className={`flex items-center gap-2 px-3.5 py-2 text-xs sm:text-sm font-semibold rounded-xl whitespace-nowrap transition-all ${
                activeTab === 'schedule'
                  ? 'bg-neutral-900 text-white shadow-xs'
                  : 'text-neutral-600 hover:text-neutral-950 hover:bg-neutral-100'
              }`}
            >
              <CalendarDays className="w-4 h-4" />
              <span>Календарный график (26 занятий)</span>
            </button>

            <button
              id="tab-lectures-btn"
              onClick={() => setActiveTab('lectures')}
              className={`flex items-center gap-2 px-3.5 py-2 text-xs sm:text-sm font-semibold rounded-xl whitespace-nowrap transition-all ${
                activeTab === 'lectures'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-neutral-600 hover:text-neutral-950 hover:bg-neutral-100'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              <span>Лекции (9 тем)</span>
            </button>

            <button
              id="tab-labs-btn"
              onClick={() => setActiveTab('labs')}
              className={`flex items-center gap-2 px-3.5 py-2 text-xs sm:text-sm font-semibold rounded-xl whitespace-nowrap transition-all ${
                activeTab === 'labs'
                  ? 'bg-amber-600 text-white shadow-xs'
                  : 'text-neutral-600 hover:text-neutral-950 hover:bg-neutral-100'
              }`}
            >
              <FlaskConical className="w-4 h-4" />
              <span>Лабораторный практикум (9 работ)</span>
            </button>

            <button
              id="tab-materials-btn"
              onClick={() => setActiveTab('materials')}
              className={`flex items-center gap-2 px-3.5 py-2 text-xs sm:text-sm font-semibold rounded-xl whitespace-nowrap transition-all ${
                activeTab === 'materials'
                  ? 'bg-emerald-700 text-white shadow-xs'
                  : 'text-neutral-600 hover:text-neutral-950 hover:bg-neutral-100'
              }`}
            >
              <Files className="w-4 h-4" />
              <span>Учебно-методическая база (РПД)</span>
            </button>

          </nav>
        </div>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
        
        {activeTab === 'schedule' && (
          <ScheduleTimeline onSelectItem={(item) => setSelectedItem(item)} />
        )}

        {activeTab === 'lectures' && (
          <LecturesView 
            onSelectItem={(item) => setSelectedItem(item)} 
            onStartPresentation={(id) => setActivePresentation(id)}
          />
        )}

        {activeTab === 'labs' && (
          <LabsView onSelectItem={(item) => setSelectedItem(item)} />
        )}

        {activeTab === 'materials' && (
          <MaterialsView />
        )}

      </main>

      {/* Detail Modal */}
      <DetailModal item={selectedItem} onClose={() => setSelectedItem(null)} />

      {/* Footer */}
      <footer className="bg-white border-t border-neutral-200 py-6 text-center text-xs text-neutral-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-neutral-800">ГУАП</span>
            <span>•</span>
            <span>Кафедра физики №3</span>
            <span>•</span>
            <span>Курс «Физические основы нанотехнологий» (Осень 2026)</span>
          </div>
          <div className="text-neutral-400">
            Сформировано методистом <span className="font-medium text-neutral-700">[CourseManager]</span> по утвержденной РПД
          </div>
        </div>
      </footer>

    </div>
  );
}
