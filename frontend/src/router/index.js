import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import Home from "@/views/Home.vue";
import About from "@/views/About.vue";
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";
import MenteeProfile from "@/components/mentee/MenteeProfile.vue";
import MentorProfile from "@/components/mentor/MentorProfile.vue";


// TODO Look for lazy loading for routes

const routes = [
	{
		path: "/",
		name: "Home",
		component: Home,
		meta: {	requires_auth: false }
	},
	{
		path: "/about",
		name: "About",
		component: About,
		meta: { requires_auth: false }
	},
	{
		path: "/login",
		name: "Login",
		component: Login,
		meta: {	requires_visitor: true }
	},
	{
		path: "/register-mentor",
		name: "RegisterMentor",
		component: Register,
		props: { register_as_mentor: true },
		meta: { requires_visitor: true }
	},
	{
		path: "/register-mentee",
		name: "RegisterMentee",
		component: Register,
		props: { register_as_mentor: false },
		meta: { requires_visitor: true }
	},
	{
		path: "/profile",
		name: 'Profile',
		component: (store.state.is_mentor === true) ? MentorProfile : MenteeProfile,
		// The following statement gives a warning (Promise not returned)
		// component: () => (store.state.is_mentor === true) ? MentorProfile : MenteeProfile,
		meta: { requires_auth: true }
	}
];

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
});

router.beforeEach((to, from, next) => {
	if (to.matched.some(record => record.meta.requires_auth)) {
		if (!store.getters.logged_in) {
			next({ name: "Login" })
		}
		else {
			next()
		}
	}
	else if (to.matched.some(record => record.meta.requires_visitor)) {
		if (store.getters.logged_in) {
			next({ name: "Home" })
		}
		else {
			next()
		}
	}
	else {
		next()
	}
});

export default router;
