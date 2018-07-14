import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Button, FormGroup, FormControl } from 'react-bootstrap';
import axios from 'axios'

class App extends Component {

  constructor(props, context) {
    super(props, context);

    this.handleClick = this.handleClick.bind(this);
    this.handleChange = this.handleChange.bind(this);

    this.state = {
      value: ''
    };

    this.altclicked = false;
    this.currText = '';
  }

  handleClick() {
    if(!this.altclicked) {
      var list = document.getElementById('curr-conv');
      if (list) {
        list.parentNode.removeChild(list);
        let newElem = document.createElement('div');
        newElem.classList.add('message-box', 'answer');
        newElem.innerHTML = this.currText;
        document.getElementById('conversation').appendChild(newElem);
      }
    }
    this.altclicked = false;
    const val = this.state.value;
    this.setState({ value: '' });
    this.addQuestionToConversation(val);
    axios.get('http://localhost:5005/conversations/default/respond?q=' + val)
      .then(response => {
        this.addAnswerToConversation(response.data.responses);
        if (response.data.confidence < 0.3) {
          this.addAlternativesToConversation(response.data.alternatives);
        }
        const convElem = document.getElementById("conversation")
        convElem.scrollTo(0, convElem.scrollHeight);
      })
  }

  addAnswerToConversation(answers) {
    answers.forEach((answer) => {
        let newElem = document.createElement('div');
        newElem.classList.add('message-box', 'answer');
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
    newElem.classList.add('message-box', 'alternative');
    newElem.innerHTML = 'Or did you mean one of the following?';
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
    let newElem = document.createElement('div');
    newElem.classList.add('message-box', 'question');
    newElem.innerHTML = question.trim();
    document.getElementById('conversation').appendChild(newElem);
  }

  handleChange(e) {
    this.setState({ value: e.target.value });
  }

  render() {
    return (
      <div className="chat-ui">
        <div id="conversation"></div>
        <form>
          <FormGroup
            className="form-group"
            controlId="formBasicText"
            onKeyPress={event => {
              if (event.key === "Enter") {
                this.handleClick();
                event.preventDefault();
              }
            }}
          >
            <FormControl
              type="text"
              value={this.state.value}
              placeholder="Write message"
              className="Question-Box"
              onChange={this.handleChange}
              autoComplete="off"
            />
            <Button onClick={this.handleClick} bsStyle="primary" className="btn-send"><img src="/assets/send.png" /></Button>
          </FormGroup>
        </form>
      </div>
    );
  }
}

export default App;
