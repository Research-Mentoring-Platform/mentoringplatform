<template>
	<div class="hero-body">
		<div class="container">
			<div class="columns is-centered p-5">
				<div class="column is-one-third">

					<div class="title is-1 has-text-centered">
						<span v-if="register_as_mentor === true">
							Be a Mentor
						</span>
						<span v-else>
							Be a Mentee
						</span>
					</div>

					<div class="field">
						<label class="label">First Name</label>
						<div class="control">
							<input v-model="user.first_name" class="input" type="text" placeholder="First name">
						</div>
					</div>

					<div class="field">
						<label class="label">Last Name</label>
						<div class="control">
							<input v-model="user.last_name" class="input" type="text" placeholder="Last name">
						</div>
					</div>

					<div class="field">
						<label class="label">Username</label>
<!--						<div class="control has-icons-left has-icons-right">-->
						<div class="control has-icons-left">
							<input v-model="user.username" class="input" type="text" placeholder="Username">
							<span class="icon is-small is-left">
								<i class="fas fa-user"></i>
							</span>
						</div>
					</div>

					<div class="field">
						<label class="label">Email</label>
						<div class="control has-icons-left">
							<input v-model="user.email" class="input" type="email" placeholder="Email">
							<span class="icon is-small is-left">
							  	<i class="fas fa-envelope"></i>
							</span>
						</div>
					</div>

					<div class="field">
<!--						<label class="label">Date of Birth</label>-->
						<div class="control has-icons-left">
							<input v-model="user.date_of_birth" class="input" type="date" v-bind:max="max_dob">
							<span class="icon is-small is-left">
							  	<i class="fas fa-calendar"></i>
							</span>
						</div>
					</div>

					<div class="field">
						<label class="label">Password</label>
						<div class="control">
							<input v-model="user.password" class="input" type="password" placeholder="Password">
						</div>
					</div>

					<div class="field">
						<label class="label">Confirm Password</label>
						<div class="control">
							<input v-model="confirm_password" class="input" type="password" placeholder="Confirm password">
						</div>
						<p class="help is-danger" v-if="confirm_password.length > 0 && user.password !== confirm_password">
							Passwords do not match!
						</p>
					</div>

					<div class="pt-3 has-text-centered">
						<strong>
							By registering you agree to the
							<a
								v-on:click="show_tnc_dialog = !show_tnc_dialog"
							    data-toggle="modal"
							    data-target="#tnc-modal"
								style="color: dodgerblue;">
								Terms & Conditions
							</a>
						</strong>
					</div>

					<br/>

					<div class="control">
						<button class="button is-fullwidth is-success" v-on:click="register">Register</button>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div id="tnc-modal" class="modal" v-bind:class="{ 'is-active': show_tnc_dialog }">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Terms & Conditions</p>
				<button class="delete" aria-label="close" v-on:click="show_tnc_dialog = !show_tnc_dialog"></button>
			</header>
			<section class="modal-card-body">
				<ul>
					<li>
						While the mentee is looking for guidance from you, please treat the mentee with respect and follow the mentoring schedule you agree with the mentee.
					</li>
					<li>
						Mentoring is exclusively to help the mentees in their research. Provide feedback on the mentee's work and ideas. Any ideas shared/discussed/given to the mentees, mentees have full right to use the idea as their own.
					</li>
					<li>
						Ideas of mentees cannot be used or discussed with anyone else by the mentor. The mentor cannot work on research problems the mentee discusses with the mentor.
					</li>
					<li>
						Mentee has the complete right to use or not use any suggestion/advice given.
					</li>
					<li>
						Keep mentorship about research and related issues like career, and keep other issues (e.g. personal) outside the scope.
					</li>
				</ul>
			</section>
			<footer class="modal-card-foot">
				<button class="button" v-on:click="show_tnc_dialog = !show_tnc_dialog">Cancel</button>
			</footer>
		</div>
	</div>
</template>


<script>
// import axios from 'axios';
import axios from '../api/my-axios'

export default {
	props: {
		request_url: {
			type: String,
			required: true
		},
		register_as_mentor: {
			type: Boolean,
			required: true
		}
	},
	data() {
		return {
			show_tnc_dialog: false,
			user: {
				first_name: "",
				last_name: "",
				username: "",
				email: "",
				date_of_birth: "",
				password: "",
			},
			confirm_password: ""
		};
	},
	methods: {
		register() {
			this.user.is_mentor = this.register_as_mentor;
			this.user.is_mentee = !this.register_as_mentor;

			if (this.user.password !== this.confirm_password) { return; }

			axios.post("/api/users/user/", this.user)
			.then((response) => {
				this.$router.replace({ name: 'Login' });
			})
			.catch((error) => {
				console.error(error);
			});
		}
	}
}
</script>