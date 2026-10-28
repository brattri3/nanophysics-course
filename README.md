# Физические основы нанотехнологий (Nanophysics Course)

**Университетский курс дисциплины «Физические основы нанотехнологий»**  
* Санкт-Петербургский государственный университет аэрокосмического приборостроения (ГУАП)
* Институт фундаментальной подготовки и технологических инноваций (ФПТИ), Кафедра №3 (Физика)
* Направления подготовки: **03.03.01 «Прикладные математика и физика»**, **28.03.01 «Нанотехнологии и микросистемная техника»**
* Трудоемкость: **7 ЗЕ (252 академических часа)** • Семестры 4 и 5

---

## 📂 Структура репозитория

```text
├── .agents/
│   └── skills/
│       └── scientific-presentation-creator/   # Проектный скилл создания презентаций (MCP PowerPoint + python-pptx)
├── course_materials/                          # Учебно-методическая база курса
│   ├── rpd.md                                 # Полная оцифрованная РПД (252 ч, 7 ЗЕ)
│   ├── RPD_summary.md                         # Краткая выжимка часов и тем
│   ├── literature/                            # Литература и указатели
│   │   └── literature_index.md                # Предметно-тематический указатель (Кузнецов, Сумм, Поленов)
│   └── semester_4/                            # Материалы 4-го семестра
│       ├── calendar_thematic_plan.md          # Календарный план 26 аудиторных занятий
│       ├── lectures/                          # Планы, конспекты, речи лектора и презентации (.pptx)
│       │   ├── lecture_01_notes.md            # Полный конспект Лекции №1
│       │   ├── lecture_02_thermodynamics.pptx # Презентация Лекции №2 (Термодинамика нанофаз)
│       │   ├── lecture_03_plan.md             # Послайдовый план и матрица навыков Лекции №3
│       │   ├── lecture_03_speech.md           # Полная живая речь лектора к Лекции №3 (90 мин)
│       │   └── lecture_03_colloids.pptx       # Презентация Лекции №3 (Коллоидные системы, ДЭС, ДЛФО)
│       └── manuals/                           # Учебное пособие (методичка в LaTeX/PDF)
│           ├── chapter_02_thermodynamics.tex  # Исходник Главы 2 (LaTeX)
│           ├── chapter_02_thermodynamics.pdf  # Скомпилированная Глава 2 (25 стр.)
│           └── chapter_03_colloids_blueprint.md # Архитектура и план Главы 3
├── scripts/
│   └── presentation_generator/                # Python-генераторы графиков (300 DPI) и слайдов (.pptx)
├── pyproject.toml                             # Конфигурация проекта, Python-зависимости и метаданные MCP/ПО
└── requirements.txt                           # Список Python-библиотек
```

---

## 🛠 Системные требования, внешние программы и MCP-зависимости

Для автоматизированной сборки и интерактивного редактирования материалов курса используются следующие компоненты (зафиксированные в [`pyproject.toml`](file:///c:/Users/ps656/OneDrive/Документы/nanophysics-course/pyproject.toml) и скилле [`SKILL.md`](file:///c:/Users/ps656/OneDrive/Документы/nanophysics-course/.agents/skills/scientific-presentation-creator/SKILL.md)):

### 1. Обязательные настольные программы (OS & Desktop Apps)
1. **ОС Windows 10/11** — требуется для работы COM-интерфейса `PowerPoint.Application` (`pywin32`) и MCP-сервера `powerpoint`.
2. **Microsoft PowerPoint (Desktop / Office 365 / 2019+)** — используется как для интерактивного управления презентацией на экране через MCP, так и для пакетного рендера PNG-превью слайдов.
3. **Дистрибутив LaTeX (MiKTeX или TeX Live)** с компилятором `pdflatex` и пакетами `babel-russian`, `tikz`, `pgfplots`, `tcolorbox`, `amsmath` — для сборки глав учебного пособия (`.tex` $\to$ `.pdf`).
4. **Пакетный менеджер `uv`** — для быстрого запуска Python-скриптов и управления виртуальным окружением.

### 2. Подключенные MCP-серверы (MCP Servers в Antigravity)
* **`powerpoint`** *(обязателен для интерактивного режима презентаций)* — управление живым окном Microsoft PowerPoint из чата:
  * Инструменты: `manage_presentation`, `add_slide_with_layout`, `populate_placeholder`, `manage_slide`, `switch_slide`, `slide_snapshot`, `add_speaker_notes`, `list_templates`, `analyze_template`, `add_animation`, `evaluate`.
* **`science_biomolecular_structure_viewer_mcp`** *(опционально)* — интерактивный 3D-просмотрщик кристаллических и молекулярных структур (`.cif`, `.pdb`) в боковой панели (`sidecar://`).

### 3. Python-зависимости (`pyproject.toml` / `requirements.txt`)
* `python-pptx>=1.0.2` — программная генерация и верстка презентаций `.pptx`.
* `matplotlib>=3.9.0`, `numpy>=2.0.0`, `scipy>=1.14.0` — аналитический расчет и построение научных графиков в разрешении `300 DPI`.
* `Pillow>=10.4.0` — обработка изображений.
* `pywin32>=306` — COM-автоматизация PowerPoint для экспорта превью слайдов (`export_slide_previews.py`).
* `pymupdf>=1.24.0` (`fitz`) — постраничный рендер PDF-файлов учебного пособия в PNG для визуального контроля верстки.

---

## 🚀 Быстрый старт и команды сборки

```powershell
# 1. Синхронизация Python-окружения через uv (автоматически читает pyproject.toml)
uv sync

# 2. Генерация графиков и сборка презентации Лекции 3 (.pptx)
uv run python scripts/presentation_generator/generate_lecture_03_figures.py
uv run python scripts/presentation_generator/build_lecture_03_colloids.py

# 3. Экспорт всех слайдов презентации в PNG-превью через движок PowerPoint
uv run python .agents/skills/scientific-presentation-creator/scripts/export_slide_previews.py `
  course_materials/semester_4/lectures/lecture_03_colloids.pptx `
  course_materials/semester_4/lectures/previews_l03

# 4. Компиляция главы учебного пособия в PDF
cd course_materials/semester_4/manuals
pdflatex -interaction=nonstopmode chapter_02_thermodynamics.tex
```
