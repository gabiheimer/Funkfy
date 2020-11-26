/* eslint-disable react-hooks/exhaustive-deps */
import './App.css';
import React, {useState, useEffect} from 'react';
import axios from './axios';
import Lottie from 'react-lottie';
import NoteMusic from './components/note_music.json'

import Dropzone from 'react-dropzone';


const isLocalhost = Boolean(
  window.location.hostname === 'localhost' ||
    window.location.hostname === '[::1]' ||
    window.location.hostname.match(
      /^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/,
    ),
);

export default function App() {
  const [fileVoice, setFileVoice] = useState(null)
  const [fileBeat, setFileBeat] = useState(null)

  const [sendFilesApi, setSendFilesApi] = useState(false)
  const [returnApiGraphics, setReturnAPIGraphics] = useState(false)

  async function sendFilesToApi(){
    const formData = new FormData();
    formData.append('vocals',fileVoice[0])
    formData.append('accompaniment',fileBeat[0])

    try {
      await axios.post('/songs', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      setSendFilesApi(true);
    } catch (e){
      console.log(e)
    }
  }

  useEffect(() => {
    if(fileVoice !== null && fileBeat !== null){
      sendFilesToApi();
    }
  },[fileVoice, fileBeat])

  async function apiGetGraphics(){
    const response = await axios.get('/graphs/' + fileVoice[0].name + '/' + fileBeat[0].name);
    return response;
  }

  useEffect(() => {
    if(sendFilesApi){
      var poolingGraphics = setInterval(async () => {
        const response = await apiGetGraphics();
        if(response.status === 200) {
          clearInterval(poolingGraphics);
          setReturnAPIGraphics(true);
          setSendFilesApi(false);
        }
      }, 3000)
    }
  },[sendFilesApi])


  const defaultOptions = {
    loop: true,
    autoplay: true, 
    animationData: NoteMusic,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid slice'
    },
  };

  const [voiceFact, setVoiceFact] = useState()
  const [decbVoice, setDecbVoice] = useState()
  const [beatFact, setBeatFact] = useState()
  const [decbBeat, setDecbBeat] = useState()

  function onChangeVoiceFactor(event){
    setVoiceFact(event.target.value);
  }

  function onChangeBeatFactor(event){
    setBeatFact(event.target.value);
  }

  function onChangeVoiceDecb(event){
    setDecbVoice(event.target.value);
  }

  function onChangeBeatDecb(event){
    setDecbBeat(event.target.value);
  }

  async function onSubmitValues(){
    await axios.put('/songs',{
      "vocals": fileVoice[0].name,
      "vocal_speed": voiceFact,
      "vocal_volume": decbVoice,
      "accompaniment": fileBeat[0].name,
      "accompaniment_speed": beatFact,
      "accompaniment_volume": decbBeat
    })
    setSendFilesApi(true);
  }

  async function onMerge(){
    await axios.patch('/songs',{
      "vocals": fileVoice[0].name,
      "vocal_speed": voiceFact,
      "vocal_volume": decbVoice,
      "accompaniment": fileBeat[0].name,
      "accompaniment_speed": beatFact,
      "accompaniment_volume": decbBeat
    })
    setPermissionGetMerge(true)
  }
  const [permissionGetMerge, setPermissionGetMerge] = useState(false)

  async function apiGetMerge(){
    const response = await axios.get('/results/' + fileVoice[0].name + '/' + fileBeat[0].name);
    return response;
  }

  const [urlMerge, setUrlMerge] = useState(null)

  useEffect(() => {
    if(permissionGetMerge){
      var poolingGraphics = setInterval(async () => {
        const response = await apiGetMerge();
        console.log(response);
        if(response.status === 200) {
          clearInterval(poolingGraphics);
          setPermissionGetMerge(false);
          setUrlMerge(response.config.baseURL + response.config.url);
        }
      }, 3000)
    }
  },[permissionGetMerge])


  return (
    <div style={{backgroundColor: '#38c172', display: 'flex', flexDirection: 'column', alignItems: 'center', maxHeight: '150vh', minHeight: '100vh'}} className="App">
      <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
        <h1 style={{display: 'flex', fontFamily: 'Viga', paddingLeft: '25%', paddingRight: '100%', justifyContent: 'center' }}>FUNKFY</h1>
        <div>
          <Lottie options={defaultOptions}
            height={120}
            width={120}
          />
        </div>
      </div>

      <div style={{display: 'flex', flexDirection: 'row'}}>
        <div style={{display: 'flex', flexDirection: 'column', borderWidth: '1.5px', borderStyle: 'dashed', borderColor: '#000', padding: '15px', marginRight: '10px', alignItems: 'center', justifyContent: 'center'}}>
          {fileVoice === null && (
            <Dropzone onDrop={acceptedFiles => setFileVoice(acceptedFiles)}>
              {({getRootProps, getInputProps}) => (
                <section>
                  <div {...getRootProps()}>
                    <input {...getInputProps()} />
                    <p>Insira o arquivo .mp3 para voz aqui, <br/>ou clique para selecionar o arquivo</p>
                  </div>
                </section>
              )}
            </Dropzone>
          )}
          {fileVoice !== null && (
            <div> Arquivo Inserido! </div>
          )}
        </div>

        <div style={{display: 'flex', flexDirection: 'column', borderWidth: '1.5px', borderStyle: 'dashed', borderColor: '#000', padding: '15px', marginRight: '10px', alignItems: 'center', justifyContent: 'center'}}>
          {fileBeat === null && (<Dropzone onDrop={acceptedFiles => setFileBeat(acceptedFiles)}>
            {({getRootProps, getInputProps}) => (
              <section>
                <div {...getRootProps()}>
                    <input {...getInputProps()} />
                    <p>Insira o arquivo .mp3 para batida aqui, <br/>ou clique para selecionar o arquivo</p>
                  </div>
                </section>
              )}
            </Dropzone>)}
            {fileBeat !== null && (
              <div> Arquivo Inserido! </div>
            )}
        </div>
      </div>

      <div style={{minWidth: '70%'}}>
        <h3 style={{textAlign: 'left'}}>Propiedades:</h3>
        {returnApiGraphics === false && (<div>Esperando api para continuar ...</div>)}
        {returnApiGraphics && (
          <div style={{display: 'flex', flexDirection: 'row', marginLeft: '15%'}}>
            <div style={{width: '50%'}}>
              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Velocidade da voz: </h4>
                <input type="number" id="quantity" name="quantity" min="-1000" max="1000" value={voiceFact} onChange={event => onChangeVoiceFactor(event)}></input>
              </div>

              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Fator decibéis da voz: </h4>
                <input type="number" id="quantity" step="0.01" name="quantity" min="0" max="10" value={decbVoice} onChange={event => onChangeVoiceDecb(event)}></input>
              </div>
            </div>

            <div style={{width: '50%'}}>
              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Velocidade da batida: </h4>
                <input type="number" id="quantity" name="quantity" min="-1000" max="1000" value={beatFact} onChange={event => onChangeBeatFactor(event)}></input>
              </div>

              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Fator decibéis da batida: </h4>
                <input type="number" id="quantity" step="0.01" name="quantity" min="0" max="10" value={decbBeat} onChange={event => onChangeBeatDecb(event)}></input>
              </div>
            </div>

            <div style={{display: 'flex', alignItems: 'flex-end' }}>
              <button type="button" style={{fontSize: '16px', backgroundColor: '#cccccc', cursor: 'pointer'}} onClick={() => onSubmitValues()}>Aplicar</button>
            </div>
          </div>
        )}
      </div>

      <div style={{minWidth: '70%'}}>
        <h3 style={{textAlign: 'left'}}>Gráfico:</h3>
        {returnApiGraphics === false && (<div>Esperando api para continuar ...</div>)}
        {returnApiGraphics && (<img key={Date.now()} src={'http://funkfy-api.dikastis.com.br/graphs/' + fileVoice[0].name + '/' + fileBeat[0].name} alt="Graphics" width="100%" height="300"></img>)}
        {/*returnApiGraphics && (<img src={url + '/graphs/' + fileVoice[0].name + '/' + fileBeat[0].name + '?' + new Date()} alt="Graphics" width="100%" height="300"></img>)*/}
      </div>
            
      {returnApiGraphics && (
        <div style={{padding: '30px'}}>
          <button type="button" style={{fontSize: '24px', backgroundColor: '#f44336', cursor: 'pointer'}} onClick={() => onMerge()}>MERGEEEE!</button>
        </div>
      )}

      {urlMerge !== null &&(
        <audio controls>
          <source src={urlMerge} type="audio/mp3"></source>
        </audio>
      )}
    </div>
  );
}