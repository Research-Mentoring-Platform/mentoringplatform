<template>
<div class="container">
	<div class="columns is-centered">
		<div class="column is-5">
			<div class="title is-1 has-text-centered">
				Verify account
			</div>

			<InputBox input_type="text" v-model="token" label="Enter verification token" icon="fas fa-check" />

			<FormErrors v-bind:errors="errors.detail" />

			<FormErrors v-bind:errors="errors.non_field_errors" />

			<button v-on:click="verify_token" class="button is-success is-fullwidth">Submit</button>
		</div>
	</div>
</div>
</template>

<script>
import InputBox from "../components/FormHelpers/InputBox";
import axios from "../api/my-axios";
import FormErrors from "../components/FormHelpers/FormErrors";
export default {
	components: {
		FormErrors,
		InputBox
	},
	data() {
		return {
			token: "",

			errors: {}
		};
	},
	methods: {
		verify_token() {
			axios
				.get(`/api/users/user/verify-email/${this.token}`)
				.then(response => {
					this.$router.replace({ name: "LoginPage" });
				})
				.catch(error => {
					this.errors = error.response ? error.response.data : {"detail": error.message};
				});
		}
	}
}
</script>

<style scoped>

</style>