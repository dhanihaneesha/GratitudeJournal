from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

entries = []

CATEGORIES = ['Gratitude', 'Ideas', 'Feelings', 'Work Notes']

DAILY_PROMPTS = [
    "What made you smile today?",
    "What are you grateful for right now?",
    "What's one thing that went well today?",
    "Who are you thankful for and why?",
    "What's something beautiful you noticed today?",
    "What challenge helped you grow today?",
    "What small win can you celebrate today?"
]

@app.route('/')
def home():
    total_entries = len(entries)
    today_entries = [e for e in entries if e['date'].date() == datetime.now().date()]
    
    categories_count = {}
    for cat in CATEGORIES:
        categories_count[cat] = len([e for e in entries if e['category'] == cat])
    
    import random
    daily_prompt = random.choice(DAILY_PROMPTS)
    
    recent_entries = sorted(entries, key=lambda x: x['date'], reverse=True)[:5]
    
    return render_template('home.html', 
                         total_entries=total_entries,
                         today_entries=len(today_entries),
                         categories_count=categories_count,
                         daily_prompt=daily_prompt,
                         recent_entries=recent_entries)

@app.route('/new-entry', methods=['GET', 'POST'])
def new_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category')
        
        if title and content and category:
            entry = {
                'id': len(entries) + 1,
                'title': title,
                'content': content,
                'category': category,
                'date': datetime.now()
            }
            entries.append(entry)
            flash('Journal entry added successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Please fill in all fields', 'error')
    
    return render_template('new_entry.html', categories=CATEGORIES)

@app.route('/history')
def history():
    filter_category = request.args.get('category', 'All')
    
    if filter_category == 'All':
        filtered_entries = entries
    else:
        filtered_entries = [e for e in entries if e['category'] == filter_category]
    
    sorted_entries = sorted(filtered_entries, key=lambda x: x['date'], reverse=True)
    
    return render_template('history.html', 
                         entries=sorted_entries, 
                         categories=CATEGORIES,
                         current_filter=filter_category)

@app.route('/entry/<int:entry_id>')
def view_entry(entry_id):
    entry = next((e for e in entries if e['id'] == entry_id), None)
    if entry:
        return render_template('view_entry.html', entry=entry)
    else:
        flash('Entry not found', 'error')
        return redirect(url_for('history'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
