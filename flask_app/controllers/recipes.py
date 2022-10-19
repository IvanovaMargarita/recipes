from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_recipe.html',user=User.get_by_id())

@app.route('/create/recipe',methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "under_30": int(request.form['under_30']),
        "date_made": request.form['date_made'],
        "user_id": session['user_id']
    }
    Recipe.save(data)
    return redirect('/dashboard')


@app.route('/edit/recipe/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html", edit=Recipe.get_one(data), user= User.get_by_id(user_data))


@app.route('/update/recipe', methods=['POST'])
def update():
    if 'user_id' not in session:
        return redirect('logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/new/recipe')
    data = {
        "name": request.form['name'],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "under_30": int(request.form["under_30"]),
        "date_made": request.form["date_made"],
        "id": session["id"]
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipe/<int:id>')
def show_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    user_data={
        "id": session['user_id']
    }
    return render_template("recipe.html", user=User.get_by_id(user_data), recipe=Recipe.get_one(data))

@app.route('/destroy/recipe/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')