# app.py

from flask import Flask, request, redirect, url_for, render_template, jsonify
from Course import CourseScheduler

app = Flask(__name__)
scheduler = CourseScheduler()

@app.route('/')
def index():
    return render_template('index.html')

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
    return jsonify({"course": course, "prerequisites": list(prerequisites)})

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
    return jsonify(courses)

@app.route('/load_courses', methods=['POST'])
def load_courses():
    file = request.files['file']
    try:
        scheduler.load_courses_from_excel(file)
        return jsonify({"message": "Courses loaded successfully from Excel."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)