from flask import Flask, request, redirect, url_for
import os

app = Flask(__name__)

DATA_DIR = '/app/data'
@app.route('/')
def index():
    notes = []
    if os.path.exists(DATA_DIR):
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.txt'):
                with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
                    notes.append({'title': filename[:-4], 'content': f.read()})
    html = "<h1>Мои заметки</h1>"
    html += "<form method='POST' action='/add'>"
    html += "<input type='text' name='title' placeholder='Заголовок' required> "
    html += "<input type='text' name='content' placeholder='Текст заметки' required> "
    html += "<button type='submit'>Добавить</button></form><hr>"
    if not notes:
        html += "<p>Пока нет заметок.</p>"
    else:
        for note in notes:
            html += f"<h3>{note['title']}</h3><p>{note['content']}</p><hr>"
    return html

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '_', '-')).strip()
    if safe_title and content:
        filepath = os.path.join(DATA_DIR, f"{safe_title}.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
