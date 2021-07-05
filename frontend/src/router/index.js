import { createRouter, createWebHistory } from "vue-router";
import store from "../store";

// Views
import Home from "../views/Home";
import About from "../views/About";
import Login from "../components/Login";
import Register from "../components/Register";

// Mentor
import MentorBase from "../components/mentor/MentorBase";
import MentorProfile from "../components/mentor/MentorProfile";
import MentorProfileSettings from "../components/mentor/MentorProfileSettings";
import MentorPendingRequests from "../components/mentor/MentorPendingRequests";
import MyMentees from "../components/mentor/MyMentees";

// Mentee
import MenteeBase from "../components/mentee/MenteeBase";
import MenteeProfile from "../components/mentee/MenteeProfile";
import MenteeProfileSettings from "../components/mentee/MenteeProfileSettings";
import MenteePendingRequests from "../components/mentee/MenteePendingRequests";
import MyMentors from "../components/mentee/MyMentors";
import FindMentor from "../components/mentee/FindMentor";

// Mentorship
import Milestones from "../components/mentorship/Milestones";
import Mentorship from "../components/mentorship/Mentorship";
import MentorSettings from "../components/mentor/MentorSettings";


// TODO Look for lazy loading for routes

const routes = [
	{
		path: "/",
		name: "Home",
		component: Home
	},
	{
		path: "/about",
		name: "About",
		component: About
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
		path: "/test",
		name: "Test",
		component: MentorSettings,
		meta: { requires_auth: true }
	},
	{
		path: "/mentor",
		name: "Mentor",
		component: MentorBase,
		meta: { requires_auth: true },

		children: [
			{
				path: "profile/:profile_uid?",
				name: "MentorProfile",
				component: MentorProfile,
				// Mentees can view the profile too
			},
			{
				path: "profile-settings",
				name: "MentorProfileSettings",
				component: MentorProfileSettings,
				meta: { requires_mentor: true }
			},
			{
				path: "pending-requests",
				name: "MentorPendingRequests",
				component: MentorPendingRequests,
				meta: { requires_mentor: true }
			},
			{
				path: "my-mentees",
				name: "MyMentees",
				component: MyMentees,
				meta: { requires_mentor: true }
			},
			{
				path: "mentor-settings",
				name: "MentorSettings",
				component: MentorSettings,
				props: { is_editable: true },
				meta: { requires_mentor: true }
			}
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
				path: "profile-settings",
				name: "MenteeProfileSettings",
				component: MenteeProfileSettings
			},
			{
				path: "pending-requests",
				name: "MenteePendingRequests",
				component: MenteePendingRequests
			},
			{
				path: "my-mentors",
				name: "MyMentors",
				component: MyMentors
			},
			{
				path: "find-mentor",
				name: "FindMentor",
				component: FindMentor,
			},
		]
	},
	{
		path: "/mentorship/:mentorship_uid",
		name: "Mentorship",
		component: Mentorship,
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
		else if (to.matched.some(record => record.meta.requires_mentor)) {
			if (!store.state.user.is_mentor) {
				next({ name: "Home" })
			}
			else {
				next()
			}
		}
		else if (to.matched.some(record => record.meta.requires_mentee)) {
			if (!store.state.user.is_mentee) {
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
