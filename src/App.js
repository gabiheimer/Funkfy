import './App.css';
import React, { useState } from 'react';
import { searchSpotifySong, searchSpotifyAudioFeatures } from './requests';
import * as Tone from 'tone'
const { exec } = require("child_process");


export default function App() {
  const [songFile, setSongFile] = useState('');
  const [spotifyTrack, setSpotifyTrack] = useState({ song: '', artist: '' });

  function onTrackChange(evt) {
    setSpotifyTrack({ ...spotifyTrack, [evt.target.name]: evt.target.value });
  }

  async function handleSubmit(evt) {
    evt.preventDefault();
    const spotifyResponseSong = await searchSpotifySong(spotifyTrack);

    if (!spotifyResponseSong) {
      alert('essa musica nao da!');
      return;
    }

    const originalSongAudioFeatures = await searchSpotifyAudioFeatures(spotifyResponseSong.id);
    console.log(originalSongAudioFeatures);
  }

  async function play2AudiosUsingToneJS() {
    const file1 = require("./audio/billijean.mp3");
    const file2 = require("./audio/acucar-de-melancia-mto-doido.mp3");

    const player = new Tone.Player(file1.default).toDestination();
    const player2 = new Tone.Player(file2.default).toDestination();
    Tone.loaded().then(() => {
      player.start();
      player2.start();
    });
  }

  function command() {

    exec("echo 'daaale'", (error, stdout, stderr) => {
      if (error) {
        console.log(`error: ${error.message}`);
        return;
      }
      if (stderr) {
        console.log(`stderr: ${stderr}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
    });
  }

  //attach a click listener to a play button
  document.querySelector('button')?.addEventListener('click', async () => {
    await Tone.start()
    console.log('audio is ready')
  })

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

  return (
    <div className="App">
      <h1>QUERO PASSINHO!</h1>
      <form onSubmit={handleSubmit}>
        <input type='text' name='song' placeholder='song name' onChange={onTrackChange} value={spotifyTrack.song} />
        <input type='text' name='artist' placeholder='artist' onChange={onTrackChange} value={spotifyTrack.artist} />
        <input type='file' accept='audio/' onChange={handleFileChange} />
        <button type='submit' >search</button>
      </form>
      <audio src={songFile} controls />


      <button onClick={play2AudiosUsingToneJS}>tonejs</button>
      <button onClick={command}>comando</button>
    </div>
  );
}