import {createRouter, createWebHistory} from 'vue-router';
import Home from '../views/Home.vue';
import About from '../views/About.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';

const routes = [
	{
		path: '/',
		name: 'Home',
		component: Home
	},
	{
		path: '/about',
		name: 'About',
		component: About
	},
	{
		path: '/login',
		name: 'Login',
		component: Login
	},
	{
		path: '/register-mentor',
		name: 'RegisterMentor',
		props: {
			request_url: "/api/users/user/register-mentor",
			register_as_mentor: true,
		},
		component: Register
	},
	{
		path: '/register-mentee',
		name: 'RegisterMentee',
		props: {
			request_url: "/api/users/user/register-mentee",
			register_as_mentor: false
		},
		component: Register
	}
];

const router = createRouter({
	history: createWebHistory(process.env.BASE_URL),
	routes
});

export default router;
