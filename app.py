from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db=SQLAlchemy(app)

class Task(db.Model):
    sno=db.Column(db.Integer , primary_key=True)
    title=db.Column(db.String , nullable=False)
    # desc= db.Column(db.String , nullable=False)
    # date= db.Column(db.DateTime , default=datetime.now)
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# way of initializing page
@app.route('/' , methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        t=request.form['title'] # getting the value from form(in html) of website     
        #initializing object of task class
        todo=Task()
        todo.title=t
        #adding the details in database
        db.session.add(todo)
        #saving details in database
        db.session.commit()


    #accessing the database
    all_task= Task.query.all()
    return render_template('index.html' , tasks=all_task) #running index.html and passing the stored database in all_task as a variable tasks to index.html

#deleting
@app.route('/Delete/<int:sno>')
def delete(sno):
    del_task = Task.query.filter_by(sno=sno).first()
    db.session.delete(del_task)
    db.session.commit()
    return redirect('/')

#update
@app.route('/Update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        t=request.form['title']
        todo=Task.query.filter_by(sno=sno).first()
        todo.title=t
        #adding the details in database
        db.session.add(todo)
        #saving details in database
        db.session.commit()
        return redirect('/')

    todo=Task.query.filter_by(sno=sno).first()
    return render_template('update.html' , data=todo)

#about us
@app.route('/About')
def about():
    return render_template('about.html')
# running flask
if __name__ == '__main__':
    app.run(debug=True)
