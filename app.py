from flask import Flask, jsonify, request

app = Flask(__name__) 

tasks = [
    {
        "id": 1,
        "title": "Learn Flask",
        "completed": False
    },
    {
        "id": 2,
        "title": "Practice REST APIs",
        "completed": True
    }
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Root path to server, this endpoint is called for that"
    })

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({
        "tasks": tasks
    })

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):

    for task in tasks:

        if task["id"] == task_id:
            return jsonify(task)

        
    return jsonify({
        "error": "Task not found"
    }), 404 


if __name__ == "__main__":
    #refreshes application whenever changes are made in code, allowing the changes to be reflected right away.
    #When there are errors, it gives more detailed error messages in the console, which can help with debugging.
    #Needs to be turned off when pushiong to prod
    app.run(debug=True)