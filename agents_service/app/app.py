import time

from flask import Flask, jsonify, request
from agent import create_agent
from session_manager import SessionManager

app = Flask(__name__)

the_agent = create_agent()
ses_manager = SessionManager()


@app.route("/chat", methods=["POST"])
def hello():
    data = request.get_json()
    session_data = ses_manager.get_session(data["session_id"])
    result = the_agent.invoke(
        {
            "messages": [
                *session_data["messages"],
                {"role": "user", "content": data["message"]},
            ]
        }
    )

    ai_message = result["messages"][-1].content
    ses_manager.append_message(data["session_id"], data["message"], "user")
    ses_manager.append_message(data["session_id"], ai_message, "assistant")

    return jsonify({"message": result["messages"][-1].content})


if __name__ == "__main__":
    app.run(port=5000)
