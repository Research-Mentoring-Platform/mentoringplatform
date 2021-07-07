<template>
<div class="container">
	<!-- HEADING -->
	<div class="title has-text-centered mb-5">
		Milestones
		<button v-on:click="milestones.modals.milestone.show=true" class="button is-rounded is-primary p-4">
			<span class="icon">
				<i class="fa fa-plus"></i>
			</span>
		</button>
	</div>

	<FormErrors v-bind:errors="milestones.errors.detail" />


	<!-- MILESTONE RECORDS -->
  	<!-- TODO Change div to ul-li for all components -->
	<ul v-if="milestones.data.length === 0">
		<li class="box has-text-centered is-centered has-text-weight-bold has-background-white">
			No data
		</li>
	</ul>
	<ul v-else class="px-3" style="max-height: min(600px, 60vh); overflow-y: auto;">
		<li v-for="(milestone, index) in milestones.data" class="pb-5">
			<MilestoneBox v-bind:milestone="milestone"
						  v-on:edit_milestone="edit_milestone(index)"
						  v-on:show_milestone_description="show_milestone_details(index)" />
		</li>
	</ul>


	<!-- VIEW PARTICULAR MILESTONE DETAILS MODAL -->
	<div v-bind:class="{ 'is-active': milestones.modals.description.show }" class="modal">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Milestone details</p>
				<button v-on:click="milestones.modals.description.show = false" class="delete" aria-label="close"></button>
			</header>

			<div class="modal-card-body">
				<p class="content is-medium has-text-left">{{ milestones.modals.milestone.content.description }}</p>
			</div>
		</div>
	</div>


	<!-- ADD/UPDATE MILESTONE MODAL -->
	<div v-bind:class="{ 'is-active': milestones.modals.milestone.show }" class="modal">
		<div class="modal-background" v-on:click="clear_and_close_milestone_modal"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<span v-if="milestones.edit_index === -1" class="modal-card-title">Add Milestone</span>
				<span v-else class="modal-card-title">Edit Milestone</span>
				<button v-on:click="clear_and_close_milestone_modal" class="delete" aria-label="close"></button>
			</header>

			<section class="modal-card-body has-text-left">
				<InputBox input_type="datetime-local" v-model="milestones.modals.milestone.content.date"
						  v-bind:errors="milestones.modals.milestone.errors.date"
						  label="Date & Time" icon="fas fa-calendar" />

				<InputBox input_type="textarea" v-model="milestones.modals.milestone.content.description"
						  v-bind:errors="milestones.modals.milestone.errors.description"
						  label="Description" icon="fas fa-info-circle"/>

				<FormErrors v-bind:errors="milestones.modals.milestone.errors.detail" />
				<FormErrors v-bind:errors="milestones.modals.milestone.errors.non_field_errors" />
			</section>

			<footer class="modal-card-foot">
				<div class="columns is-mobile" style="width: 100%;">
					<div class="column is-narrow has-text-left">
						<button v-if="milestones.edit_index >= 0" v-on:click="delete_milestone" class="button is-danger">Delete</button>
					</div>

					<div class="column has-text-right">
						<button v-if="milestones.edit_index >= 0" v-on:click="update_milestone" class="button is-success">Update</button>
						<button v-else v-on:click="add_milestone" class="button is-success">Add</button>

						<button v-on:click="clear_and_close_milestone_modal" class="button">Cancel</button>
					</div>
				</div>
			</footer>
		</div>
	</div>
</div>
</template>


<script>
import axios from "../../api/my-axios";
import MilestoneBox from "./MilestoneBox";
import InputBox from "../FormHelpers/InputBox";
import FormErrors from "../FormHelpers/FormErrors";

export default {
	name: "Milestones",
	components: {
		MilestoneBox,
		InputBox,
		FormErrors
	},
	props: {
		mentorship_uid: {
			type: String,
			required: true
		}
	},
	data() {
		return {
			milestones: {
				request_token: {
					mentorship: ""
				},

				errors: {},

				edit_index: -1,

				modals: {
					description: {
						show: false,
						content: {
							description: ""
						},
						errors: {}
					},

					milestone: {
						show: false,
						content: {
							date: "",
							title: "",
							description: "",
						},
						errors: {}
					}
				},

				data: [
					// {
					// 	date: "",
					// 	title: "",
					// 	description: "",
					// }
				],
			}
		};
	},
	created()
	{
		this.milestones.request_token.mentorship = this.mentorship_uid;
		this.get_milestones();
	},
	methods: {
		clear_milestone_modal()
		{
			for (const key in this.milestones.modals.milestone.content) {
				this.milestones.modals.milestone.content[key] = "";
			}

			this.milestones.edit_index = -1; // Important
			this.milestones.modals.milestone.errors = {};
		},

		clear_and_close_milestone_modal()
		{
			this.clear_milestone_modal();
			this.milestones.modals.milestone.show = false;
		},

		show_milestone_details(index)
		{
			if (index >= this.milestones.data.length) { return; }
			this.milestones.modals.milestone.content.description = this.milestones.data[index].description;
			this.milestones.modals.description.show = true;
		},

		get_milestones()
		{
			axios
				.get("/api/mentorship/milestone/", {
					params: {
						...this.milestones.request_token
					}
				})
				.then(response => {
					this.milestones.data = response.data;
				})
				.catch(error => {
					this.milestones.modals.milestone.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		add_milestone()
		{
			axios
				.post("/api/mentorship/milestone/", {
					...this.milestones.modals.milestone.content,
					...this.milestones.request_token
				})
				.then(_ => {
					this.get_milestones();
					this.clear_and_close_milestone_modal();
				})
				.catch(error => {
					this.milestones.modals.milestone.errors = error.response.data;
				});
		},

		edit_milestone(index)
		{
			if (index < 0 || index >= this.milestones.data.length) { return; }

			this.milestones.edit_index = index;
			for (const key in this.milestones.modals.milestone.content) {
				this.milestones.modals.milestone.content[key] = this.milestones.data[this.milestones.edit_index][key];
			}

			this.milestones.modals.milestone.show = true;
		},

		update_milestone()
		{
			if (this.milestones.edit_index < 0 || this.milestones.edit_index >= this.milestones.data.length) { return; }

			axios
				.put(`/api/mentorship/milestone/${this.milestones.data[this.milestones.edit_index].uid}/`, {
					...this.milestones.modals.milestone.content,
					...this.milestones.request_token
				})
				.then(_ => {
					this.get_milestones();
					this.clear_and_close_milestone_modal();
				})
				.catch(error => {
					this.milestones.modals.milestone.errors = error.response.data;
				});
		},

		delete_milestone()
		{
			if (this.milestones.edit_index < 0 || this.milestones.edit_index >= this.milestones.data.length) { return; }

			axios
				.delete(`/api/mentorship/milestone/${this.milestones.data[this.milestones.edit_index].uid}/`, {
					data: {
						...this.milestones.request_token
					}
				})
				.then(_ => { // No need to get milestones again as order remains unchanged
					this.milestones.data.splice(this.milestones.edit_index, 1);
					this.clear_and_close_milestone_modal();
				})
				.catch(error => {
					this.milestones.modals.milestone.errors = error.response.data;
				});
		}
	}
}
</script>
