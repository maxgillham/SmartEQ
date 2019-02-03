import openSocket from 'socket.io-client'

const socket = openSocket('http://localhost:5000/test');

function subscribeToSocket(cb) {
  socket.emit('connect', 'Connected')
  socket.on('predictions', response => cb(null, response))
}

function sendImageToSocket(data) {
  socket.emit('video', data)
}

function sendSpeechToSocket() {
  socket.emit('speech', 'Start Mic')
}

export {
  subscribeToSocket,
  sendImageToSocket,
  sendSpeechToSocket
}