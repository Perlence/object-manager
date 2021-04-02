import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';

function main() {
  ReactDOM.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>,
    document.getElementById('root'),
  );
}

function App() {
  return (
    <>
      <InputForm name="Put" onSubmit={putObject} />
      <ButtonForm name="Get" onSubmit={getObject} />
      <InputForm name="Free" onSubmit={freeObject} />
      <InputForm name="Drop" onSubmit={dropObject} />
    </>
  );
}

class InputForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
      error: '',
      result: '',
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({ value: event.target.value });
  }

  async handleSubmit(event) {
    event.preventDefault();
    if (typeof this.props.onSubmit === 'function') {
      try {
        const result = await this.props.onSubmit(this.state.value);
        this.setState({
          error: '',
          result,
        });
      } catch (err) {
        this.setState({
          error: err.message,
          result: '',
        });
      }
    }
  }

  render() {
    return (
      <form id={this.props.name.toLowerCase()} onSubmit={this.handleSubmit}>
        <fieldset>
          <legend>{this.props.name} Object</legend>
          <input type="text" value={this.state.value} onChange={this.handleChange} />
          <input type="submit" value={this.props.name} disabled={!this.state.value} />
          {this.state.error && (
            <div>
              Error: {this.state.error}
            </div>
          )}
          {this.state.result && (
            <div>
              {this.state.result}
            </div>
          )}
        </fieldset>
      </form>
    );
  }
}

class ButtonForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: '',
      result: '',
    };
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  async handleSubmit(event) {
    event.preventDefault();
    if (typeof this.props.onSubmit === 'function') {
      try {
        const result = await this.props.onSubmit();
        this.setState({
          error: '',
          result,
        });
      } catch (err) {
        this.setState({
          error: err.message,
          result: '',
        });
      }
    }
  }

  render() {
    return (
      <form id={this.props.name.toLowerCase()} onSubmit={this.handleSubmit}>
        <fieldset>
          <legend>{this.props.name} Object</legend>
          <input type="submit" value={this.props.name} />
          {this.state.error && (
            <div>
              Error: {this.state.error}
            </div>
          )}
          {this.state.result && (
            <div>
              {this.state.result}
            </div>
          )}
        </fieldset>
      </form>
    );
  }
}

async function putObject(value, acquire = false) {
  const resp = await window.fetch(
    '/objects',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ object: Number(value), acquired: acquire }),
    },
  );

  if (!resp.ok) {
    return responseError(await resp.text());
  } else if (resp.status === 201) {
    return `Put ${value} into the pool`;
  } else if (resp.status === 200) {
    return `Object ${value} is already in the pool`;
  }
}

async function getObject() {
  const resp = await window.fetch('/objects/get', { method: 'POST' });

  if (!resp.ok) {
    return responseError(await resp.text());
  }

  const obj = await resp.json();
  return `Got object ${obj.object}`;
}

async function freeObject(value) {
  const resp = await window.fetch(
    `/objects/${value}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ acquired: false }),
    },
  );
  if (!resp.ok) {
    return responseError(await resp.text());
  }
  return `Freed object ${value}`;
}

async function dropObject(value) {
  const resp = await window.fetch(`/objects/${value}`, { method: 'DELETE' });
  if (resp.status === 404) {
    return `There's no object ${value} in the pool`;
  } else if (!resp.ok) {
    return responseError(await resp.text());
  } else {
    return `Removed object ${value} from the pool`;
  }
}

function responseError(respText) {
  let errorObj;
  try {
    errorObj = JSON.parse(respText);
  } catch (e) {
    throw new Error(respText);
  }
  throw new Error(errorObj.error);
}

main();
