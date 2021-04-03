import React from 'react';

function ObjectManagerList({ objects }) {
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
          {available.map(obj => <li>{obj.object}</li>)}
        </ul>
      </div>
      <div className="ObjectManagerList-acquired">
        Acquired objects:
        <ul>
          {acquired.map(obj => <li>{obj.object}</li>)}
        </ul>
      </div>
    </div>
  );
}

export default ObjectManagerList;
