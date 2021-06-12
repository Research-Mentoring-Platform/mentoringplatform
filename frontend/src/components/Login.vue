<template>
	<transition>
	<div class="hero-body">
		<div class="container">
			<div class="columns is-centered">
				<div class="column is-one-third">
					<div class="title is-1 has-text-centered">
						Login
					</div>

					<div class="field">
<!--						<label class="label">Email</label>-->
						<p class="control has-icons-left">
							<input v-model="user.email" class="input" type="email" placeholder="Email">
							<span class="icon is-small is-left">
								<i class="fas fa-envelope"></i>
							</span>
						</p>
					</div>

					<div class="field">
<!--						<label class="label">Password</label>-->
						<p class="control has-icons-left">
							<input v-model="user.password" v-on:keyup.enter="login" class="input" type="password" placeholder="Password">
							<span class="icon is-small is-left">
								<i class="fas fa-lock"></i>
							</span>
						</p>
					</div>

					<br/>

					<div class="control">
						<button v-on:click="login" class="button is-success is-fullwidth">
							Login
						</button>
					</div>

					<div class="pt-3 has-text-centered">
						<a class="has-text-centered" style="color:dodgerblue;">
							Forgot password?
						</a>
					</div>

					<div class="pt-3 has-text-centered">
						Don't have an account? Register as a
						<router-link v-bind:to="{ name: 'RegisterMentor' }" style="color:dodgerblue;">
							mentor
						</router-link>
						or
						<router-link v-bind:to="{ name: 'RegisterMentee' }" style="color: dodgerblue;">
							mentee
						</router-link>
						.
					</div>
				</div>
			</div>
		</div>
	</div></transition>
</template>


<script>
import axios from "../api/my-axios";

export default {
	data() {
		return {
			user: {
				email: "",
				password: ""
			}
		}
	},
	methods: {
		login() {
			axios.post('/api/users/token/', this.user)
			.then((response) => {
				this.$store.commit('update_local_storage', response.data);
				this.$router.replace({ name: 'MenteeProfile' });
			})
			.catch((error) => {
				console.error(error);
			});
		}
	}
}
</script>
