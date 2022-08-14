
import json, os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')



class taskForm(FlaskForm):
    task = StringField('Input Task', validators=[DataRequired()])
    add = SubmitField('Add')
    delete = SubmitField('Delete')





@app.route('/', methods=['GET', 'POST', 'DELETE'])
def index():

    form = taskForm()
    
    data = None
     

    with open('tasks.txt', 'r') as file:
        print('getting data')
        data = file.read()
    
        if data != '':
            data = json.loads(data)
        else:
            data = {'tasks': []}
        tasks = data.get('tasks')
        session['tasks'] = tasks    


    if form.validate_on_submit():
        
        with open('tasks.txt', 'w') as file:
            data.get('tasks').append(form.task.data)   
            tasks = data.get('tasks')
            session['tasks'] = tasks   
            strData = json.dumps(data)
            file.write(strData)
            
        return redirect(url_for('index'))

    print(session['tasks'])
    return render_template('index.html', form=form, tasks=session['tasks'])




@app.route('/delete/<task>', methods=['DELETE'])
def delete(task):
    print('deleting')
    with open('tasks.txt', 'r') as file:
        data = file.read()
    
    with open('tasks.txt', 'w') as file:
        data = json.loads(data)
        data.get('tasks').remove(task)
        tasks = data.get('tasks')
        session['tasks'] = tasks 
        file.write(json.dumps(data))
    
    return json.dumps(data)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 