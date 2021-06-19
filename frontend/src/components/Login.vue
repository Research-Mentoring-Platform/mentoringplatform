<template>
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
				<FormErrors v-bind:errors="errors.email" />
			</div>

			<div class="field">
<!--						<label class="label">Password</label>-->
				<p class="control has-icons-left">
					<input v-model="user.password" v-on:keyup.enter="login" class="input" type="password" placeholder="Password">
					<span class="icon is-small is-left">
						<i class="fas fa-lock"></i>
					</span>
				</p>
				<FormErrors v-bind:errors="errors.password" />
			</div>

			<FormErrors v-bind:errors="errors.detail" />
			<FormErrors v-bind:errors="errors.non_field_errors" />

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
				<router-link v-bind:to="{ name: 'RegisterMentor' }" class="hyperlink">
					mentor
				</router-link>
				or
				<router-link v-bind:to="{ name: 'RegisterMentee' }" class="hyperlink">
					mentee
				</router-link>
				.
			</div>
		</div>
	</div>
</div>
</template>


<script>
import axios from "@/api/my-axios";
import FormErrors from "@/components/FormErrors";

export default {
	components: {
		FormErrors
	},
	data() {
		return {
			user: {
				email: "",
				password: ""
			},

			errors: {}
		};
	},
	methods: {
		login()
		{
			// Get token
			axios
				.post("/api/users/token/", this.user)
				.then(resp => {
					this.$store.commit("set_token", resp.data.token);

					// Get user details
					axios
						.get(`/api/users/user/${resp.data.uid}`)
						.then(user_data => {
							user_data.data.profile_uid = resp.data.profile_uid;
							this.$store.commit("set_current_user", user_data.data);

							// TODO Also check if profile already completed. If so, redirect to Home instead
							if (user_data.data.is_mentor) {
								this.$router.replace({ name: "MentorProfile" });
							}
							else if (user_data.data.is_mentee) {
								this.$router.replace({ name: "MenteeProfile" });
							}
						})
						.catch(error => {
							this.errors = error.response.data;
						});
				})
				.catch(error => {
					this.errors = error.response.data;
				});
		}
	}
}
</script>
