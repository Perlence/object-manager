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

export {
  putObject,
  getObject,
  freeObject,
  dropObject,
};
