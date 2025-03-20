function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function onRender(event) {

  const {action, key, value} = event.detail.args;

  switch(action){
    case "set_item":
      sessionStorageSetItem();
      break;
    case "get_item":
      sessionStorageGetItem();
      break;
  }

  function sessionStorageSetItem(){
    sessionStorage.setItem(key, value);
  }
  window.rendered = true

  function sessionStorageGetItem(){
    return sendValue(sessionStorage.getItem(key));
  }
  
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(100)
