import { createStore } from "vuex";

const store = createStore({
	strict: true,
	state: {
		token: localStorage.getItem("rmp_token"),
		current_user: JSON.parse(localStorage.getItem("rmp_current_user")) || {
			uid: null,
			profile_uid: null,
			email: null,
			username: null,
			first_name: null,
			last_name: null,
			date_of_birth: null,
			is_mentor: false,
			is_mentee: false,
		},

		show_loading: false,
	},
	getters: {
		logged_in(state)
		{
			return state.token != null; // Not using !==
		}
	},
	mutations: {
		set_token(state, token)
		{
			localStorage.setItem("rmp_token", token);
			state.token = token;
		},

		set_current_user(state, data)
		{
			localStorage.setItem("rmp_current_user", JSON.stringify(data)); // Stringify is needed
			state.current_user = {...data};

			// TODO Logout and redirect to 'Home' if this is the case
			// if (state.is_mentor === state.is_mentee) {}
		},

		update_token(state, token)
		{
			state.token_token = token;
		},

		destroy_token(state)
		{
			state.token = null;
			localStorage.removeItem("rmp_token");
		},

		destroy_current_user(state)
		{
			state.current_user = {};
			localStorage.removeItem("rmp_current_user");
		},

		set_show_loading(state, value)
		{
			state.show_loading = value;
		}
	},
	actions: {
		logout_user(context)
		{
			context.commit("destroy_token");
			context.commit("destroy_current_user");
		}
	},
	modules: {

	}
});

export default store;
