from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) #referencing this file for flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # /// relative //// absolute path
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']  #input from form
        new_task = Todo(content=task_content) #create object from classTodo as model with content from input

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'Oops! There was an issue adding your task.'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #get all tasks from db in order added
        return render_template('index.html', tasks=tasks) #no need route bcs the method auto searches for templates folder

if __name__ == "__main__":
    app.run(debug=True)