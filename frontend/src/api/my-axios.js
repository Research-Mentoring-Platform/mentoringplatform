import { default as my_axios } from "axios";
const API_URL = "http://localhost:8000/";

const axios = my_axios.create({
	baseURL: API_URL,
	headers: {
		"content-type": "application/json",
	}
});

// For setting Authorization headers automatically
axios.interceptors.request.use((config) => {
	const bearer_token = localStorage.getItem("rmp_token");
	if (bearer_token) { config.headers.Authorization = `Bearer ${bearer_token}`; }
	return config;
});

export default axios;
