// src/firebase.js
import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  getIdToken,
} from "firebase/auth";

import {
  getFirestore,
  collection,
  addDoc,
  query,
  where,
  getDocs,
  orderBy,
  serverTimestamp,
} from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyB3MtOEECEuMYoZ5Fw7TpCh68kD0eC_H5c",
  authDomain: "gitresume-63d22.firebaseapp.com",
  projectId: "gitresume-63d22",
  storageBucket: "gitresume-63d22.firebasestorage.app",
  messagingSenderId: "939790669754",
  appId: "1:939790669754:web:de24ab5ce7f35ac3f6af83",
  measurementId: "G-0TCVJT7HJE"
};

// Initialize Firebase app
const app = initializeApp(firebaseConfig);

// Auth exports
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

// Firestore exports
const db = getFirestore(app);

export {
  auth,
  provider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  getIdToken,
  db,
  collection,
  addDoc,
  query,
  where,
  getDocs,
  orderBy,
  serverTimestamp,
};
