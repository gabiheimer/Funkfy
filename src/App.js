import './App.css';
import React, { useState } from 'react';
import { searchSpotifySong, searchSpotifyAudioFeatures } from './requests';
import Crunker from 'crunker/src/crunker';

export default function App() {
  const [songFile, setSongFile] = useState('');
  const [spotifyTrack, setSpotifyTrack] = useState({song: '', artist: ''});

  let audio = new Crunker();
  const file1 = require('./audio/funk.mp3');

  function onTrackChange(evt) {
    setSpotifyTrack({...spotifyTrack, [evt.target.name]: evt.target.value});
  }

  async function handleSubmit(evt) {
    evt.preventDefault();
    const spotifyResponseSong = await searchSpotifySong(spotifyTrack);

    if(!spotifyResponseSong) {
      alert('essa musica nao da!');
      return;
    }

    const originalSongAudioFeatures = await searchSpotifyAudioFeatures(spotifyResponseSong.id);
    console.log(originalSongAudioFeatures);
  }

  function handleFileChange(e) {
    var target = e.currentTarget;
    var file = target.files[0];    
    if (target.files && file) {
      var reader = new FileReader();
      reader.onload = function (e) {
        setSongFile(e.target.result);
      }
      reader.readAsDataURL(file);
    }
  }

  async function mergeee() {
    audio
      .fetchAudio(file1.default, songFile)
      .then(buffers => audio.mergeAudio(buffers))
      .then(merged => audio.export(merged, "audio/mp3"))
      .then(output => audio.download(output.blob))
      .catch(error => {
        throw new Error(error);
      });
  }

  return (
    <div className="App">
      <h1>QUERO PASSINHO!</h1>
      <form onSubmit={handleSubmit}>
        <input type='text' name='song' placeholder='song name' onChange={onTrackChange} value={spotifyTrack.song}/>
        <input type='text' name='artist' placeholder='artist' onChange={onTrackChange} value={spotifyTrack.artist}/>
        <input type='file'  accept='audio/' onChange={handleFileChange}/>
        <button type='submit' >search</button>
      </form>
      <audio src={songFile} controls />
      <button onClick={mergeee} >teste do merge de audio</button>
    </div>
  );
}