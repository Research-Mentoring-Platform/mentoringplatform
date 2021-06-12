<template>
	<div class="hero-body">
		<div class="container">
			<div class="columns is-centered p-5">
				<div class="column is-one-third has-text-left">

					<div class="title is-3 has-text-centered">
						<span>
							Fill your Profile!
						</span>
					</div>

					<div class="field">
						<label class="label">Designation</label>
						<div class="control">
							<div class="select">
								<select>
									<option>Select dropdown</option>
									<option>With options</option>
								</select>
							</div>
						</div>
					</div>

					<div class="field">
						<label class="label">Department</label>
						<div class="control">
							<div class="select">
								<select>
									<option>Select dropdown</option>
									<option>With options</option>
								</select>
							</div>
						</div>
					</div>

					<div class="field">
						<label class="label">Discipline</label>
						<div class="control">
							<div class="select">
								<select>
									<option>Select dropdown</option>
									<option>With options</option>
								</select>
							</div>
						</div>
					</div>

					<div class="field">
						<label class="label">Specialization</label>
						<div class="control">
							<div class="select">
								<select>
									<option>Select dropdown</option>
									<option>With options</option>
								</select>
							</div>
						</div>
					</div>

					<div class="title is-3 has-text-centered">
						<span>
							Education
						</span>
						<button class="button is-primary"
								data-toggle="modal"
								data-target="#tnc-modal">
							<i class="fa fa-plus"></i>
						</button>

					</div>



					<br/>

					<div class="control">
						<button class="button is-fullwidth is-success" v-on:click="register">Submit</button>
					</div>
				</div>
			</div>
		</div>
	</div>

	<div id="tnc-modal" class="modal" v-bind:class="{ 'is-active': show_tnc_dialog }">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Add Education</p>
				<button class="delete" aria-label="close" v-on:click="show_tnc_dialog = !show_tnc_dialog"></button>
			</header>
			<section class="modal-card-body">
				<div class="content">

				</div>
			</section>
			<footer class="modal-card-foot">
				<button v-on:click="show_tnc_dialog = !show_tnc_dialog" class="button">Cancel</button>
			</footer>
		</div>
	</div>
</template>


<script>
// import axios from 'axios';
import axios from '../../api/my-axios'

export default {
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
				is_mentor: false,
				is_mentee: false
			},
			max_dob: new Date().toISOString().split("T")[0]
		};
	},
	methods: {

	}
}
</script>