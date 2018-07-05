import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Button, FormGroup, FormControl, HelpBlock } from 'react-bootstrap';
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
      if(list){
        list.parentNode.removeChild(list);
        let newElem = document.createElement('div');
        newElem.classList.add('answer');
        newElem.innerHTML = this.currText;
        document.getElementById('conversation').appendChild(newElem);
      }
    }
    this.altclicked = false;
    const val = this.state.value;
    this.setState({ value: '' });
    this.addQuestionToConversation(val);
    var currentConv = document.createElement('div');
    currentConv.id = 'curr-conv';
    document.getElementById('conversation').appendChild(currentConv);
    axios.get('http://localhost:5005/conversations/default/respond?q=' + val)
      .then(response => {
        this.addAnswerToConversation(response.data.responses);
        this.addAlternativesToConversation(response.data.alternatives);
      })
  }

  addAnswerToConversation(answers) {
    answers.forEach((answer) => {
        let newElem = document.createElement('div');
        newElem.classList.add('answer');
        newElem.innerHTML = answer.text.trim();
        document.getElementById('curr-conv').appendChild(newElem);
        this.currText = answer.text.trim();
    })
  }

  removeIntentsFromChat(text){
    var list = document.getElementById('curr-conv');
    list.parentNode.removeChild(list);
    let newElem = document.createElement('div');
    newElem.classList.add('answer');
    newElem.innerHTML = text;
    document.getElementById('conversation').appendChild(newElem);
  }

  addAlternativesToConversation(alternatives) {
    let newElem = document.createElement('div');
    newElem.classList.add('answer');
    newElem.innerHTML = 'Or did you mean? :';
    document.getElementById('curr-conv').appendChild(newElem);
    alternatives.forEach((alternative) => {
      const intent = alternative['intent']['name'];
      const text = alternative['responses'][0].text;
      let newElem = document.createElement('div');
      newElem.classList.add('answer');
      newElem.innerHTML = text.trim();
      newElem.addEventListener('click', () => this.changeCurrentIntent(intent, text))
      document.getElementById('curr-conv').appendChild(newElem);
    })
  }

  changeCurrentIntent(intent, text) {
    this.altclicked = true;
    this.removeIntentsFromChat(text);
    axios.get('http://localhost:5005/conversations/default/tracker/reset_intent?intent=' + intent)
      .then(response => console.log(response))
  }

  addQuestionToConversation(question) {
    let newElem = document.createElement('div');
    newElem.classList.add('question');
    newElem.innerHTML = question.trim();
    document.getElementById('conversation').appendChild(newElem);
  }

  handleChange(e) {
    this.setState({ value: e.target.value });
  }

  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to a Conversational UI Experiment</h1>
        </header>
        <div id="conversation">

        </div>
        <form className="App-intro">
          <FormGroup
            controlId="formBasicText"
            onKeyPress={event => {
              if (event.key === "Enter") {
                this.handleClick();
                event.preventDefault();
              }
            }}
          >
            {/* <HelpBlock>Enter any question you have!</HelpBlock> */}
            <FormControl
              type="text"
              value={this.state.value}
              placeholder="Enter Question"
              className="Question-Box"
              onChange={this.handleChange}
              autoComplete="off"
            />
          </FormGroup>
          <Button onClick={this.handleClick} bsStyle="primary">Submit</Button>
        </form>
      </div>
    );
  }
}

export default App;
