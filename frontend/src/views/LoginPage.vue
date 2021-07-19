<template>
<div class="container">
	<div class="columns is-centered">
		<div class="column is-one-third">
			<div class="title is-1 has-text-centered">
				Login
			</div>

			<FormErrors v-bind:errors="errors.detail" />
			<FormErrors v-bind:errors="errors.non_field_errors" />

			<div>
				<InputBox input_type="email" v-model="user.email" v-bind:errors="errors.email" v-on:keyup.enter="login"
						  placeholder="Email" icon="fas fa-envelope" />

				<InputBox input_type="password" v-model="user.password" v-bind:errors="errors.password" v-on:keyup.enter="login"
						  placeholder="Password" icon="fas fa-lock" />

				<button v-on:click="login" class="button is-success is-fullwidth">
					Login
				</button>
			</div>

			<div class="pt-3 has-text-centered">
				<router-link v-bind:to="{ name: 'ForgotPasswordPage' }" class="has-text-centered hyperlink">
					Forgot password?
				</router-link>
			</div>

			<div class="pt-3 has-text-centered">
				Don't have an account? Register as a
				<router-link v-bind:to="{ name: 'RegisterMentorPage' }" class="hyperlink">
					mentor
				</router-link>
				or
				<router-link v-bind:to="{ name: 'RegisterMenteePage' }" class="hyperlink">
					mentee
				</router-link>
				.
			</div>
		</div>
	</div>
</div>
</template>


<script>
import axios from "../api/my-axios";
import InputBox from "../components/FormHelpers/InputBox";
import FormErrors from "../components/FormHelpers/FormErrors";

export default {
	components: {
		InputBox,
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
				.then(response => {
					this.$store.commit("set_token", response.data.token);

					// Get user details
					axios
						.get(`/api/users/user/${response.data.uid}/`)
						.then(user_data => {
							user_data.data.profile_uid = response.data.profile_uid;
							this.$store.commit("set_user", user_data.data);

							// TODO Also check if profile already completed. If so, redirect to Home instead
							if (user_data.data.is_mentor) {
								this.$router.replace({ name: "MentorProfileSettingsPage" });
							}
							else if (user_data.data.is_mentee) {
								this.$router.replace({ name: "MenteeProfileSettingsPage" });
							}
						})
						.catch(error => {
							this.errors = error.response ? error.response.data : {"detail": error.message};
						});
				})
				.catch(error => {
					this.errors = error.response ? error.response.data : {"detail": error.message};
				});
		}
	}
}
</script>
