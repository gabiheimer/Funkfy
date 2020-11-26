import axios from 'axios';

const baseURL = `http://funkfy-api.dikastis.com.br`;

const api = axios.create({
  baseURL,
});

export default api;