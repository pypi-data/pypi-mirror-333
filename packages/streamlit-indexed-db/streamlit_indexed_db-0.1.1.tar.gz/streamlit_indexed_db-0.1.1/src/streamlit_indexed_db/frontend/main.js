// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function onRender(event) {

  const {
    action, 
    db, version, 
    objectStoreName, 
    indexMode, 
    key, 
    values, 
    accessMode
  } = event.detail.args;

  switch(action){
    case "creat_db":
      createIndexedDB();
      break;
    case "cursor_update":
      console.log('chamando cursor update')
      cursorUpdateIndexedDB();
      break;
    case "get_all":
      getAllIndexedDB();
    case "clear_object_store":
      clearObjectStore();
      break;
  }

  function createIndexedDB(){
    request = window.indexedDB.open(db, version);

    request.onupgradeneeded = (event) => {
      let db = event.target.result;
  
      if(!db.objectStoreNames.contains(objectStoreName)){
        db.createObjectStore(objectStoreName, indexMode);
      }
    }

    request.onerror = (event) => {
      console.log("failed to create a indexedDB: ", event.target.error);
    }
  }

  function cursorUpdateIndexedDB(){

    request = window.indexedDB.open(db, version);

    request.onsuccess = (event) => {
      let db = event.target.result;
      let objectStore = db.transaction([objectStoreName], "readwrite")
      .objectStore(objectStoreName);

      values.forEach((value) => {
        let found = false;
        console.log(JSON.stringify(value));

        let cursorRequest = objectStore.openCursor();

        cursorRequest.onsuccess = (event) => {
          let cursor = event.target.result;
          
          if (cursor){
            if(JSON.stringify(cursor.value) === JSON.stringify(value))
              found = true;
            cursor.continue();
          }
          else{
            if(!found){
              let requestUpdate = objectStore.put(value);

              requestUpdate.onerror = (event) => {
                console.log("failed to update value on indexedDB: ", event.target.error);
              }
            }
          }
        }
      });
    }

    request.onerror = (event) => {
      console.log('failed in requisition: ', event.target.error)
    }

  }

  function getAllIndexedDB(){
    request = window.indexedDB.open(db, version);

    request.onsuccess = (event) => {
      let indexedDBValues = []

      let db = event.target.result;
      let objectStore = db.transaction([objectStoreName], "readonly")
      .objectStore(objectStoreName);

      cursorRequest = objectStore.openCursor();

      cursorRequest.onsuccess = (event) => {
        cursor = event.target.result;

        if (cursor){
          indexedDBValues.push(cursor.value);
          cursor.continue();
        }
        // Allow streamlit to send data for Python
        Streamlit.setComponentValue(indexedDBValues);
      }
      
      cursorRequest.onerror = (event) => {
        console.log('failed to get a value: ', event.target.error);
      }

    }
  }

  function clearObjectStore(){
    request = window.indexedDB.open(db, version);

    reques.onsuccess = (event) => {
      let db = event.target.result;
      objectStore = db.transaction([objectStoreName], "readwrite")
      .objectStore(objectStoreName)

      clearRequest = objectStore.clear()

      clearRequest.onsuccess = (event) => {
        console.log('objectStore is cleaned');
      }

      clearRequest.onerror = (event) => {
        console.log('failed to clear object store: ', event.target.error);
      }
    }
  }

  window.rendered = true
}

// Add listener for Streamlit rendering
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
// Mark the component as ready
Streamlit.setComponentReady();
