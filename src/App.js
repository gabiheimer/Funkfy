import './App.css';
import React, { useState } from 'react';
import { searchSpotifySong } from './requests';

export default function App() {
  const [track, setTrack] = useState({song: '', artist: ''})

  function onChange(evt) {
    setTrack({...track, [evt.target.name]: evt.target.value});
  }

  function handleSubmit(evt) {
    evt.preventDefault();
    searchSpotifySong(track);
    setTrack({song: '', artist: ''});
  }

  return (
    <div className="App">
      <h1>QUERO PASSINHO!</h1>
      <form onSubmit={handleSubmit}>
        <input type='text' name='song' placeholder='song name' onChange={onChange} value={track.song}/>
        <input type='text' name='artist' placeholder='artist' onChange={onChange} value={track.artist}/>
        <button type='submit' >search</button>
      </form>
    </div>
  );
}
