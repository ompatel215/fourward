# app.py

from flask import Flask, request, redirect, url_for, render_template, jsonify
from Course import CourseScheduler

app = Flask(__name__)
scheduler = CourseScheduler()

@app.route('/')
def index():
    courses = list(scheduler.graph.keys())
    return render_template('index.html', courses=courses)

@app.route('/add_course', methods=['POST'])
def add_course():
    course = request.form.get('course')
    scheduler.add_course(course)
    # Redirect back to the main menu
    return redirect(url_for('index'))

@app.route('/add_prerequisite', methods=['POST'])
def add_prerequisite():
    course = request.form.get('course')
    prerequisite = request.form.get('prerequisite')
    scheduler.add_prerequisite(course, prerequisite)
    # Redirect back to the main menu
    return redirect(url_for('index'))

@app.route('/get_prerequisites', methods=['GET'])
def get_prerequisites():
    course = request.args.get('course')
    prerequisites = scheduler.get_prerequisites(course)
    return render_template('get_prerequisites.html', course=course, prerequisites=prerequisites)

@app.route('/display_courses', methods=['GET'])
def display_courses():
    courses = {
        course: {
            "prerequisites": scheduler.graph[course]["prerequisites"],
            "credits": scheduler.graph[course]["credits"],
            "description": scheduler.graph[course]["description"]
        }
        for course in scheduler.graph
    }
    return render_template('display_courses.html', courses=courses)

@app.route('/load_courses', methods=['POST'])
def load_courses():
    file = request.files['file']
    try:
        scheduler.load_courses_from_excel(file)
        # Redirect back to the main menu after successful loading
        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/delete_course', methods=['POST'])
def delete_course():
    course = request.form.get('course')
    scheduler.delete_course(course)
    return redirect(url_for('index'))

@app.route('/edit_course', methods=['POST'])
def edit_course():
    old_course = request.form.get('old_course')
    new_course = request.form.get('new_course')
    new_credits = request.form.get('new_credits')
    new_description = request.form.get('new_description')
    scheduler.edit_course(old_course, new_course, new_credits, new_description)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)