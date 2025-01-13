import axios from "axios";

const API_KEY = "814254e9d1fb4859da3f4798b86b6f49"; // Tu API Key
const BASE_URL = "https://api.themoviedb.org/3";

const api = axios.create({
  baseURL: BASE_URL,
  params: {
    api_key: API_KEY,
    language: "en-US", // Idioma predeterminado
  },
});

export default api;
