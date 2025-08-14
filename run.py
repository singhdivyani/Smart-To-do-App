from  PROJECT_FLASK import create_app,db
from PROJECT_FLASK.models.model import Task 
app=create_app()
with app.app_context():
    db.create_all()
    
    # 🔹 Normalize all task statuses to lowercase
    tasks = Task.query.all()
    for task in tasks:
        if task.status:
            task.status = task.status.strip().lower()
            # if status not in ["pending", "working", "done"]:
            #     status = "pending"  # default if unexpected value
            # task.status = status
    db.session.commit()
    print("✅ All task statuses normalized to lowercase.")
if __name__=="__main__":
    app.run(debug=True)