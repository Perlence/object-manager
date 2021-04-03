import { getObject, freeObject } from './api';
import ButtonForm from './ButtonForm';
import InputForm from './InputForm';

function App() {
  return (
    <>
      <ButtonForm name="Get" onSubmit={getObject} />
      <InputForm name="Free" onSubmit={freeObject} />
    </>
  );
}

export default App;
