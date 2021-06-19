import { createRouter, createWebHistory } from "vue-router";
import store from "@/store";
import Home from "@/views/Home.vue";
import About from "@/views/About.vue";
import Login from "@/components/Login.vue";
import Register from "@/components/Register.vue";
import MenteeProfile from "@/components/mentee/MenteeProfile.vue";
import MentorProfile from "@/components/mentor/MentorProfile.vue";
import FindMentor from "../components/mentee/FindMentor";
import MenteeBase from "../components/mentee/MenteeBase";
import MentorBase from "../components/mentor/MentorBase";


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
		path: "/login",
		name: "Login",
		component: Login,
		meta: {	requires_visitor: true }
	},
	{
		path: "/mentor",
		name: "Mentor",
		component: MentorBase, // TODO change
		meta: { requires_auth: true, requires_mentor: true },

		children: [
			{
				path: "profile",
				name: "MentorProfile",
				component: MentorProfile
			},
		]
	},
	{
		path: "/mentee",
		name: "Mentee",
		component: MenteeBase,
		meta: { requires_auth: true, requires_mentee: true },

		children: [
			{
				path: "profile",
				name: "MenteeProfile",
				component: MenteeProfile
			},
			{
				path: "find-mentor",
				name: "FindMentor",
				component: FindMentor,
			}
		]
	},
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
		else if (to.matched.some(record => record.meta.requires_mentor)) {
			if (!store.state.current_user.is_mentor) {
				next({ name: "Home" })
			}
			else {
				next()
			}
		}
		else if (to.matched.some(record => record.meta.requires_mentee)) {
			if (!store.state.current_user.is_mentee) {
				next({ name: "Home" })
			}
			else {
				next()
			}
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
