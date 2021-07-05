<template>
<div class="container">
	<!-- HEADING -->
	<div class="title has-text-centered mb-5">
		Meeting Summary
		<button v-on:click="meeting_summaries.modals.summary.show=true" class="button is-rounded is-primary p-4">
			<span class="icon">
				<i class="fa fa-plus"></i>
			</span>
		</button>
	</div>

	<FormErrors v-bind:errors="meeting_summaries.errors.detail" />


	<!-- MEETING SUMMARY RECORDS -->
	<div v-if="meeting_summaries.data.length === 0">
		<span class="box is-centered has-text-weight-bold has-background-white">
			No data
		</span>
	</div>
	<div v-else v-for="(meeting_summary, index) in meeting_summaries" class="pb-5">
		<MeetingSummaryBox v-bind:meeting_summary="meeting_summary" v-on:edit_meeting_summary="edit_meeting_summary(index)"
						   v-on:show_meeting_summary_details="show_meeting_summary_details(index)" />
	</div>


	<!-- VIEW PARTICULAR MEETING SUMMARY DETAILS MODAL -->
	<div v-bind:class="{ 'is-active': meeting_summaries.modals.description.show }" class="modal">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Meeting Summary</p>
				<button v-on:click="meeting_summaries.modals.description.show = false" class="delete" aria-label="close"></button>
			</header>

			<div class="modal-card-body">
				<p class="content is-medium has-text-left">{{ meeting_summaries.modals.description.content.description }}</p>
			</div>
		</div>
	</div>


	<!-- ADD/UPDATE MEETING SUMMARY MODAL -->
	<div v-bind:class="{ 'is-active': meeting_summaries.modals.summary.show }" class="modal">
		<div class="modal-background" v-on:click="clear_and_close_meeting_summary_modal"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<span v-if="meeting_summaries.edit_index === -1" class="modal-card-title">Add Meeting Summary</span>
				<span v-else class="modal-card-title">Edit Meeting Summary</span>
				<button v-on:click="clear_and_close_meeting_summary_modal" class="delete" aria-label="close"></button>
			</header>

			<section class="modal-card-body has-text-left">
				<InputBox input_type="datetime-local" v-model="meeting_summaries.modals.summary.content.date_time"
						  v-bind:errors="meeting_summaries.modals.summary.errors.date_time"
						  label="Date & Time" icon="fas fa-graduation-cap" />

				<InputBox input_type="number" v-model="meeting_summaries.modals.summary.content.duration"
						  v-bind:errors="meeting_summaries.modals.summary.errors.duration"
						  label="Duration (hours)" icon="fas fa-school" />

				<InputBox input_type="textarea" v-model="meeting_summaries.modals.summary.content.description"
						  v-bind:errors="meeting_summaries.modals.summary.errors.description"
						  label="Description" icon="fas fa-calendar" />

				<InputBox input_type="textarea" v-model="meeting_summaries.modals.summary.content.todos"
						  v-bind:errors="meeting_summaries.modals.summary.errors.todos"
						  label="Todos" icon="fas fa-calendar" />

				<InputBox input_type="datetime-local" v-model="meeting_summaries.modals.summary.content.next_meeting_date_time"
						  v-bind:errors="meeting_summaries.modals.summary.errors.next_meeting_date_time"
						  label="Next Meeting Date & Time" icon="fas fa-info-circle"/>

				<InputBox input_type="textarea" v-model="meeting_summaries.modals.summary.content.next_meeting_agenda"
						  v-bind:errors="meeting_summaries.modals.summary.errors.next_meeting_agenda"
						  label="Next Meeting Agenda" icon="fas fa-calendar" />

				<FormErrors v-bind:errors="meeting_summaries.modals.summary.errors.detail" />
				<FormErrors v-bind:errors="meeting_summaries.modals.summary.errors.non_field_errors" />
			</section>

			<footer class="modal-card-foot">
				<div class="columns is-mobile" style="width: 100%;">
					<div class="column is-narrow has-text-left">
						<button v-if="meeting_summaries.edit_index >= 0" v-on:click="delete_meeting_summary" class="button is-danger">Delete</button>
					</div>

					<div class="column has-text-right">
						<button v-if="meeting_summaries.edit_index >= 0" v-on:click="update_meeting_summary" class="button is-success">Update</button>
						<button v-else v-on:click="add_meeting_summary" class="button is-success">Add</button>

						<button v-on:click="clear_and_close_meeting_summary_modal" class="button">Cancel</button>
					</div>
				</div>
			</footer>
		</div>
	</div>
</div>
</template>


<script>
import { mapState } from "vuex";
import axios from "../../api/my-axios";
import MeetingSummaryBox from "./MeetingSummaryBox";
import InputBox from "../FormHelpers/InputBox";
import FormErrors from "../FormHelpers/FormErrors";

export default {
	name: "MeetingSummaries",
	components: {
		MeetingSummaryBox,
		InputBox,
		FormErrors
	},
	props: {

	},
	data() {
		return {
			meeting_summaries: {
				request_token: {
					mentor: "",
					mentee: ""
				},

				errors: {},

				edit_index: -1,

				modals: {
					description: {
						show: false,
						content: {
							description: "",
						},
						errors: {}
					},

					summary: {
						show: false,
						content: {
							date_time: "",
							duration: "",
							description: "",
							todos: "",
							next_meeting_date_time: "",
							next_meeting_agenda: ""
						},
						errors: {}
					},
				},

				data: [
					// {
					// 	date_time: "",
					// 	duration: "",
					// 	description: "",
					// 	todos: "",
					// 	next_meeting_date_time: "",
					// 	next_meeting_agenda: ""
					// }
				],
			}
		};
	},
	computed: {
		...mapState({
			user: "user"
		})
	},
	created()
	{
		if (this.user.is_mentor) {
			this.meeting_summaries.request_token.mentor = this.user.profile_uid;
			this.meeting_summaries.request_token.mentee = this.profile_uid;
		}
		else {
			this.meeting_summaries.request_token.mentor = this.profile_uid;
			this.meeting_summaries.request_token.mentee = this.user.profile_uid;
		}

		this.get_meeting_summaries();
	},
	methods: {
		clear_meeting_summary_modal()
		{
			for (const key in this.meeting_summaries.modals.summary.content) {
				this.meeting_summaries.modals.summary.content[key] = "";
			}

			this.meeting_summaries.edit_index = -1; // Important
			this.meeting_summaries.modals.summary.errors = {};
		},

		clear_and_close_meeting_summary_modal()
		{
			this.clear_meeting_summary_modal();
			this.meeting_summaries.modals.summary.show = false;
		},

		show_meeting_summary_details(index)
		{
			if (index >= this.meeting_summaries.data.length) { return; }
			this.meeting_summaries.modals.description.content.description = this.meeting_summaries.data[index].details;
			this.meeting_summaries.modals.description.show = true;
		},

		get_meeting_summaries()
		{
			axios
				.get("/api/mentorship/meeting-summary/", {
					// ...this.user_token
				})
				.then(response => {
					this.meeting_summaries.data = response.data;
				})
				.catch(error => {
					this.meeting_summaries.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		add_meeting_summary()
		{
			axios
				.post("/api/mentorship/meeting-summary/", {
					...this.meeting_summaries.modals.summary.content,
					...this.meeting_summaries.request_token
				})
				.then(_ => {
					this.get_meeting_summaries();
					this.clear_and_close_meeting_summary_modal();
				})
				.catch(error => {
					this.meeting_summaries.modals.summary.errors = error.response.data;
				});
		},

		edit_meeting_summary(index)
		{
			if (index < 0 || index >= this.meeting_summaries.data.length) { return; }

			this.meeting_summaries.edit_index = index;
			for (const key in this.meeting_summaries.modals.summary.content) {
				this.meeting_summaries.modals.summary.content[key] = this.meeting_summaries.data[this.meeting_summaries.edit_index][key];
			}

			this.meeting_summaries.modals.summary.show = true;
		},

		update_meeting_summary()
		{
			if (this.meeting_summaries.edit_index < 0 || this.meeting_summaries.edit_index >= this.meeting_summaries.data.length) { return; }

			axios
				.put(`/api/mentorship/meeting-summary/${this.meeting_summaries.data[this.meeting_summaries.edit_index].uid}/`, {
					...this.meeting_summaries.modals.summary.content,
					...this.meeting_summaries.request_token
				})
				.then(_ => {
					this.get_meeting_summaries();
					this.clear_and_close_meeting_summary_modal();
				})
				.catch(error => {
					this.meeting_summaries.modals.summary.errors = error.response.data;
				});
		},

		delete_meeting_summary()
		{
			if (this.meeting_summaries.edit_index < 0 || this.meeting_summaries.edit_index >= this.meeting_summaries.data.length) { return; }

			axios
				.delete(`/api/mentorship/meeting_summary/${this.meeting_summaries.data[this.meeting_summaries.edit_index].uid}/`, {
					data: {
						...this.meeting_summaries.request_token
					}
				})
				.then(_ => { // No need to get meeting_summaries again as order remains unchanged
					this.meeting_summaries.data.splice(this.meeting_summaries.edit_index, 1);
					this.clear_and_close_meeting_summary_modal();
				})
				.catch(error => {
					this.meeting_summaries.modals.summary.errors = error.response.data;
				});
		}
	}
}
</script>
