import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import About from "../views/About.vue";
import Base from "../views/Base.vue";
import Login from "../components/Login.vue";
import Register from "../components/Register.vue";
import Profile from "../components/mentee/Profile.vue";


//TODO Look for lazy loading for routes

const routes = [
	{
		path: "/",
		name: "Home",
		component: Home,
		meta: {
			requires_auth: false
		}
	},
	{
		path: "/about",
		name: "About",
		component: About,
		meta: {
			requires_auth: false
		}
	},
	{
		path: "/login",
		name: "Login",
		component: Login,
		meta: {
			requires_visitor: true
		}
	},
	{
		path: "/register-mentor",
		name: "RegisterMentor",
		props: { register_as_mentor: true },
		component: Register,
		meta: {
			requires_visitor: true
		}
	},
	{
		path: "/register-mentee",
		name: "RegisterMentee",
		props: { register_as_mentor: false },
		component: Register,
		meta: {
			requires_visitor: true
		}
	},
	{
		path: "/mentee",
		component: Base,
		children: [
			{
				path: "profile",
				name: "MenteeProfile",
				component: Profile,
				meta: {
					requires_auth: true
				}
			}
		]
	}
];

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
});

export default router;
