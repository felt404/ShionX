class WSClient {
  constructor(path) {
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    this.url = `${proto}://${window.location.host}${path}`;
    this.socket = null;
    this.listeners = new Map();
  }

  connect() {
    this.socket = new WebSocket(this.url);
    this.socket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      (this.listeners.get(payload.type) || []).forEach((cb) => cb(payload));
    };
    return this.socket;
  }

  on(type, callback) {
    const existing = this.listeners.get(type) || [];
    this.listeners.set(type, [...existing, callback]);
  }

  send(type, payload) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      throw new Error("WebSocket not connected");
    }
    this.socket.send(JSON.stringify({ type, payload }));
  }
}

window.WSClient = WSClient;
