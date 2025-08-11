function init(chatPort) {
  const socket = new WebSocket(`${window.location.hostname}:${chatPort}`);

  socket.onopen = () => {
    console.log("Connected to chat server");
  };

  socket.onmessage = (event) => {
    console.log("Received message:", event.data);
  };

  socket.onclose = () => {
    console.log("Disconnected from chat server");
  };
}
