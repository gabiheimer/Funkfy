import './App.css';
import React, { useState } from 'react';

export default function App() {
  const [song, setSong] = useState('');
  const coiso = new FileReader();

  console.log('coiso:')
  console.log(coiso);

  function handleChange(e) {
    var target = e.currentTarget;
    var file = target.files[0];    
    if (target.files && file) {
      var reader = new FileReader();
      reader.onload = function (e) {
        setSong(e.target.result);
      }
      reader.readAsDataURL(file);
    }
  }

  return (
    <div className="App">
      <h1>QUERO PASSINHO!</h1>
      <form>
        <input type='file'  accept='audio/' onChange={handleChange}/>
      </form>
      <audio src={song} controls />
    </div>
  );
}