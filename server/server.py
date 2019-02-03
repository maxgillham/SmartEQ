from flask import *
from flask_socketio import SocketIO, emit
import utils
from utils import *
import os
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'QHacks2019!'
socketio = SocketIO(app)

sent_rating = SentimentRating();

# print Benji is fun
@socketio.on('predictions', namespace='/test')
def send_message(message):
  emit('predictions', message)

@socketio.on('speech', namespace='/test')
def recieve_speech(speech):
  result = start_mic(sent_rating)
  emit('predictions', result)

@socketio.on('video', namespace='/test')
def recieve_message(message):
  f = open("./img/download.jpeg", "wb")
  f.write(message)
  f.close()
  result = utils.get_emotion('./img/download.jpeg')
  emit('predictions', result)
# You found it
@socketio.on('connect', namespace='/test')
def test_connect():
  emit('connect', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
  print('Client disconnected')

if __name__ == "__main__":
  app.run()
