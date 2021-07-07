<template>
<div>
	<!-- HEADING -->
	<div class="title has-text-centered mb-5">
		Research
		<button v-if="allow_editing" v-on:click="researches.modals.research.show=true" class="button is-rounded is-primary p-4">
			<span class="icon">
				<i class="fa fa-plus"></i>
			</span>
		</button>
	</div>

	<FormErrors v-bind:errors="researches.errors.detail" />


	<!-- RESEARCH RECORDS -->
	<ul v-if="researches.data.length === 0">
		<li class="box has-text-centered is-centered has-text-weight-bold has-background-white">
			No data
		</li>
	</ul>
	<ul v-else class="px-3" style="max-height: min(600px, 60vh); overflow-y: auto;">
		<li v-for="(research, index) in researches.data" class="pb-5">
			<ResearchBox v-bind:is_editable="allow_editing"
						 v-bind:research="research"
						 v-on:edit_research="edit_research(index)"
						 v-on:show_research_details="show_research_details(index)" />
		</li>
	</ul>


	<!-- VIEW PARTICULAR RESEARCH DETAILS MODAL -->
	<div v-bind:class="{ 'is-active': researches.modals.details.show }" class="modal">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Research details</p>
				<button v-on:click="researches.modals.details.show=false" class="delete" aria-label="close"></button>
			</header>

			<div class="modal-card-body">
				<p class="content is-medium">{{ researches.modals.details.content.details }}</p>
			</div>
		</div>
	</div>


	<!-- ADD/UPDATE RESEARCH MODAL -->
	<div v-if="allow_editing" v-bind:class="{ 'is-active': researches.modals.research.show }" class="modal">
		<div class="modal-background" v-on:click="clear_and_close_research_modal"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<span v-if="researches.edit_index === -1" class="modal-card-title">Add Research</span>
				<span v-else class="modal-card-title">Edit Research</span>
				<button v-on:click="clear_and_close_research_modal" class="delete" aria-label="close"></button>
			</header>

			<section class="modal-card-body has-text-left">
				<InputBox input_type="text" v-model="researches.modals.research.content.title"
						  v-bind:errors="researches.modals.research.errors.title"
						  label="Title" icon="fas fa-heading" />

				<InputBox input_type="text" v-model="researches.modals.research.content.organization"
						  v-bind:errors="researches.modals.research.errors.organization"
						  label="Organization" icon="fas fa-school" />

				<div class="columns pb-0">
					<div class="column">
						<InputBox input_type="month" v-model="researches.modals.research.content.start_date"
								  v-bind:errors="researches.modals.research.errors.start_date"
								  label="Start Date" icon="fas fa-calendar" />
					</div>

					<div class="column">
						<InputBox input_type="month" v-model="researches.modals.research.content.end_date"
								  v-bind:errors="researches.modals.research.errors.end_date"
								  v-bind:disabled="researches.modals.research.is_ongoing"
								  label="End Date" icon="fas fa-calendar"/>

						<input v-model="researches.modals.research.is_ongoing" class="checkbox" type="checkbox"> Is ongoing
					</div>
				</div>

				<InputBox input_type="textarea" v-model="researches.modals.research.content.details"
						  v-bind:errors="researches.modals.research.errors.details"
						  label="Details" icon="fas fa-info-circle"/>

				<FormErrors v-bind:errors="researches.modals.research.errors.detail" />
				<FormErrors v-bind:errors="researches.modals.research.errors.non_field_errors" />
			</section>

			<footer class="modal-card-foot">
				<div class="columns is-mobile" style="width: 100%;">
					<div class="column is-narrow has-text-left">
						<button v-if="researches.edit_index >= 0" v-on:click="delete_research" class="button is-danger">Delete</button>
					</div>

					<div class="column has-text-right">
						<button v-if="researches.edit_index >= 0" v-on:click="update_research" class="button is-success">Update</button>
						<button v-else v-on:click="add_research" class="button is-success">Add</button>

						<button v-on:click="clear_and_close_research_modal" class="button">Cancel</button>
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
import ResearchBox from "./ResearchBox";
import InputBox from "../FormHelpers/InputBox";
import FormErrors from "../FormHelpers/FormErrors";

export default {
	name: "Research",
	components: {
		ResearchBox,
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

			researches: {
				request_token: {
					// mentee: ""
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

					research: {
						show: false,
						is_ongoing: false,
						content: {
							title: "", // "" is important, as null=True is not allowed in back-end
							organization: "",
							start_date: "",
							end_date: "",
							details: ""
						},
						errors: {}
					}
				},

				data: [
					// uid: "",
					// title: "", // "" is important, as null=True is not allowed in back-end
					// organization: "",
					// start_date: "",
					// end_date: "",
					// details: ""
				]
			}
		};
	},
	created()
	{
		this.to_show_profile_uid = this.profile_uid ? this.profile_uid : this.user.profile_uid;
		this.to_show_user_role = this.user_role ? this.user_role : this.role;
		this.allow_editing = this.is_editable ? (this.to_show_profile_uid === this.user.profile_uid) : false;

		this.researches.request_token[this.role] = this.user.profile_uid;
		this.get_researches();
	},
	methods: {
		clear_research_modal()
		{
			for (const key in this.researches.modals.research.content) {
				this.researches.modals.research.content[key] = "";
			}
			this.researches.modals.research.is_ongoing = false;

			this.researches.edit_index = -1; // Important
			this.researches.modals.research.errors = {};
		},

		clear_and_close_research_modal()
		{
			this.clear_research_modal();
			this.researches.modals.research.show = false;
		},

		show_research_details(index)
		{
			if (index >= this.researches.data.length) { return; }
			this.researches.modals.details.content.details = this.researches.data[index].details;
			this.researches.modals.details.show = true;
		},

		get_researches()
		{
			axios
				.get(`/api/${this.to_show_user_role}/research/`, {
					params: {
						[this.to_show_user_role]: this.to_show_profile_uid
					}
				})
				.then(response => {
					this.researches.data = response.data;
				})
				.catch(error => {
					this.researches.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		add_research()
		{
			if (!this.allow_editing) { return; }

			this.researches.modals.research.content.end_date = this.researches.modals.research.is_ongoing ? null : this.researches.modals.research.content.end_date;

			axios
				.post(`/api/${this.role}/research/`, {
					...this.researches.modals.research.content,
					...this.researches.request_token,
				})
				.then(_ => {
					this.get_researches();
					this.clear_and_close_research_modal();
				})
				.catch(error => {
					this.researches.modals.research.errors = error.response.data;
				});
		},

		edit_research(index)
		{
			if (!this.allow_editing) { return; }
			if (index < 0 || index >= this.researches.data.length) { return; }

			this.researches.edit_index = index;
			for (const key in this.researches.modals.research.content) {
				this.researches.modals.research.content[key] = this.researches.data[this.researches.edit_index][key];
			}

			this.researches.modals.research.is_ongoing = (this.researches.modals.research.content.end_date === null);
			this.researches.modals.research.show = true;
		},

		update_research()
		{
			if (!this.allow_editing) { return; }
			if (this.researches.edit_index < 0 || this.researches.edit_index >= this.researches.data.length) { return; }

			if (this.researches.modals.research.is_ongoing) {
				this.researches.modals.research.content.end_date = null;
			}
			else if (this.researches.modals.research.content.end_date === null) {
				this.researches.modals.research.content.end_date = "";  // So that the backend throws an error (incorrect date format)
			}

			axios
				.put(`/api/${this.role}/research/${this.researches.data[this.researches.edit_index].uid}/`, {
					...this.researches.modals.research.content,
					...this.researches.request_token,
				})
				.then(_ => {
					this.get_researches();
					this.clear_and_close_research_modal();
				})
				.catch(error => {
					this.researches.modals.research.errors = error.response.data;
				});
		},

		delete_research()
		{
			if (!this.allow_editing) { return; }
			if (this.researches.edit_index < 0 || this.researches.edit_index >= this.researches.data.length) { return; }

			axios
				.delete(`/api/${this.role}/research/${this.researches.data[this.researches.edit_index].uid}/`, {
					data: {
						...this.researches.request_token
					}
				})
				.then(_ => { // No need to get researches again as order remains unchanged
					this.researches.data.splice(this.researches.edit_index, 1);
					this.clear_and_close_research_modal();
				})
				.catch(error => {
					this.researches.modals.research.errors = error.response.data;
				});
		}
	}
}
</script>
