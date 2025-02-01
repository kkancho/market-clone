import App from "./App.svelte";
import "../firebase.js";

const app = new App({
  target: document.getElementById("app"), // index.html에 있는 #app 요소
});

export default app;
