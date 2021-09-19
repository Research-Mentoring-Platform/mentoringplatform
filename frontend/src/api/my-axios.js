import { default as my_axios } from "axios";
import store from "../store";

const API_URL = "http://localhost:8000/"; // URL for the backend API server

const axios = my_axios.create({
	baseURL: API_URL,
	headers: {
		"content-type": "application/json",
	}
});

// For setting Authorization request headers automatically
axios.interceptors.request.use((config) => {
	store.commit("set_show_loading", true);
	const bearer_token = store.state.token;
	if (bearer_token) { config.headers.Authorization = `Bearer ${bearer_token}`; }
	return config;
}, (error) => {
	store.commit("set_show_loading", false);
	return Promise.reject(error);
});

axios.interceptors.response.use((response) => {
	store.commit("set_show_loading", false);
	return response;
}, (error) => {
	store.commit("set_show_loading", false);
	return Promise.reject(error);
});

export default axios;
