<template>
<div style="width: 100%">
	<div class="container">
		<div class="columns is-centered">
			<div class="column is-one-third">

				<div class="title is-1 has-text-centered">
					<span v-if="register_as_mentor">
						Be a Mentor
					</span>
					<span v-else>
						Be a Mentee
					</span>
				</div>

				<div>
					<InputBox input_type="text" v-model="user.first_name" v-bind:errors="errors.first_name"
							  placeholder="First name" icon="fas fa-user-circle" />

					<InputBox input_type="text" v-model="user.last_name" v-bind:errors="errors.last_name"
							  placeholder="Last name" icon="fas fa-user-circle" />

					<InputBox input_type="text" v-model="user.username" v-bind:errors="errors.username"
							  placeholder="Username" icon="fas fa-user" />

					<InputBox input_type="text" v-model="user.email" v-bind:errors="errors.email"
							  placeholder="Email" icon="fas fa-envelope" />

					<InputBox input_type="date" v-model="user.date_of_birth" v-bind:errors="errors.date_of_birth"
							  icon="fas fa-calendar" />

					<InputBox input_type="password" v-model="user.password" v-bind:errors="errors.password"
							  placeholder="Password" icon="fas fa-lock" />

					<InputBox input_type="password" v-model="confirm_password" v-bind:errors="errors.confirm_password"
							  placeholder="Confirm password" icon="fas fa-lock" />

					<div class="has-text-centered has-text-weight-bold pt-3 pb-5">
						By registering you agree to the
						<a v-on:click="terms_and_conditions_modal.show = true" class="hyperlink">
							Terms & Conditions
						</a>
					</div>

					<button v-on:click="register" class="button is-fullwidth is-success">Register</button>
				</div>

			</div>
		</div>
	</div>

	<div v-bind:class="{ 'is-active': terms_and_conditions_modal.show }" id="terms_and_conditions-modal" class="modal">
		<div class="modal-background" v-on:click="terms_and_conditions_modal.show=false"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Terms & Conditions</p>
				<button class="delete" aria-label="close" v-on:click="terms_and_conditions_modal.show = !terms_and_conditions_modal.show"></button>
			</header>

			<section class="modal-card-body px-0 pt-0">
				<div class="content">
					<ul>
						<li class="py-1" v-for="tnc in terms_and_conditions_modal.content.terms_and_conditions">
							{{ tnc }}
						</li>
					</ul>
				</div>
			</section>

			<footer class="modal-card-foot">
				<div class="columns" style="width: 100%;">
					<div class="column has-text-right">
						<button v-on:click="terms_and_conditions_modal.show=false" class="button">Close</button>
					</div>
				</div>
			</footer>
		</div>
	</div>
</div>
</template>


<script>
import axios from "../api/my-axios";
import InputBox from "./FormHelpers/InputBox";
import FormErrors from "./FormHelpers/FormErrors";

export default {
	name: "Register",
	components: {
		InputBox,
		FormErrors
	},
	props: {
		register_as_mentor: {
			type: Boolean,
			required: true
		}
	},
	data() {
		return {
			terms_and_conditions_modal: {
				show: false,
				content: {
					terms_and_conditions: [
						"While the mentee is looking for guidance from you, please treat the mentee with respect and follow the mentoring schedule you agree with the mentee.",
						"Mentoring is exclusively to help the mentees in their research. Provide feedback on the mentee's work and ideas. Any ideas shared/discussed/given to the mentees, mentees have full right to use the idea as their own.",
						"Ideas of mentees cannot be used or discussed with anyone else by the mentor. The mentor cannot work on research problems the mentee discusses with the mentor.",
						"Mentee has the complete right to use or not use any suggestion/advice given.",
						"Keep mentorship about research and related issues like career, and keep other issues (e.g. personal) outside the scope.",
					]
				}
			},

			user: {
				first_name: "",
				last_name: "",
				username: "",
				email: "",
				date_of_birth: "",
				password: "",
				is_mentor: false,
				is_mentee: false
			},
			confirm_password: "",
			errors: {},
			max_dob: new Date().toISOString().split("T")[0]
		};
	},
	methods: {
		register() {
			if (this.user.password !== this.confirm_password) {
				this.errors.confirm_password = "Passwords do not match";
				return;
			}

			this.user.is_mentor = this.register_as_mentor;
			this.user.is_mentee = !this.register_as_mentor;

			axios
				.post("/api/users/user/", this.user)
				.then(_ => {
					this.$router.replace({ name: "VerifyToken" });
				})
				.catch(error => {
					this.errors = error.response.data;
				});
		}
	}
}
</script>