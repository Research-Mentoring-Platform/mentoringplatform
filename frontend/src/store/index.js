import { createStore } from "vuex";

export default createStore({
	state: {
		access_token: localStorage.getItem("rmp_access_token") || null,
		refresh_token: localStorage.getItem("rmp_refresh_token") || null
	},
	getters: {
		logged_in(state) {
			return state.access_token != null; // Not using !==
		}
	},
	mutations: {
		update_local_storage (state, { access, refresh }) {
			localStorage.setItem("rmp_access_token", access);
			localStorage.setItem("rmp_refresh_token", refresh);
			state.access_token = access;
			state.refresh_token = refresh;
		},
		update_access (state, access) {
			state.access_token = access;
		},
		destroy_token (state) {
			state.access_token = null;
			state.refresh_token = null;
			localStorage.removeItem("rmp_access_token");
			localStorage.removeItem("rmp_refresh_token");
		}
	},
	actions: {

	},
	modules: {

	}
});
