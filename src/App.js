import { putObject, getObject, freeObject, dropObject } from './api';
import ButtonForm from './ButtonForm';
import InputForm from './InputForm';

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

export default App;
