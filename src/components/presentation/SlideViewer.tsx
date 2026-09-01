import React, { useState, useEffect, ReactNode, useCallback } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { X, ChevronLeft, ChevronRight, Play, FileText, Presentation, HelpCircle } from 'lucide-react';

interface SlideViewerProps {
  slides: ReactNode[];
  onClose: () => void;
  title: string;
  notesContent?: ReactNode;
}

export const SlideViewer: React.FC<SlideViewerProps> = ({ slides, onClose, title, notesContent }) => {
  const [currentSlide, setCurrentSlide] = useState(0);
  const [direction, setDirection] = useState(0);
  const [viewMode, setViewMode] = useState<'slides' | 'boardPlan'>('slides');

  const totalSlides = slides.length;

  const nextSlide = useCallback(() => {
    if (currentSlide < totalSlides - 1) {
      setDirection(1);
      setCurrentSlide((prev) => prev + 1);
    }
  }, [currentSlide, totalSlides]);

  const prevSlide = useCallback(() => {
    if (currentSlide > 0) {
      setDirection(-1);
      setCurrentSlide((prev) => prev - 1);
    }
  }, [currentSlide]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (viewMode !== 'slides') {
        if (e.key === 'Escape') onClose();
        return;
      }
      if (e.key === 'ArrowRight' || e.key === 'Space') {
        nextSlide();
      } else if (e.key === 'ArrowLeft') {
        prevSlide();
      } else if (e.key === 'Escape') {
        onClose();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [nextSlide, prevSlide, onClose, viewMode]);

  const progress = ((currentSlide + 1) / totalSlides) * 100;

  const variants = {
    enter: (dir: number) => ({
      x: dir > 0 ? '100%' : '-100%',
      opacity: 0,
    }),
    center: {
      zIndex: 1,
      x: 0,
      opacity: 1,
    },
    exit: (dir: number) => ({
      zIndex: 0,
      x: dir < 0 ? '100%' : '-100%',
      opacity: 0,
    }),
  };

  return (
    <div className="fixed inset-0 z-50 bg-neutral-950 flex flex-col font-['Manrope'] text-neutral-100 select-none">
      
      {/* TOP BAR */}
      <header className="h-14 sm:h-16 flex items-center justify-between px-3 sm:px-6 border-b border-neutral-800/80 bg-neutral-900/90 backdrop-blur shrink-0 z-20">
        <div className="flex items-center gap-2 sm:gap-3 min-w-0">
          <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
            <Play className="w-3.5 h-3.5 sm:w-4 sm:h-4 fill-current" />
          </div>
          <span className="text-xs sm:text-sm font-semibold tracking-wide text-neutral-200 truncate">
            {title}
          </span>
        </div>
        
        {/* Middle Mode Switcher (Slides vs Board Plan) */}
        <div className="flex items-center bg-neutral-800/80 p-0.5 rounded-lg border border-neutral-700/60 mx-2 shrink-0">
          <button
            onClick={() => setViewMode('slides')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
              viewMode === 'slides'
                ? 'bg-emerald-600 text-white shadow-xs'
                : 'text-neutral-400 hover:text-neutral-200'
            }`}
          >
            <Presentation className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Слайды</span>
          </button>
          
          <button
            onClick={() => setViewMode('boardPlan')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold transition-all ${
              viewMode === 'boardPlan'
                ? 'bg-emerald-600 text-white shadow-xs'
                : 'text-neutral-400 hover:text-neutral-200'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">План доски и конспект</span>
            <span className="sm:hidden">Доска</span>
          </button>
        </div>

        {/* Right controls */}
        <div className="flex items-center gap-2 sm:gap-4 shrink-0">
          {viewMode === 'slides' && (
            <span className="text-[11px] sm:text-xs font-mono text-neutral-400 px-2 py-1 rounded bg-neutral-800/50">
              {currentSlide + 1} / {totalSlides}
            </span>
          )}
          
          <button 
            onClick={onClose}
            aria-label="Закрыть"
            className="p-1.5 sm:p-2 rounded-lg hover:bg-neutral-800 text-neutral-400 hover:text-white transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>
      </header>

      {/* Progress Bar (Slides Mode) */}
      {viewMode === 'slides' && (
        <div className="h-1 bg-neutral-900 w-full z-20 shrink-0">
          <div 
            className="h-full bg-emerald-500 transition-all duration-300 ease-out" 
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {/* MAIN CONTENT AREA */}
      <main className="relative flex-1 flex items-center justify-center overflow-hidden bg-neutral-950 p-2 sm:p-4 md:p-6 lg:p-8">
        {viewMode === 'slides' ? (
          <div className="w-full h-full max-w-6xl max-h-[90vh] flex items-center justify-center relative">
            <AnimatePresence initial={false} custom={direction} mode="wait">
              <motion.div
                key={currentSlide}
                custom={direction}
                variants={variants}
                initial="enter"
                animate="center"
                exit="exit"
                transition={{
                  x: { type: "spring", stiffness: 300, damping: 30 },
                  opacity: { duration: 0.2 }
                }}
                className="w-full h-full flex items-center justify-center"
              >
                {/* Slide Card: Flexible on mobile, aspect-[16/9] on desktop when height permits */}
                <div className="w-full h-full max-h-[82vh] md:max-h-[86vh] bg-neutral-900/60 border border-neutral-800/90 rounded-2xl p-4 sm:p-6 md:p-10 lg:p-12 flex flex-col relative overflow-y-auto shadow-2xl backdrop-blur-xs">
                  {slides[currentSlide]}
                </div>
              </motion.div>
            </AnimatePresence>

            {/* Desktop Navigation Arrows on Sides */}
            {currentSlide > 0 && (
              <button
                onClick={prevSlide}
                className="hidden lg:flex absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/60 border border-neutral-700 items-center justify-center text-neutral-300 hover:text-white hover:bg-neutral-800 transition-all z-30"
              >
                <ChevronLeft className="w-6 h-6" />
              </button>
            )}

            {currentSlide < totalSlides - 1 && (
              <button
                onClick={nextSlide}
                className="hidden lg:flex absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/60 border border-neutral-700 items-center justify-center text-neutral-300 hover:text-white hover:bg-neutral-800 transition-all z-30"
              >
                <ChevronRight className="w-6 h-6" />
              </button>
            )}
          </div>
        ) : (
          /* BOARD PLAN & NOTES VIEW */
          <div className="w-full h-full max-w-4xl max-h-[88vh] bg-neutral-900/90 border border-neutral-800 rounded-2xl p-4 sm:p-8 overflow-y-auto text-neutral-200">
            {notesContent || (
              <div className="text-center py-12 text-neutral-500">
                Конспект и план работы на доске для этой лекции формируются.
              </div>
            )}
          </div>
        )}
      </main>

      {/* BOTTOM MOBILE / TOUCH CONTROLS (Always visible in slides mode) */}
      {viewMode === 'slides' && (
        <footer className="h-14 sm:h-16 px-4 border-t border-neutral-800/80 bg-neutral-900/90 flex items-center justify-between shrink-0 z-20">
          <button
            onClick={prevSlide}
            disabled={currentSlide === 0}
            className={`flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              currentSlide === 0
                ? 'opacity-40 cursor-not-allowed bg-neutral-800 text-neutral-500'
                : 'bg-neutral-800 hover:bg-neutral-700 text-white active:scale-95'
            }`}
          >
            <ChevronLeft className="w-4 h-4" />
            <span>Назад</span>
          </button>

          <div className="text-center">
            <span className="text-xs font-mono text-neutral-400">
              Слайд {currentSlide + 1} из {totalSlides}
            </span>
            <div className="hidden sm:block text-[10px] text-neutral-500 mt-0.5">
              Стрелки ← → или Пробел для навигации
            </div>
          </div>

          <button
            onClick={nextSlide}
            disabled={currentSlide === totalSlides - 1}
            className={`flex items-center gap-1.5 px-3 sm:px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
              currentSlide === totalSlides - 1
                ? 'opacity-40 cursor-not-allowed bg-neutral-800 text-neutral-500'
                : 'bg-emerald-600 hover:bg-emerald-500 text-white active:scale-95 shadow-xs'
            }`}
          >
            <span>Вперед</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </footer>
      )}
    </div>
  );
};
