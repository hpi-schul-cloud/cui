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
  }

  handleClick() {
    const val = this.state.value;
    this.setState({ value: '' });
    this.addQuestionToConversation(val);
    axios.get('http://localhost:5005/conversations/default/respond?q=' + val)
      .then(response => this.addAnswerToConversation(response.data))
  }

  addAnswerToConversation(answers) {
    console.log(answers);
    answers.forEach((answer, index) => {
      setTimeout( () => {
        let newElem = document.createElement('div');
        newElem.classList.add('answer');
        newElem.innerHTML = answer.text.trim();
        document.getElementById('conversation').appendChild(newElem);
      }, 500);
    })
  }

  sentDelayedAnswer(){
    
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
