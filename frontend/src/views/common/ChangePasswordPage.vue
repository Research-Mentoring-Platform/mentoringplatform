<template>
<div class="container">
	<div class="columns is-centered">
		<div class="column is-5">
			<div class="title has-text-centered">
				Change password
			</div>

			<InputBox input_type="password" v-model="current_password"
					  label="Current password" icon="fas fa-lock" />

			<InputBox input_type="password" v-model="new_password"
					  label="New password" icon="fas fa-lock" />

			<InputBox input_type="password" v-model="confirm_new_password"
					  label="Confirm new password" icon="fas fa-lock" />

			<FormErrors v-bind:errors="errors.detail" />

			<button v-on:click="change_password" class="button is-success is-fullwidth">Update</button>
		</div>
	</div>
</div>
</template>

<script>
import { mapState } from "vuex";
import axios from "../../api/my-axios";
import InputBox from "../../components/FormHelpers/InputBox";
import FormErrors from "../../components/FormHelpers/FormErrors";

export default {
	components: {
		InputBox,
		FormErrors
	},
	computed: {
		...mapState({
			user: "user"
		}),
	},
	data() {
		return {
			current_password: "",
			new_password: "",
			confirm_new_password: "",

			errors: {}
		};
	},
	methods: {
		change_password() {
			if (this.new_password !== this.confirm_new_password) {
				this.errors.detail = "Passwords do not match";
				return;
			}

			axios
				.post(`/api/users/user/${this.user.uid}/change-password/`, {
					current_password: this.current_password,
					new_password: this.new_password,
				})
				.then(_ => {
					this.$router.replace({ name : "HomePage" });
				})
				.catch(error => {
					this.errors = error.response ? error.response.data : {"detail": error.message};
				})
		}
	}
}
</script>
