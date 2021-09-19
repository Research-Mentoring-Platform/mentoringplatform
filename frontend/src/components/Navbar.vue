<template>
<div class="hero-head pb-2">
	<nav class="navbar">
		<div class="container">
			<div class="navbar-brand">
				<router-link v-bind:to="{ name: 'HomePage' }" class="navbar-item">
					<span class="is-size-4 has-text-weight-bold">
						RMP
					</span>
				</router-link>

				<span v-on:click="show_navbar_burger_menu = !show_navbar_burger_menu"
					  v-bind:class="{ 'is-active': show_navbar_burger_menu }"
					  class="navbar-burger"
					  data-target="navbarMenuHeroB">
					<span></span>
					<span></span>
					<span></span>
				</span>
			</div>

			<div v-bind:class="{ 'is-active': show_navbar_burger_menu }" id="navbarMenuHeroB" class="navbar-menu">
				<div class="navbar-end">
					<div v-if="logged_in" class="navbar-item">
						<div class="navbar-item has-dropdown is-hoverable">
							<a class="navbar-link">
								<span class="icon">
									<i class="fas fa-user"></i>
								</span>
								<span class="has-text-weight-bold">
									{{ user.first_name }}
								</span>
							</a>

							<div class="navbar-dropdown is-boxed is-right">
								<div v-if="user.is_mentor">
									<router-link v-bind:to="{ name: 'MentorProfilePage', params: { profile_uid: user.profile_uid } }" class="navbar-item">
										My Profile
									</router-link>

									<router-link v-bind:to="{ name: 'MyMenteesPage' }" class="navbar-item">
										My Mentees
									</router-link>

									<router-link v-bind:to="{ name: 'MentorPendingRequestsPage' }" class="navbar-item">
										Pending Requests
									</router-link>

									<router-link v-bind:to="{ name: 'MentorProfileSettingsPage' }" class="navbar-item">
										Profile Settings
									</router-link>

									<router-link v-bind:to="{ name: 'MentorSettingsPage' }" class="navbar-item">
										Mentor Settings
									</router-link>
								</div>
								<div v-else-if="user.is_mentee">
									<router-link v-bind:to="{ name: 'MenteeProfilePage' }" class="navbar-item">
										My Profile
									</router-link>

									<router-link v-bind:to="{ name: 'MyMentorsPage' }" class="navbar-item">
										My Mentors
									</router-link>

									<router-link v-bind:to="{ name: 'FindMentorPage' }" class="navbar-item">
										Find Mentor
									</router-link>

									<router-link v-bind:to="{ name: 'MenteePendingRequestsPage' }" class="navbar-item">
										Pending Requests
									</router-link>

									<router-link v-bind:to="{ name: 'MenteeProfileSettingsPage' }" class="navbar-item">
										Profile Settings
									</router-link>
								</div>

								<router-link v-bind:to="{ name: 'ChangePasswordPage', params: { profile_uid: user.profile_uid } }" class="navbar-item">
									Change Password
								</router-link>

								<hr class="navbar-divider">

								<a v-on:click="logout" class="navbar-item">
									<span class="icon">
										<i class="fas fa-sign-out-alt"></i>
									</span>
									<span>Logout</span>
								</a>
							</div>
						  </div>
					</div>
					<div v-else class="navbar-item">
						<router-link v-bind:to="{ name: 'LoginPage' }" class="navbar-item">
							<span class="icon">
								<i class="fas fa-sign-in-alt"></i>
							</span>
							<span>Login</span>
						</router-link>

						<div class="navbar-item has-dropdown is-hoverable pl-2">
							<a class="navbar-link">
								<span class="icon pr-1">
									<i class="fas fa-user-plus"></i>
								</span>
								<span>Register</span>
							</a>

							<div class="navbar-dropdown">
								<router-link v-bind:to="{ name: 'RegisterMentorPage' }" class="navbar-item">
									As Mentor
								</router-link>
								<router-link v-bind:to="{ name: 'RegisterMenteePage' }" class="navbar-item">
									As Mentee
								</router-link>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</nav>
</div>
</template>


<script>
import { mapGetters, mapState } from "vuex";

export default {
	computed: {
		...mapGetters({
			logged_in: "logged_in"
		}),
		...mapState({
			user: "user"
		})
	},
	data() {
		return {
			show_navbar_burger_menu: false
		};
	},
	methods: {
		logout() {
			this.$store.dispatch("logout_user");
			this.$router.replace({ name: "HomePage" });
		}
	}
}
</script>
