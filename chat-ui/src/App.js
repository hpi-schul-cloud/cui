import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import { Button, FormGroup, FormControl, HelpBlock, ControlLabel } from 'react-bootstrap';
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
    console.log(this.state.value);
    axios.get('http://localhost:5005/conversations/default/respond?q=hello')
      .then(response => console.log(response))
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
        <form className="App-intro">
          <FormGroup
            controlId="formBasicText"
            
          >
            <HelpBlock>Enter any question you have to you openSAP Account!</HelpBlock>
            <FormControl
              type="text"
              value={this.state.value}
              placeholder="Enter Question"
              className="Question-Box"
              onChange={this.handleChange}
            />
          </FormGroup>
          <Button onClick={this.handleClick} bsStyle="primary">Submit</Button>
        </form>
      </div>
    );
  }
}

export default App;
