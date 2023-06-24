#to test 
from flask import Flask, Response
from pyngrok import ngrok
import time

app = Flask(__name__)

@app.route('/domain')
def data():
    def generate():
        while(True):
            with open('data.txt', 'r') as f:
                for line in f:
                    print("sent:",line)
                    yield f"{line}\n\n"
                    time.sleep(5)
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Start the Flask app on port 8082
    app.run(port=8082)