import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from transformers import pipeline
from gradio_client import Client
import requests

#client = Client("https://mosaicml-mpt-7b-chat--thv27.hf.space/")


def generate_text(text):
    ans = "Server Error"

    response = requests.post("https://tloen-alpaca-lora.hf.space/run/predict", json={
        "data": [
            text,
            "Explain this code to me : ",
            0,
            0.75,
            40,
            4,
            300,
        ]
    }).json()
    if "data" not in response:
        return ans
    data = response['data'][0]
    print(data)
    ans = f"Output : {data}"
    return ans


app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/explain_code")
def handle_explain_code(ack, body, logger):
    ack()
    text = " ".join(body["text"].split()[1:])
    if not text.strip():
        return "Please provide some text to explain."
    generated_text = generate_text(text)
    response = f"Explanation for '{text}':\n{generated_text}"
    return response

@app.event("message")
def handle_message(event, say):
    text = event["text"]
    if not text.strip():
        say("Please provide some text to explain.")
        return
    generated_text = generate_text(text)
    say(generated_text)


handler = SocketModeHandler(app_token=os.environ["SLACK_APP_TOKEN"], app=app)
handler.start()
