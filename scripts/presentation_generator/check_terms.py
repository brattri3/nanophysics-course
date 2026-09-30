with open(r'course_materials/literature/Электронный учебник по термодинамике.htm', 'r', encoding='windows-1251', errors='ignore') as f:
    text = f.read().lower()

for term in ['лаплас', 'кельвин', 'томсон', 'поверхностн', 'зародыш', 'капилляр', 'адсорбц']:
    cnt = text.count(term)
    print(f'Term "{term}": count={cnt}')
