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
        "title": "flask",
        "completed": False
    }
]

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Root path to server, this endpoint is called for that"
    })

@app.route("/tasks", methods=["GET"])
def get_tasks():

    completed = request.args.get("completed")
    title = request.args.get("title")
    res = tasks

    if completed:
        if completed.lower() not in ["true", "false"]:
            return jsonify({
                "error": "Invalid value for 'completed' parameter. Use 'true' or 'false'."
            }), 400

        completed_bool = completed.lower() == "true"
        res = [task for task in res if task["completed"] == completed_bool]

    if title:
        res = [task for task in res if task['title'] == title]

    return jsonify({
        "tasks": res
    })

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):

    for task in tasks:

        if task["id"] == task_id:
            return jsonify(task)

        
    return jsonify({
        "error": "Task not found"
    }), 404 

@app.route("/tasks", methods=["POST"])
def create_task():

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "JSON body is required"
        }), 400

    if "title" not in data:
        return jsonify({
            "error": "Missing 'title' in request data"  
    }), 400

    if not isinstance(data["title"], str):
        return jsonify({
            "error": "title must be a string"
    }), 400

    if data["title"].strip() == "":
        return jsonify({
            "error": "title cannot be empty"
    }), 400

    completed = data.get("completed", False)

    if not isinstance(completed, bool):
        return jsonify({
            "error": "completed must be a boolean"
    }), 400


    new_task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "completed": completed
    }

    tasks.append(new_task)

    return jsonify(new_task), 201
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)

            return jsonify({
                "message": "Task deleted"
            }), 200

    return jsonify({
        "error": "Task not found"
    }), 404

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):

    data = request.get_json(silent=True)

    if "title" not in data or "completed" not in data:
        return jsonify({
            "error": "title and completed are required"
        }), 400
    for task in tasks:
        if task["id"] == task_id:

            task["title"] = data["title"]
            task["completed"] = data["completed"]

            return jsonify(task), 200
    return jsonify({
        "error": "Task not found"
    }), 404

@app.route("/tasks/<int:task_id>", methods=["PATCH"])
def patch_task(task_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "No data provided"
        }), 400

    for task in tasks:
        if task["id"] == task_id:

            if "title" in data:
                task["title"] = data["title"]
            if "completed" in data:
                task["completed"] = data["completed"]

            return jsonify(task), 200

    return jsonify({
        "error": "Task not found"
    }), 404





if __name__ == "__main__":
    #refreshes application whenever changes are made in code, allowing the changes to be reflected right away.
    #When there are errors, it gives more detailed error messages in the console, which can help with debugging.
    #Needs to be turned off when pushiong to prod
    app.run(debug=True)