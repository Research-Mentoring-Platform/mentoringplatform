import { default as my_axios } from "axios";
const API_URL = "http://localhost:8000/";

const axios = my_axios.create({
	baseURL: API_URL,
	headers: { "content-type": "application/json" }
});

export default axios;
