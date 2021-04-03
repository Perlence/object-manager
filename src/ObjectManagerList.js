import React from 'react';

function ObjectManagerList({ objects, freeObject }) {
  const available = [];
  const acquired = [];
  objects.forEach(obj => {
    if (obj.acquired) {
      acquired.push(obj);
    } else {
      available.push(obj);
    }
  });

  return (
    <div>
      <div className="ObjectManagerList-available">
        Available objects:
        <ul>
          {available.map(obj => <li key={obj.object}>{obj.object}</li>)}
        </ul>
      </div>
      <div className="ObjectManagerList-acquired">
        Acquired objects:
        <ul>
          {acquired.map(obj =>
            <li key={obj.object}>
              {obj.object}{' '}
              <button
                data-object={obj.object}
                onClick={() => freeObject(obj.object)}
              >
                Free
              </button>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}

export default ObjectManagerList;
