import React from 'react';

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

export default InputForm;
