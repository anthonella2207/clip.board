import axios from "axios";

const api = axios.create({
  baseURL: "https://api.themoviedb.org/3",
  params: {
    api_key: "814254e9d1fb4859da3f4798b86b6f49",
  },
});

export default api;
