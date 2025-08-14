# add,view ,update ,delete logic
from flask import Blueprint,request,redirect,url_for,session,render_template,flash
from PROJECT_FLASK import db
from PROJECT_FLASK.models.model import Task

task_bp=Blueprint('tasks',__name__)
@task_bp.route('/')
def view_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    tasks=Task.query.filter_by(user_id=session['user_id']).all()
    # render tasks.html to shoe all tasks
    return render_template('tasks.html',tasks=tasks)


@task_bp.route('/add',methods=["POST"])
def add_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    task_name=request.form.get('task_name')
    if task_name :
        new_task=Task(task_name=task_name,status="Pending",user_id=session['user_id'])
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully','success')
    return  redirect(url_for('tasks.view_task'))
@task_bp.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    if task.status == 'Pending':
        task.status = 'Working'
    elif task.status == 'Working':
        task.status = 'Done'
    else:
        task.status = 'Pending'
    db.session.commit()
    flash(f"Task status updated to {task.status}")
    return redirect(url_for('tasks.view_task'))


# @task_bp.route('/set_status/<int:task_id>/<string:new_status>', methods=["POST"])
# def set_status(task_id, new_status):
#     """Set a task's status directly to a given value."""
#     allowed_statuses = ["pending", "working", "done"]
#     if 'user_id' not in session:
#         return redirect(url_for('auth.login'))
    
#     task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
#     if task and new_status in allowed_statuses:
#         task.status = new_status
#         db.session.commit()
#         flash(f"Task status updated to {new_status.title()}", "info")
#     else:
#         flash("Task not found or you don't have permission to change it.", "danger")
#     return redirect(url_for('tasks.view_task'))


@task_bp.route('/edit/<int:task_id>', methods=["POST"])
def edit_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    new_name = request.form.get('task_name')
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if task and new_name:
        task.task_name = new_name.strip()
        db.session.commit()
        flash("Task updated successfully", "success")
    return redirect(url_for('tasks.view_task'))

@task_bp.route('/delete/<int:task_id>', methods=["POST"])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully", "info")
    return redirect(url_for('tasks.view_task'))


@task_bp.route('/toggle/<int:task_id>', methods=["POST"])
def toggle_status(task_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
    if task:
        status = (task.status or "").strip().lower()
        if status == "pending":
            task.status = "Working"
        elif status == "working":
            task.status = "Done"
        elif status == "done":
            task.status = "Pending"
        else:
            task.status = "Pending"
        db.session.commit()
        flash(f"Task status updated to {task.status}", "info")
    return redirect(url_for('tasks.view_task'))


# @task_bp.route('/toggle/<int:task_id>', methods=["POST"])
# def toggle_status(task_id):
#     task = Task.query.get(task_id)
#     if task:
#         # Normalize the value: remove spaces and make lowercase
#         current_status = (task.status or "").strip().lower()

#         if current_status == "pending":
#             task.status = "working"
#         elif current_status == "working":
#             task.status = "done"
#         elif current_status == "done":
#             task.status = "pending"
#         else:
#             # If something unexpected is stored, default to Pending
#             task.status = "pending"

#         db.session.commit()
#     return redirect(url_for('tasks.view_task'))


# @task_bp.route('/Toggle/<int:task_id>',methods=["POST"])
# def toggle_status(task_id):
#     task=Task.query.get(task_id)
#     if task:
#         status = task.status.strip().lower()
#         if status == "pending":
#             task.status = "Working"
#         elif status == "working":
#             task.status = "Done"
#         elif status == "done":
#             task.status = "Pending"
#         print(task.status)
#         db.session.commit()
#     return redirect(url_for('tasks.view_task'))
@task_bp.route('/clear',methods=["POST"])
def clear_task():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    Task.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash('All tasks cleared!', 'info')
    return redirect(url_for('tasks.view_task'))
    # db.query(Task).delete()
    # db.session.commit()
    # flash('All task cleared!','info')
    # return redirect(url_for('tasks.view_task'))

