import axios from 'axios';
import qs from 'qs';

const clientId = process.env.REACT_APP_CLIENT_ID;
const clientSecret = process.env.REACT_APP_CLIENT_SECRET;

async function getToken() {
    const headers = {
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        auth: {
          username: clientId,
          password: clientSecret,
        },
    };
  
    const data = {
        grant_type: 'client_credentials',
    };
  
    const response = await axios.post('https://accounts.spotify.com/api/token', qs.stringify(data), headers);
    return response.data.access_token;
}

export async function searchSpotifySong(trackInfo) {
    const token = await getToken()
    const song = trackInfo.song.replaceAll(' ', '%20');
    const artist = trackInfo.artist.replaceAll(' ', '%20');
    const query = `https://api.spotify.com/v1/search?q=track%3A${song}%20artist%3A${artist}&type=track`

    const headers = {
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    }

    const response = await axios.get(query, headers);
    console.log(response);
}