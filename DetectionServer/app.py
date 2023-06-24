import pickle
import threading
from flask import Flask, render_template, request, jsonify , Response
from flask_socketio import SocketIO, emit
import numpy as np
import preprocessInput
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import requests
import time


# Load the trained model from a pickle file
with open('XGBoost/xgboost_model_v3-93.pkl','rb') as file:
    xgb_model = pickle.load(file)

def predict(domain):
        domainName = str(domain)
        # Preprocess the domain name
        preprocessed_domain = preprocessInput.preprocess_input(domainName)
        # Make the prediction using the saved model
        predictionl = xgb_model.predict(preprocessed_domain)
        return predictionl


# Create the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'project'
socketio = SocketIO(app)

result = {}

@app.route('/')
def index():
    return render_template('index.html')

###start part 1
def handle_part1():
    global result
    url = 'http://192.168.35.100:8082/receive_dns_packets'
    #url = 'http://127.0.0.1:8082/domain'
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        print("Successfully connected to the SSE server.")
        for line in response.iter_lines():
            if line:
                try:
                    data = line.decode('utf-8')
                    print('Received data:', data)
                    ip_address , domain = data.split(',')
                    if domain.endswith('.'): domain = domain[:-1]  # Remove the last character (dot)
                    prediction_class = 'benign'
                    prediction = predict(domain)
                    prediction_class = "benign" if prediction == 0 else "malicious"
                    result = {'domain': domain, 'ip_address': ip_address, 'prediction_class': prediction_class}
                    print("The result is:", result)
                    socketio.emit('update_result', result)  # Emit the result to clients
                except Exception as e:
                    print("Error occurred while processing SSE event:", e)
    else:
        print('Failed to connect to the SSE server.')
###end part 1

@socketio.on('connect')
def on_connect():
    print("Client connected successfully")
    socketio.emit('update_result', result)  # Emit the result to clients

# Start Part 1 in a separate thread
part1_thread = threading.Thread(target=handle_part1)
part1_thread.start()

# Run the application
if __name__ == '__main__':
    socketio.run(app, debug=False)