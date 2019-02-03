import React, { Component } from 'react';
import { subscribeToSocket, sendImageToSocket, sendSpeechToSocket } from './sockets'
import { InformationCard, WebCamera } from './components'
import './App.css';

class App extends Component {

  constructor(props) {
    super(props)

    this.state = {
      imageData: {},
      speechData: ''
    }

    subscribeToSocket((err,response)=>{

      if(typeof(response) === "object") {
        this.setState({
          imageData: response
        })
      } else if(typeof(response) === "number") {
        this.setState({
          speechData: response
        })
      }

      this.setState({
        sendData: true
      })
    })
  }

  screenCap = (data) => {
    sendImageToSocket(data)
    sendSpeechToSocket()
    this.setState({
      sendData: false
    })
  }

  render() {
    return (
      <div>
        <WebCamera sendImage={this.screenCap} sendData={this.state.sendData}/>
        <InformationCard imageData={this.state.imageData} speechData={this.state.speechData}/>
      </div>
    );
  }
}

export default App;
