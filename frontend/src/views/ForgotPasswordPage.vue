<template>
<div class="container">
	<div class="columns is-centered">
		<div class="column is-5">
			<div class="title is-1 has-text-centered">
				Reset password
			</div>

			<FormErrors v-bind:errors="errors.detail" />

			<div v-if="email_exists">
				<InputBox input_type="text" v-model="token" v-bind:errors="errors.token"
						  label="Enter the forgot password token you received on your mail" icon="fas fa-check" />

				<InputBox input_type="password" v-model="new_password" v-bind:errors="errors.new_password"
						  label="New password" icon="fas fa-lock" />

				<InputBox input_type="password" v-model="confirm_new_password"
						  label="Confirm new password" icon="fas fa-lock" />

				<button v-on:click="change_password" class="button is-success is-fullwidth mt-5">Update</button>
			</div>
			<div v-else>
				<InputBox input_type="text" v-model="email" v-bind:errors="errors.email"
						  label="Email" icon="fas fa-envelope" />

				<button v-on:click="get_forgot_password_token" class="button is-success is-fullwidth mt-5">Get token</button>
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
			email: "",
			email_exists: false,

			token: "",
			new_password: "",
			confirm_new_password: "",

			errors: {}
		};
	},
	methods: {
		get_forgot_password_token() {
			axios
				.post("/api/users/user/forgot-password-token/", {
					email: this.email
				})
				.then(_ => {
					this.email_exists = true;
				})
				.catch(error => {
					this.errors = error.response ? error.response.data : {"detail": error.message};
				});
		},
		change_password() {
			if (this.new_password !== this.confirm_new_password) {
				this.errors.detail = "Passwords do not match";
				return;
			}

			axios
				.post("/api/users/user/forgot-password/", {
					token: this.token,
					new_password: this.new_password,
				})
				.then(_ => {
					this.$router.replace({ name : "LoginPage" });
				})
				.catch(error => {
					this.errors = error.response ? error.response.data : {"detail": error.message};
				});
		}
	}
}
</script>
