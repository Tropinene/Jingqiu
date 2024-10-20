from flask import Flask, jsonify, render_template
import sqlite3

app = Flask(__name__)


def get_random_poem():
    conn = sqlite3.connect('database/poetry.db')
    cursor = conn.cursor()

    cursor.execute("SELECT title, content, author FROM works ORDER BY RANDOM() LIMIT 1")
    work_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if work_data:
        work_title, work_content, work_author = work_data
        return {
            'title': work_title,
            'content': work_content,
            'author': work_author
        }
    else:
        return None


@app.route('/')
def serve_index():
    return render_template('index.html')


@app.route('/random-poem', methods=['GET'])
def random_poem():
    poem = get_random_poem()
    if poem:
        return jsonify(poem), 200
    else:
        return jsonify({"error": "No data found"}), 404


if __name__ == '__main__':
    app.run(debug=False)
