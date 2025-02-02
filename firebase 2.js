import { initializeApp } from "firebase/app";
import { getDatabase } from "firebase/database";
import { getStorage } from "firebase/storage";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyCia2Yw4EzHEd1jddEWu0RDsGXtaV2gHho",
  authDomain: "carrot-market-10b0e.firebaseapp.com",
  databaseURL:
    "https://carrot-market-10b0e-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "carrot-market-10b0e",
  storageBucket: "carrot-market-10b0e.firebasestorage.app",
  messagingSenderId: "634854984709",
  appId: "1:634854984709:web:9c29b5b9f884092448a06c",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Realtime Database and get a reference to the service
const database = getDatabase(app);
const storage = getStorage(app);
const auth = getAuth(app);
