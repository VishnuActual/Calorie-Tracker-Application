
from datetime import datetime

from flask import make_response
from flaskblog.calories.utils import * 
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import db 
from flaskblog.calories.forms import CalorieForm
from flaskblog.models import Calorie 
from flask_login import  current_user, login_required

from flask import Blueprint


calories = Blueprint('calories',__name__) 


# @login_required
@calories.route("/")
@calories.route("/home")
@login_required 
def home():
    page = request.args.get('page', 1, type=int)
    
    logs = Calorie.query \
        .filter_by(user_id=current_user.id) \
        .order_by(Calorie.date_posted.desc()) \
        .paginate(page=page, per_page=7) 
    print(logs.items)
    print("*************************************************")
    ans = weekly_csv(logs.items)  

    

    return render_template("home.html", logs=logs)


@calories.route("/about")
def about():
    return render_template('about.html', title='About')



@calories.route("/calorie/new", methods=['GET', 'POST'])
@login_required
def new_calorie():
    form = CalorieForm()
    if form.validate_on_submit():
        date_posted = datetime.combine(form.date_posted.data, datetime.min.time())
        calorie = Calorie(breakfast=form.breakfast.data,
                          lunch=form.lunch.data,
                          dinner=form.dinner.data,
                          snacks=form.snacks.data,
                          date_posted=date_posted,  # Use datetime.now() to get current date and time
                          user_id=current_user.id)
        db.session.add(calorie)
        db.session.commit()
        flash('Your calorie intake has been recorded!', 'success')
        return redirect(url_for('calories.home'))
    return render_template('create_calorie.html', title='New Calorie', form=form)


@calories.route("/calorie/<int:calorie_id>")
def calorie(calorie_id):
    calorie = Calorie.query.get_or_404(calorie_id)
    return render_template('calorie.html',calorie=calorie)


@calories.route("/calorie/<int:calorie_id>/update", methods=['GET', 'POST'])
@login_required
def update_calorie(calorie_id):
    calorie = Calorie.query.get_or_404(calorie_id)
    if calorie.user_id != current_user.id:
        abort(403)
    form = CalorieForm()
    if form.validate_on_submit():
        date_posted = datetime.combine(form.date_posted.data, datetime.min.time())
        calorie.date_posted=date_posted 
        calorie.breakfast = form.breakfast.data
        calorie.lunch=form.lunch.data 
        calorie.dinner=form.dinner.data 
        calorie.snacks=form.snacks.data 
        
        calorie.user_id = current_user.id 

        db.session.commit()
        flash('Your Calorie has been updated!', 'success')
        return redirect(url_for('calories.calorie', calorie_id=calorie.id))

    elif request.method == 'GET':
        form.date_posted.data = calorie.date_posted 
        form.breakfast.data = calorie.breakfast
        form.lunch.data = calorie.lunch
        form.dinner.data = calorie.dinner
        form.snacks.data = calorie.snacks 
    return render_template('create_calorie.html', title='Update Calorie',
                           form=form, legend='Update Calorie')


@calories.route("/calorie/<int:calorie_id>/delete", methods=['POST'])
@login_required
def delete_calorie(calorie_id):
    calorie = Calorie.query.get_or_404(calorie_id)
    if calorie.author != current_user:
        abort(403)
    db.session.delete(calorie)
    db.session.commit()
    flash('Your Calorie has been deleted!', 'success')
    return redirect(url_for('calories.home'))




@login_required
@calories.route('/download_csv', methods=['GET'])
def download_csv():
    logs = Calorie.query \
        .filter_by(user_id=current_user.id) \
        .order_by(Calorie.date_posted.desc()) 
    csv_data = generate_csv(logs)
    response = make_response(csv_data.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=calorie_logs.csv"
    response.headers["Content-Type"] = "text/csv"
    return response
