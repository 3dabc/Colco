// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";
import {getFirebase, getFirestore} from 'firebase/firestore';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCBzfCPae5dpeVEFKK4dSTQDp8CNiYnTLI",
  authDomain: "columbiaproject-f0f91.firebaseapp.com",
  databaseURL: "https://columbiaproject-f0f91-default-rtdb.firebaseio.com",
  projectId: "columbiaproject-f0f91",
  storageBucket: "columbiaproject-f0f91.firebasestorage.app",
  messagingSenderId: "958497867712",
  appId: "1:958497867712:web:44f82be004fd5bb96aaa25",
  measurementId: "G-W628QEQFKG"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);

const db = getFirestore(app);
export{db}