<template>
	<div class="hero-head">
		<nav class="navbar">
			<div class="container">
				<div class="navbar-brand">
					<router-link v-bind:to="{ name: 'Home' }" class="navbar-item">
						<img src="https://bulma.io/images/bulma-type-white.png" alt="Logo">
					</router-link>

					<span class="navbar-burger"
						  data-target="navbarMenuHeroB"
						  v-on:click="show_nav_bar_menu = !show_nav_bar_menu"
						  v-bind:class="{ 'is-active': show_nav_bar_menu }"
					>
						<span></span>
						<span></span>
						<span></span>
					</span>
				</div>

				<div id="navbarMenuHeroB" class="navbar-menu" v-bind:class="{ 'is-active': show_nav_bar_menu }">
					<div class="navbar-end">

						<div class="navbar-item has-dropdown is-hoverable">
							<a class="navbar-link" style="color: #0A0A0A">
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

						<router-link :to="{ name: 'Login' }" class="navbar-item">
							Login
						</router-link>

						<span class="navbar-item">
							<a class="button is-info is-inverted">
								<span class="icon">
									<i class="fab fa-github"></i>
								</span>
								<span>Download</span>
							</a>
						</span>
					</div>
				</div>
			</div>
		</nav>
	</div>
</template>


<script>
export default {
	data() {
		return {
			show_nav_bar_menu: false
		};
	},
	computed: {
		...mapGetters({
			logged_in: 'logged_in'
		})
	},
	methods: {
		logout() {
			this.$store.commit('destroy_token');
			this.$router.replace({ name: 'Home' });
		}
	}
}
</script>
