import { createRouter, createWebHistory } from "vue-router";
import store from "../store";

// Basic (Visitor)
import HomePage from "../views/HomePage";
import AboutPage from "../views/AboutPage";
import LoginPage from "../views/LoginPage";
import RegisterPage from "../views/RegisterPage";
import VerifyTokenPage from "../views/VerifyTokenPage";
import ForgotPasswordPage from "../views/ForgotPasswordPage";

// Common
import ChangePasswordPage from "../views/common/ChangePasswordPage";

// Mentor
import MentorBasePage from "../views/mentor/MentorBasePage";
import MentorProfilePage from "../views/mentor/MentorProfilePage";
import MentorProfileSettingsPage from "../views/mentor/MentorProfileSettingsPage";
import MentorPendingRequestsPage from "../views/mentor/MentorPendingRequestsPage";
import MyMenteesPage from "../views/mentor/MyMenteesPage";
import MentorSettingsPage from "../views/mentor/MentorSettingsPage";

// Mentee
import MenteeBasePage from "../views/mentee/MenteeBasePage";
import MenteeProfilePage from "../views/mentee/MenteeProfilePage";
import MenteeProfileSettingsPage from "../views/mentee/MenteeProfileSettingsPage";
import MenteePendingRequestsPage from "../views/mentee/MenteePendingRequestsPage";
import MyMentorsPage from "../views/mentee/MyMentorsPage";
import FindMentorPage from "../views/mentee/FindMentorPage";

// Mentorship
import MentorshipPage from "../views/mentorship/MentorshipPage";


// TODO Look for lazy loading for routes

const routes = [
	{
		path: "/",
		name: "HomePage",
		component: HomePage
	},
	{
		path: "/about",
		name: "AboutPage",
		component: AboutPage
	},
	{
		path: "/verify-token",
		name: "VerifyTokenPage",
		component: VerifyTokenPage,
		meta: { requires_visitor: true }
	},
	{
		path: "/register-mentor",
		name: "RegisterMentorPage",
		component: RegisterPage,
		props: { register_as_mentor: true },
		meta: { requires_visitor: true }
	},
	{
		path: "/register-mentee",
		name: "RegisterMenteePage",
		component: RegisterPage,
		props: { register_as_mentor: false },
		meta: { requires_visitor: true }
	},
	{
		path: "/login",
		name: "LoginPage",
		component: LoginPage,
		meta: {	requires_visitor: true }
	},
	{
		path: "/forgot-password",
		name: "ForgotPasswordPage",
		component: ForgotPasswordPage,
		meta: {	requires_visitor: true }
	},
	{
		path: "/change-password",
		name: "ChangePasswordPage",
		component: ChangePasswordPage,
		meta: {	requires_auth: true }
	},
	{
		path: "/mentor",
		name: "MentorPage",
		component: MentorBasePage,
		meta: { requires_auth: true },

		children: [
			{
				path: "profile/:profile_uid?",
				name: "MentorProfilePage",
				component: MentorProfilePage,
				// Mentees can view the profile too
			},
			{
				path: "profile-settings",
				name: "MentorProfileSettingsPage",
				component: MentorProfileSettingsPage,
				meta: { requires_mentor: true }
			},
			{
				path: "pending-requests",
				name: "MentorPendingRequestsPage",
				component: MentorPendingRequestsPage,
				meta: { requires_mentor: true }
			},
			{
				path: "my-mentees",
				name: "MyMenteesPage",
				component: MyMenteesPage,
				meta: { requires_mentor: true }
			},
			{
				path: "mentor-settings",
				name: "MentorSettingsPage",
				component: MentorSettingsPage,
				props: { is_editable: true },
				meta: { requires_mentor: true }
			}
		]
	},
	{
		path: "/mentee",
		name: "MenteePage",
		component: MenteeBasePage,
		meta: { requires_auth: true },

		children: [
			{
				path: "profile/:profile_uid?",
				name: "MenteeProfilePage",
				component: MenteeProfilePage,
				// meta: { requires_mentee: true }
			},
			{
				path: "profile-settings",
				name: "MenteeProfileSettingsPage",
				component: MenteeProfileSettingsPage,
				meta: { requires_mentee: true }
			},
			{
				path: "pending-requests",
				name: "MenteePendingRequestsPage",
				component: MenteePendingRequestsPage,
				meta: { requires_mentee: true }
			},
			{
				path: "my-mentors",
				name: "MyMentorsPage",
				component: MyMentorsPage,
				meta: { requires_mentee: true }
			},
			{
				path: "find-mentor",
				name: "FindMentorPage",
				component: FindMentorPage,
				meta: { requires_mentee: true }
			},
		]
	},
	{
		path: "/mentorship/:mentorship_uid",
		name: "MentorshipPage",
		component: MentorshipPage,
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
			next({ name: "LoginPage" })
		}
		else if (to.matched.some(record => record.meta.requires_mentor)) {
			if (!store.state.user.is_mentor) {
				next({ name: "HomePage" })
			}
			else {
				next()
			}
		}
		else if (to.matched.some(record => record.meta.requires_mentee)) {
			if (!store.state.user.is_mentee) {
				next({ name: "HomePage" })
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
			next({ name: "HomePage" })
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
