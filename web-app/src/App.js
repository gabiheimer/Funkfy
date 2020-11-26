import './App.css';
import React, {useState, useEffect} from 'react';
import { post } from 'axios';
import Lottie from 'react-lottie';
import NoteMusic from './components/note_music.json'

import Dropzone from 'react-dropzone';

const url = process.env.api;

export default function App() {
  const [fileVoice, setFileVoice] = useState(null)
  const [fileBeat, setFileBeat] = useState(null)

  const [returnApi, setReturnAPI] = useState(true)
  const [returnApiGraphics, setReturnAPIGraphics] = useState(true)

  const [loading, setLoading] = useState(true)

  const [askingGraphics, setAskingGraphics] = useState(false)
  const [askingMerge, setAskingMerge] = useState(false)

  useEffect(() => {
    if(fileVoice !== null && fileBeat !== null){
      const formData = new FormData();
      formData.append('vocals',fileVoice)
      formData.append('accompaniment',fileBeat)

      const config = {
          headers: {
              'content-type': 'multipart/form-data'
          }
      }

      try {
        post(`${url}/song`, formData, config)
        setAskingGraphics(true);
        setAskingMerge(true);
      } catch (e){
        console.log(e)
      }
    }
  },[fileVoice, fileBeat])

  async function apiGetGraphics(){
    const response = await post();
    return response;
  }

  async function apiGetMerge(){
    const response = await post();
    return response;
  }

  useEffect(() => {
    if(askingGraphics){
      var poolingGraphics = setInterval(() => {
        const response = apiGetGraphics();
        if(response.status === 200) clearInterval(poolingGraphics);
      }, 3000)
    }
  }, [askingGraphics])

  useEffect(() => {
    if(askingMerge){
      var poolingMerge = setInterval(() => {
        const response = apiGetMerge();
        if(response.status === 200) clearInterval(poolingMerge);
      }, 3000)
    }
  }, [askingMerge])

  const defaultOptions = {
    loop: true,
    autoplay: true, 
    animationData: NoteMusic,
    rendererSettings: {
      preserveAspectRatio: 'xMidYMid slice'
    },
  };

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
        {returnApi === false && (<div>Esperando api para continuar ...</div>)}
        {returnApi && (
          <div style={{display: 'flex', flexDirection: 'row', marginLeft: '15%'}}>
            <div style={{width: '50%'}}>
              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Velocidade da voz: </h4>
                <input type="number" id="quantity" name="quantity" min="-1000" max="1000"></input>
              </div>

              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Fator decibéis da voz: </h4>
                <input type="number" id="quantity" step="0.01" name="quantity" min="-1000" max="1000"></input>
              </div>
            </div>

            <div style={{width: '50%'}}>
              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Velocidade da batida: </h4>
                <input type="number" id="quantity" name="quantity" min="-1000" max="1000"></input>
              </div>

              <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
                <h4 style={{marginRight: '10px'}}>Fator decibéis da batida: </h4>
                <input type="number" id="quantity" step="0.01" name="quantity" min="-1000" max="1000"></input>
              </div>
            </div>

            <div style={{display: 'flex', alignItems: 'flex-end' }}>
              <button type="button" style={{fontSize: '16px', backgroundColor: '#cccccc', cursor: 'pointer'}}>Aplicar</button>
            </div>
          </div>
        )}
      </div>

      <div style={{minWidth: '70%'}}>
        <h3 style={{textAlign: 'left'}}>Gráfico:</h3>
        {returnApiGraphics === false && (<div>Esperando api para continuar ...</div>)}
        {returnApiGraphics && (<img src="https://static.imasters.com.br/wp-content/uploads/2018/04/HG.jpg" alt="Graphics" width="100%" height="300"></img>)}
      </div>
            
      {returnApi && (
        <div style={{padding: '30px'}}>
          <button type="button" style={{fontSize: '24px', backgroundColor: '#f44336', cursor: 'pointer'}}>MERGEEEE!</button>
        </div>
      )}
    </div>
  );
}