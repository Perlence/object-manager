import React from 'react';
import { listObjects, getObject, freeObject } from './api';
import ButtonForm from './ButtonForm';
import ObjectManagerList from './ObjectManagerList';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      objects: [],
      objectsError: '',
    };
    this.refreshObjects = this.refreshObjects.bind(this);
  }

  componentDidMount() {
    this.refreshObjects();
  }

  async refreshObjects() {
    let newObjects;
    try {
      newObjects = await listObjects();
    } catch (err) {
      this.setState({
        objects: [],
        objectsError: err.message,
      })
      return;
    }
    this.setState({
      objects: newObjects,
      objectsError: '',
    });
  }

  render() {
    return (
      <>
        {this.state.objectsError
          ? <div>Error listing objects: {this.state.objectsError}</div>
          : <ObjectManagerList
              objects={this.state.objects}
              freeObject={async (value) => {
                try {
                  return await freeObject(value);
                } finally {
                  await this.refreshObjects();
                }
              }}
            />
        }
        <ButtonForm
          name="Get"
          onSubmit={async () => {
            try {
              return await getObject();
            } finally {
              await this.refreshObjects();
            }
          }}
        />
      </>
    );
  }
}

export default App;
