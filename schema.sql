
CREATE TABLE students (
	student_id INTEGER PRIMARY KEY AUTOINCREMENT,
	first_name TEXT,
	last_name TEXT
);

CREATE TABLE quizzes (
	quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
	quiz_subject TEXT,
	number_of_question INTEGER,
	quiz_date DATE
);

CREATE TABLE student_results (
	student_id INTEGER,
	quiz_id INTEGER,
	score INTEGER
);
