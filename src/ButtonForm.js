import React from 'react';

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

export default ButtonForm;
