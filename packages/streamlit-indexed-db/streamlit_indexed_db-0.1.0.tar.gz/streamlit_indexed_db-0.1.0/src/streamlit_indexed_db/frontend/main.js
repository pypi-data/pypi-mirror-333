// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function onRender(event) {

  const {action, db, version, objectStoreName, indexMode, key, values, accessMode} = event.detail.args;

  switch(action){
    case "creat_db":
      createIndexedDB();
      break;
    case "cursor_update":
      console.log('chamando cursor update')
      cursorUpdateIndexedDB();
      break;
    case "get_all":
      getAllIndexedDB()
  }

  function createIndexedDB(){
    request = window.indexedDB.open(db, version);

    request.onupgradeneeded = (event) => {
      let db = event.target.result;
  
      if(!db.objectStoreNames.contains(objectStoreName)){
        db.createObjectStore(objectStoreName, indexMode);
        console.log(objectStoreName + " foi criado com sucesso!");
      }
    }

    request.onerror = (event) => {
      console.log("failed to create a indexedDB: ", event.target.error);
    }
  }

  function cursorUpdateIndexedDB(){
    console.log('cursor update inicializado')

    request = window.indexedDB.open(db, version);

    request.onsuccess = (event) => {
      console.log('requisição ao banco bem sucedidia');
      let db = event.target.result;
      let objectStore = db.transaction([objectStoreName], "readwrite")
      .objectStore(objectStoreName);

      values.forEach((value) => {
        let found = false;
        console.log('passando pelo valor: ')
        console.log(JSON.stringify(value));

        let cursorRequest = objectStore.openCursor();

        cursorRequest.onsuccess = (event) => {
          let cursor = event.target.result;
          
          if (cursor){
            console.log('cursor foi chamado');
            if(JSON.stringify(cursor.value) === JSON.stringify(value))
              found = true;
            cursor.continue();
          }
          else{
            if(!found){
              console.log('fazendo update do valor: ', value);
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
      console.log('falha na requisição do banco: ', event.target.error)
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
        Streamlit.setComponentValue(indexedDBValues);
        console.log('sucesso ao passar os valores')
      }
      
      cursorRequest.onerror = (event) => {
        console.log('failed to get a value: ', event.target.error);
      }

    }
  }

  window.rendered = true
}

// Adiciona o listener para renderização do Streamlit
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
// Marca o componente como pronto
Streamlit.setComponentReady();
