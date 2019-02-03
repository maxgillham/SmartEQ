import React from 'react'
import './infocard.css'

import happyFace from './images/happy-icon.png' 
import angryFace from './images/angry-icon.png' 
import contemptFace from './images/contempt-icon.png' 
import disgustedFace from './images/disgusted-icon.png' 
import fearFace from './images/fear-icon.png' 
import neutralFace from './images/neutral-icon.png' 
import sadFace from './images/sad-icon.png' 
import surpriseFace from './images/happy-icon.png' 
import questionMark from './images/question-mark.png'

let emojiLookupObj = {
  'angry': angryFace,
  'happiness': happyFace,
  'contempt': contemptFace,
  'disgust': disgustedFace,
  'fear': fearFace,
  'neutral': neutralFace,
  'sadness': sadFace,
  'surprise': surpriseFace
}

class InformationCard extends React.Component {

  processSpeechData = (speechData) => {
    let speechObj = {}
    if(speechData < 0.20) {
      speechObj.happiness = 'Very Unhappy'
      speechObj.emoji = sadFace
    }
    if(speechData >= 0.20 && speechData < 0.40) {
      speechObj.happiness = 'Unhappy'
      speechObj.emoji = sadFace
    }
    if(speechData >= 0.40 && speechData < 0.60) {
      speechObj.happiness = 'Neutral'
      speechObj.emoji = neutralFace
    }
    if(speechData >= 0.60 && speechData < 0.80) {
      speechObj.happiness = 'Happy'
      speechObj.emoji = happyFace
    }
    if(speechData >= 0.80 && speechData <= 1) {
      speechObj.happiness = 'Very Happy'
      speechObj.emoji = happyFace
    }

    return speechObj
  }

  render() {
    let { imageData, speechData } = this.props
    let imageAnalysisString = '-'
    
    if(imageData['Emotion'] && imageData['Value']) {
      imageAnalysisString = imageData['Emotion'] + ' ' + imageData['Value']*100 + '%';
      imageAnalysisString = imageAnalysisString.charAt(0).toUpperCase() + imageAnalysisString.slice(1);
    }

    let speechAnalysis = {
      happiness: '-'
    }

    if(speechData) {
      speechAnalysis = this.processSpeechData(speechData);
    }
    
    return (
      <div className="container">
        <div className="inner-class">

            <h2>Image Analysis</h2>
            <p><img src={emojiLookupObj[imageData['Emotion']] || questionMark} height="18" width="18"/> {imageAnalysisString}</p>

            <h2>Conversation Analysis</h2>
            <p><img src={speechAnalysis.emoji || questionMark} height="18" width="18"/> {speechAnalysis.happiness || '-'}</p>
        </div>
        

      </div>
    );
  };
    
    
}

export default InformationCard