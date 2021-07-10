<template>
<div class="container">
	<InputBox input_type="text" v-model="token" label="Enter token" />
	<button v-on:click="verify_token" class="button is-success">Submit</button>
	<FormErrors v-bind:errors="errors.detail" />
	<FormErrors v-bind:errors="errors.non_field_errors" />
</div>
</template>

<script>
import InputBox from "../components/FormHelpers/InputBox";
import axios from "../api/my-axios";
import FormErrors from "../components/FormHelpers/FormErrors";
export default {
	name: "VerifyToken",
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
					console.log("Done!");
					this.$router.replace({ name: "Login" });
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