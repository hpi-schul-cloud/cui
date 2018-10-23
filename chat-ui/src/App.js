import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import axios from 'axios'

class App extends Component {

  constructor(props, context) {
    super(props, context);

    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);

    this.state = {
      value: '',
      waitingForResponse: false,
    };

    this.altclicked = false;
    this.currText = '';
  }

  /*
  colorSchemes can be changed here to: 
    "greenGrey"       (= openWHO)
    "orangeGrey"      (= openSAP)
    "lightOrangeGrey" (= openHPI)
  */
  getColorScheme() {
    var colorScheme = "greenGrey";
    return colorScheme.toString();
  }

  /*
  Keywords of the greeting-message can be changed here.
    First: Create a string with the keywords, following the format of "openwhoKeywords".
    Second: Change the string assigned to "keywordsToUse" to your keywords.
  */
  getKeywords() {
    var openwhoKeywords = "-login,-registration,-confirmation email,-enrollment/enroll,-certificate,-video/audio,-subtitles,-modules";
    var openhpiEngKeywords = "-login,-registration,-courses,-tests/homeworks,-certificate"
    var keywordsToUse = openhpiEngKeywords.split(",").join("\n");
    return "\n"+keywordsToUse.toString();
  }

  handleClick() {
    if(!this.altclicked) {
      var list = document.getElementById('curr-conv');
      if (list) {
        list.parentNode.removeChild(list);
        let newElem = document.createElement('div');
        newElem.classList.add('message-box', 'answer', this.getColorScheme());
        newElem.innerHTML = this.currText;
        document.getElementById('conversation').appendChild(newElem);
      }
    }
    this.altclicked = false;
    const val = this.state.value;
    this.setState({
      value: '',
      waitingForResponse: true,
    });
    this.addQuestionToConversation(val);
    axios.get('http://localhost:5005/conversations/default/respond?q=' + val)
      .then(response => {
        this.addAnswerToConversation(response.data.responses);
        if (response.data.confidence < 0.2) {
          this.addAlternativesToConversation(response.data.alternatives);
        }
        const convElem = document.getElementById("conversation")
        convElem.scrollTo(0, convElem.scrollHeight);
      })
      .finally(() => {
        this.setState({ waitingForResponse: false });
        document.getElementsByClassName('Question-Box ' + this.getColorScheme())[0].focus();
      });
  }

  addAnswerToConversation(answers) {
    answers.forEach((answer) => {
        let newElem = document.createElement('div');
        newElem.classList.add('message-box', 'answer', this.getColorScheme());
        newElem.innerHTML = answer.text.trim();
        document.getElementById('conversation').appendChild(newElem);
        this.currText = answer.text.trim();
    })
  }

  removeIntentsFromChat() {
    let alternativeElems = document.getElementsByClassName('alternative');
    while (alternativeElems[0]) {
      alternativeElems[0].parentNode.removeChild(alternativeElems[0]);
    }
  }

  removeLastAnswersFromChat() {
    let convElem = document.getElementById('conversation');
    while (convElem.childNodes[convElem.childNodes.length - 1]) {
      const elem = convElem.childNodes[convElem.children.length - 1];
      if (elem.nodeType === Node.ELEMENT_NODE && elem.className.includes('answer')) {
        convElem.removeChild(elem);
      } else {
        break;
      }
    }
  }

  addAlternativesToConversation(alternatives) {
    let newElem = document.createElement('div');
    newElem.classList.add('message-box', 'alternative', 'alternative-intro');
    newElem.innerHTML = 'Not the answer you were looking for? Maybe one of the following can help:';
    document.getElementById('conversation').appendChild(newElem);
    alternatives.forEach((alternative) => {
      const intent = alternative['intent']['name'];
      const text = alternative['question'];
      let newElem = document.createElement('div');
      newElem.classList.add('message-box', 'alternative');
      newElem.innerHTML = text.trim();
      newElem.addEventListener('click', () => this.changeCurrentIntent(intent, text))
      document.getElementById('conversation').appendChild(newElem);
    })
  }

  changeCurrentIntent(intent) {
    this.altclicked = true;
    axios.get('http://localhost:5005/conversations/default/tracker/reset_intent?intent=' + intent)
      .then(response => {
        this.removeIntentsFromChat();
        this.removeLastAnswersFromChat();
        this.addAnswerToConversation(response.data.responses);
      })
  }

  addQuestionToConversation(question) {
    this.removeIntentsFromChat();
    let newElem = document.createElement('div');
    newElem.classList.add('message-box', 'question', this.getColorScheme());
    newElem.innerHTML = question.trim();
    document.getElementById('conversation').appendChild(newElem);
  }

  handleChange(e) {
    this.setState({ value: e.target.value });
  }

  render() {
    return (
      <div className="chat-ui">
        <div id="conversation">
           <div className={'message-box '+ 'answer '+ this.getColorScheme()}>Hello, I am your Helpdesk-Assistant. Please describe your problem or choose from these keywords:{this.getKeywords()}</div>
        </div>
        <form>
          <form
            className="form-group"
            controlId="formBasicText"
            onKeyPress={event => {
              if (event.key === "Enter") {
                this.handleClick();
                event.preventDefault();
              }
            }}
          >
            <input
              type="text"
              value={this.state.value}
              placeholder="Write message"
              className={"Question-Box " + this.getColorScheme()}
              onChange={this.handleChange}
              autoComplete="off"
              disabled={this.state.waitingForResponse}
            />
            <button type="button" onClick={this.handleClick} className={'btn-send ' + this.getColorScheme()}> <img src="/assets/send.png"/> </button>
          </form>
        </form>
      </div>
    );
  }
}

export default App;
