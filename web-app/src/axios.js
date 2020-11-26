import axios from 'axios';

const baseURL = `http://funkfy-api.dikastis.com.br:5020`;

const api = axios.create({
  baseURL,
});

export default api;