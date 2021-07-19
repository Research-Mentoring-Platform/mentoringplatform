<template>
<div>
	<!-- HEADING -->
	<div class="title has-text-centered mb-5">
		Education
		<button v-if="allow_editing" v-on:click="educations.modals.education.show=true" class="button is-rounded is-primary p-4">
			<span class="icon">
				<i class="fa fa-plus"></i>
			</span>
		</button>
	</div>

	<FormErrors v-bind:errors="educations.errors.detail" />


	<!-- EDUCATION RECORDS -->
	<ul v-if="educations.data.length === 0">
		<li class="box has-text-centered is-centered has-text-weight-bold has-background-white">
			No data
		</li>
	</ul>
	<ul v-else class="px-3" style="max-height: min(500px, 60vh); overflow-y: auto;">
		<li v-for="(education, index) in educations.data" class="pb-5">
			<EducationBox v-bind:is_editable="allow_editing"
						  v-bind:education="education"
						  v-on:edit_education="edit_education(index)"
						  v-on:show_education_details="show_education_details(index)" />
		</li>
	</ul>


	<!-- VIEW PARTICULAR EDUCATION DETAILS MODAL -->
	<div v-bind:class="{ 'is-active': educations.modals.details.show }" class="modal">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Education details</p>
				<button v-on:click="educations.modals.details.show=false" class="delete" aria-label="close"></button>
			</header>

			<div class="modal-card-body">
				<p class="content is-medium">{{ educations.modals.details.content.details }}</p>
			</div>
		</div>
	</div>


	<!-- ADD/UPDATE EDUCATION MODAL -->
	<div v-if="allow_editing" v-bind:class="{ 'is-active': educations.modals.education.show }" class="modal">
		<div class="modal-background" v-on:click="clear_and_close_education_modal"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<span v-if="educations.edit_index === -1" class="modal-card-title">Add Education</span>
				<span v-else class="modal-card-title">Edit Education</span>
				<button v-on:click="clear_and_close_education_modal" class="delete" aria-label="close"></button>
			</header>

			<section class="modal-card-body has-text-left">
				<InputBox input_type="text" v-model="educations.modals.education.content.qualification"
						  v-bind:errors="educations.modals.education.errors.qualification"
						  label="Qualification" icon="fas fa-graduation-cap" />

				<InputBox input_type="text" v-model="educations.modals.education.content.organization"
						  v-bind:errors="educations.modals.education.errors.organization"
						  label="Organization" icon="fas fa-school" />

				<div class="columns pb-0">
					<div class="column">
						<InputBox input_type="month" v-model="educations.modals.education.content.start_date"
								  v-bind:errors="educations.modals.education.errors.start_date"
								  label="Start Date" icon="fas fa-calendar" />
					</div>

					<div class="column">
						<InputBox input_type="month" v-model="educations.modals.education.content.end_date"
								  v-bind:errors="educations.modals.education.errors.end_date"
								  v-bind:disabled="educations.modals.education.is_ongoing"
								  label="End Date" icon="fas fa-calendar"/>

						<input v-model="educations.modals.education.is_ongoing" class="checkbox" type="checkbox"> Is ongoing
					</div>
				</div>

				<InputBox input_type="textarea" v-model="educations.modals.education.content.details"
						  v-bind:errors="educations.modals.education.errors.details"
						  label="Details" icon="fas fa-info-circle"/>

				<FormErrors v-bind:errors="educations.modals.education.errors.detail" />
				<FormErrors v-bind:errors="educations.modals.education.errors.non_field_errors" />
			</section>

			<footer class="modal-card-foot">
				<div class="columns is-mobile" style="width: 100%;">
					<div class="column is-narrow has-text-left">
						<button v-if="educations.edit_index >= 0" v-on:click="delete_education" class="button is-danger">Delete</button>
					</div>

					<div class="column has-text-right">
						<button v-if="educations.edit_index >= 0" v-on:click="update_education" class="button is-success">Update</button>
						<button v-else v-on:click="add_education" class="button is-success">Add</button>

						<button v-on:click="clear_and_close_education_modal" class="button">Cancel</button>
					</div>
				</div>
			</footer>
		</div>
	</div>
</div>
</template>


<script>
import { mapGetters, mapState } from "vuex";
import axios from "../../api/my-axios";
import EducationBox from "./EducationBox";
import InputBox from "../FormHelpers/InputBox";
import FormErrors from "../FormHelpers/FormErrors";

export default {
	components: {
		EducationBox,
		InputBox,
		FormErrors
	},
	props: {
		is_editable: {
			type: Boolean,
			default: false
		},
		profile_uid: {
			type: String,
			default: null
		},
		user_role: { // "mentor" or "mentee"
			type: String,
			default: null
		}
	},
	computed: {
		...mapState({
			user: "user"
		}),
		...mapGetters({
			role: "role" // "mentor" or "mentee"
		})
	},
	data() {
		return {
			allow_editing: false,
			to_show_user_role: this.user_role,
			to_show_profile_uid: this.profile_uid,

			educations: {
				request_token: {
					// mentor or mentee: ""
				},

				errors: {},

				edit_index: -1,

				modals: {
					details: {
						show: false,
						content: {
							details: ""
						},
						errors: {}
					},

					education: {
						show: false,
						is_ongoing: false,
						content: {
							qualification: "", // "" is important, as null=True is not allowed in back-end
							organization: "",
							start_date: "",
							end_date: "",
							details: ""
						},
						errors: {}
					}
				},

				data: [
					// {
					// 	uid: "",
					// 	qualification: "", // "" is important, as null=True is not allowed in back-end
					// 	organization: "",
					// 	start_date: "",
					// 	end_date: "",
					// 	details: ""
					// }
				]
			}
		};
	},
	created()
	{
		this.to_show_profile_uid = this.profile_uid ? this.profile_uid : this.user.profile_uid;
		this.to_show_user_role = this.user_role ? this.user_role : this.role;
		this.allow_editing = this.is_editable ? (this.to_show_profile_uid === this.user.profile_uid) : false;

		this.educations.request_token[this.role] = this.user.profile_uid;
		this.get_educations();
	},
	methods: {
		clear_education_modal()
		{
			for (const key in this.educations.modals.education.content) {
				this.educations.modals.education.content[key] = "";
			}
			this.educations.modals.education.is_ongoing = false;

			this.educations.edit_index = -1; // Important
			this.educations.modals.education.errors = {};
		},

		clear_and_close_education_modal()
		{
			this.clear_education_modal();
			this.educations.modals.education.show = false;
		},

		show_education_details(index)
		{
			if (index >= this.educations.data.length) { return; }
			this.educations.modals.details.content.details = this.educations.data[index].details;
			this.educations.modals.details.show = true;
		},

		get_educations()
		{
			axios
				.get(`/api/${this.to_show_user_role}/education/`, {
					params: {
						[this.to_show_user_role]: this.to_show_profile_uid
					}
				})
				.then(response => {
					this.educations.data = response.data;
				})
				.catch(error => {
					this.educations.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		add_education()
		{
			if (!this.allow_editing) { return; }

			if (this.educations.modals.education.is_ongoing) {
				this.educations.modals.education.content.end_date = null;
			}

			axios
				.post(`/api/${this.role}/education/`, {
					...this.educations.modals.education.content,
					...this.educations.request_token,
				})
				.then(_ => {
					this.get_educations();
					this.clear_and_close_education_modal();
				})
				.catch(error => {
					this.educations.modals.education.errors = error.response.data;
				});
		},

		edit_education(index)
		{
			if (!this.allow_editing) { return; }
			if (index < 0 || index >= this.educations.data.length) { return; }

			this.educations.edit_index = index;
			for (const key in this.educations.modals.education.content) {
				this.educations.modals.education.content[key] = this.educations.data[this.educations.edit_index][key];
			}

			this.educations.modals.education.is_ongoing = (this.educations.modals.education.content.end_date === null);
			this.educations.modals.education.show = true;
		},

		update_education()
		{
			if (!this.allow_editing) { return; }
			if (this.educations.edit_index < 0 || this.educations.edit_index >= this.educations.data.length) { return; }

			if (this.educations.modals.education.is_ongoing) {
				this.educations.modals.education.content.end_date = null;
			}
			else if (this.educations.modals.education.content.end_date === null) {
				this.educations.modals.education.content.end_date = "";  // So that the backend throws an error (incorrect date format)
			}

			axios
				.put(`/api/${this.role}/education/${this.educations.data[this.educations.edit_index].uid}/`, {
					...this.educations.modals.education.content,
					...this.educations.request_token,
				})
				.then(_ => {
					this.get_educations();
					this.clear_and_close_education_modal();
				})
				.catch(error => {
					this.educations.modals.education.errors = error.response.data;
				});
		},

		delete_education()
		{
			if (!this.allow_editing) { return; }
			if (this.educations.edit_index < 0 || this.educations.edit_index >= this.educations.data.length) { return; }

			axios
				.delete(`/api/${this.role}/education/${this.educations.data[this.educations.edit_index].uid}/`, {
					data: {
						...this.educations.request_token
					}
				})
				.then(_ => { // No need to get educations again as order remains unchanged
					this.educations.data.splice(this.educations.edit_index, 1);
					this.clear_and_close_education_modal();
				})
				.catch(error => {
					this.educations.modals.education.errors = error.response.data;
				});
		}
	}
}
</script>
