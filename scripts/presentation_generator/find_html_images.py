import re

with open(r'course_materials/literature/Электронный учебник по термодинамике.htm', 'rb') as f:
    raw = f.read()

# detect encoding from header
m = re.search(rb'charset=([^\">\s]+)', raw)
print('Charset in HTML:', m.group(1) if m else 'not found')

# decode
text = raw.decode('windows-1251', errors='replace')
print('Length of decoded HTML:', len(text))

# Let's find occurrences of "Фазовые" or "равновесия" or "ликвидус"
for term in ['Фазовые', 'ликвидус', 'солидус', 'рычаг', 'эвтектик']:
    pos = text.lower().find(term.lower())
    print(f'Term "{term}": pos={pos}')

# Find all image files
matches = list(re.finditer(r'image\d+\.(?:jpg|png|gif|wmf|emf)', text, re.IGNORECASE))
print(f'Total image references in HTML: {len(matches)}')

# Let's find images where term is near
img_entries = []
for m in matches:
    img_name = m.group(0)
    # look at surrounding 300 characters
    start = max(0, m.start() - 300)
    end = min(len(text), m.end() + 300)
    snippet = re.sub(r'<[^>]+>', ' ', text[start:end])
    snippet = ' '.join(snippet.split())
    img_entries.append((img_name, snippet, m.start()))

with open('all_diagram_images.txt', 'w', encoding='utf-8') as out:
    for name, snip, pos in img_entries:
        if any(k in snip.lower() for k in ['ликвидус', 'солидус', 'эвтектик', 'рычаг', 'фаз', 'кристал', 'расплав', 'диаграмм']):
            out.write(f'{name} (pos {pos}): {snip}\n\n')

print('Wrote all_diagram_images.txt!')
