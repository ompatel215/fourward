# Course.py

class CourseScheduler:
    def __init__(self):
        # Dictionary to store courses and their prerequisites
        self.graph = {}

    def add_course(self, course):
        """Add a course to the graph."""
        if course not in self.graph:
            self.graph[course] = []

    def add_prerequisite(self, course, prerequisite):
        """Add a prerequisite relationship (prerequisite -> course)."""
        if course not in self.graph:
            self.add_course(course)
        if prerequisite not in self.graph:
            self.add_course(prerequisite)
        self.graph[course].append(prerequisite)

    def get_prerequisites(self, course, visited=None):
        """Get all prerequisites for a given course."""
        if visited is None:
            visited = set()
        if course not in self.graph:
            return f"Course {course} not found in the graph."
        prerequisites = set()
        for prereq in self.graph[course]:
            if prereq not in visited:
                visited.add(prereq)
                prerequisites.add(prereq)
                prerequisites.update(self.get_prerequisites(prereq, visited))
        return prerequisites

    def display_courses(self):
        """Display all courses and their prerequisites."""
        for course in self.graph:
            prerequisites = self.get_prerequisites(course)
            print(f"Course: {course}, Prerequisites: {prerequisites}")

    def load_courses_from_excel(self, file_path):
        """Load courses and prerequisites from an Excel file."""
        from openpyxl import load_workbook
        workbook = load_workbook(filename=file_path)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):  # Assuming the first row is headers
            course, prerequisite = row
            self.add_course(course)
            if prerequisite:  # Check if prerequisite is not None
                self.add_prerequisite(course, prerequisite)