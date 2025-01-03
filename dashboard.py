from flask import Flask, request, jsonify, render_template, redirect, url_for
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key (replace with your actual key)
openai.api_key = (
    "sk-proj-sLs3tZS6g-"  # First part
    "MaEdFloz93eRkvuxKX8VF9hqFiCisqjLeQEASxmtWm7U-"  # Second part
    "GTFX_Pk4oZIYS4pHY91T3BlbkFJhLqsae1XxUsQBgGs8yZ3dJ_jF1GpTmHxGO8Nn48fjKQWms5KL6KAouwgqHsm5D_zTWyRUAjiMA"  # Third part
)

@app.route("/")
def home():
    return render_template("index.html")  # Ensure templates/index.html exists

@app.route("/run_task", methods=["POST"])
def run_task():
    try:
        # Get the task description from the form input
        task_description = request.form.get("task_description")

        # Validate input
        if not task_description.strip():
            return render_template("error.html", message="Task description cannot be empty!")

        # Generate a response using OpenAI API (Chat Completion)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": task_description}
            ],
            max_tokens=150
        )

        # Return the response
        result = response["choices"][0]["message"]["content"].strip()
        return render_template("result.html", task=task_description, result=result)

    except Exception as e:
        return render_template("error.html", message=str(e))

@app.route("/api/run_task", methods=["POST"])
def api_run_task():
    try:
        # Get JSON input from request
        data = request.json
        task_description = data.get("task_description", "")

        # Validate input
        if not task_description.strip():
            return jsonify({"error": "Task description cannot be empty!"})

        # Generate a response using OpenAI API (Chat Completion)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": task_description}
            ],
            max_tokens=150
        )

        # Return the response as JSON
        result = response["choices"][0]["message"]["content"].strip()
        return jsonify({"task": task_description, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/api/ai_task", methods=["POST"])
def ai_task():
    """
    This endpoint accepts a task description via JSON,
    sends it to OpenAI, and returns the AI-generated result.
    """
    try:
        # Get the task description from the JSON payload
        data = request.json
        task_description = data.get("task_description", "")

        # Validate input
        if not task_description.strip():
            return jsonify({"error": "Task description cannot be empty!"}), 400

        # Send task to OpenAI API (Chat Completion)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": task_description}
            ],
            max_tokens=150
        )

        # Extract AI's response
        result = response["choices"][0]["message"]["content"].strip()

        # Return the result as JSON
        return jsonify({"task": task_description, "result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", message="Page not found!"), 404

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Use port 5001 to avoid conflicts

