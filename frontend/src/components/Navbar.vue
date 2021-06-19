<template>
<div class="hero-head pb-2">
	<nav class="navbar">
		<div class="container">
			<div class="navbar-brand">
				<router-link v-bind:to="{ name: 'Home' }" class="navbar-item">
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

			<div id="navbarMenuHeroB" class="navbar-menu" v-bind:class="{ 'is-active': show_navbar_burger_menu }">
				<div class="navbar-end">
					<div v-if="logged_in" class="navbar-item">
						<div class="navbar-item has-dropdown is-hoverable">
							<a class="navbar-link">
								<span class="icon">
									<i class="fas fa-user"></i>
								</span>
								<span class="has-text-weight-bold">
									{{ current_user.first_name }}
								</span>
							</a>

							<div class="navbar-dropdown is-boxed is-right">
								<router-link v-if="current_user.is_mentor" v-bind:to="{ name: 'MentorProfile' }" class="navbar-item">
									Profile
								</router-link>
								<router-link v-else-if="current_user.is_mentee" v-bind:to="{ name: 'MenteeProfile' }" class="navbar-item">
									Profile
								</router-link>

								<router-link v-if="current_user.is_mentee" v-bind:to="{ name: 'FindMentor' }" class="navbar-item">
									Find Mentor
								</router-link>

								<hr class="navbar-divider">

								<a v-on:click="logout" class="navbar-item">
									Logout
								</a>
							</div>
						  </div>
					</div>
					<div v-else class="navbar-item">
						<router-link v-bind:to="{ name: 'Login' }" class="navbar-item">
							Login
						</router-link>

						<div class="navbar-item has-dropdown is-hoverable">
							<a class="navbar-link">
								Register
							</a>

							<div class="navbar-dropdown">
								<router-link v-bind:to="{ name: 'RegisterMentor' }" class="navbar-item">
									As Mentor
								</router-link>
								<router-link v-bind:to="{ name: 'RegisterMentee' }" class="navbar-item">
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
	data() {
		return {
			show_navbar_burger_menu: false
		};
	},
	computed: {
		...mapGetters({
			logged_in: "logged_in"
		}),
		...mapState({
			current_user: "current_user"
		})
	},
	methods: {
		logout() {
			this.$store.dispatch("logout_user");
			this.$router.replace({ name: "Home" });
		}
	}
}
</script>
