import React from 'react'
import Webcam from 'react-webcam'

import './style.css'

const convertBase64ToFile = function (image) {
  const byteString = atob(image.split(',')[1]);
  const ab = new ArrayBuffer(byteString.length);
  const ia = new Uint8Array(ab);
  for (let i = 0; i < byteString.length; i += 1) {
    ia[i] = byteString.charCodeAt(i);
  }
  const newBlob = new Blob([ab], {
    type: 'image/jpeg',
  });
  return newBlob;
};

class WebcamCapture extends React.Component {
  
  setRef = webcam => {
    this.webcam = webcam
  }

  capture = () => {
    const imageSrc = this.webcam.getScreenshot()
    this.props.sendImage(convertBase64ToFile(imageSrc))
  }

  componentDidUpdate() {
    if(this.props.sendData) {
      this.capture()
    }
  }

  render() {
    const videoConstraints = {
      width: 1280,
      height: 720,
      facingMode: "user"
    }
    return (
      <div>
        <Webcam
          audio={false}
          height={window.innerHeight - 100}
          ref={this.setRef}
          screenshotFormat="image/jpeg"
          width={window.innerWidth}
          videoConstraints={videoConstraints}
        />
        <button className="start-button" onClick={this.capture}>Start</button>
      </div>
    );
  }
}

export default WebcamCapture