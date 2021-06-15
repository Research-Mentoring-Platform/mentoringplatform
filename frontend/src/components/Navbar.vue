<template>
<div class="hero-head">
	<nav class="navbar">
		<div class="container">
			<div class="navbar-brand">
				<router-link v-bind:to="{ name: 'Home' }" class="navbar-item">
					<span class="is-size-3 has-text-weight-bold">
						RMP
					</span>
				</router-link>

				<span v-on:click="show_nav_bar_menu = !show_nav_bar_menu"
					  v-bind:class="{ 'is-active': show_nav_bar_menu }"
					  class="navbar-burger"
					  data-target="navbarMenuHeroB">
					<span></span>
					<span></span>
					<span></span>
				</span>
			</div>

			<div id="navbarMenuHeroB" class="navbar-menu" v-bind:class="{ 'is-active': show_nav_bar_menu }">
				<div class="navbar-end">
					<div v-if="logged_in" class="navbar-item">
						<div class="navbar-item has-dropdown is-hoverable">
							<a class="navbar-link">
								First Name
							</a>

							<div class="navbar-dropdown is-right">
								<router-link v-bind:to="{ name: 'Profile' }" class="navbar-item">
									Profile
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
import { mapGetters } from "vuex";

export default {
	data() {
		return {
			show_nav_bar_menu: false
		};
	},
	computed: {
		...mapGetters({
			logged_in: "logged_in"
		})
	},
	methods: {
		logout() {
			this.$store.dispatch("logout");
			this.$router.replace({ name: "Home" });
		}
	}
}
</script>
