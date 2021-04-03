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
  getObject,
  freeObject,
};
