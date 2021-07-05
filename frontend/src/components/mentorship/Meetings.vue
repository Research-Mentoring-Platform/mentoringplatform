<template>
<div class="container">
	<!-- HEADING -->
	<div class="title has-text-centered mb-5">
		Meetings
		<button v-on:click="meetings.modals.meeting.show=true" class="button is-rounded is-primary p-4">
			<span class="icon">
				<i class="fa fa-plus"></i>
			</span>
		</button>
	</div>

	<FormErrors v-bind:errors="meetings.errors.detail" />
	<FormErrors v-bind:errors="meeting_summaries.errors.detail" />


	<!-- MEETING RECORDS -->
	<ul v-if="meetings.data.length === 0">
		<li class="box is-centered has-text-weight-bold has-background-white">
			No data
		</li>
	</ul>
	<ul v-else class="px-3" style="max-height: min(600px, 60vh); overflow-y: auto;">
		<li v-for="(meeting, index) in meetings.data" class="pb-5">
			<MeetingBox v-bind:meeting="meeting"
						v-on:edit_meeting="edit_meeting(index)"
						v-on:show_meeting_agenda="show_meeting_agenda(index)"
						v-on:add_meeting_summary="meeting_summaries.modals.summary.show=true; set_meeting_uid_for_summary(meeting);" />
		</li>
	</ul>


	<!-- VIEW PARTICULAR MEETING DETAILS MODAL -->
	<div v-bind:class="{ 'is-active': meetings.modals.agenda.show }" class="modal">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Meeting details</p>
				<button v-on:click="meetings.modals.agenda.show=false" class="delete" aria-label="close"></button>
			</header>

			<div class="modal-card-body">
				<p class="content is-medium has-text-left">{{ meetings.modals.agenda.content.agenda }}</p>
			</div>
		</div>
	</div>


	<!-- ADD/UPDATE MEETING MODAL -->
	<div v-bind:class="{ 'is-active': meetings.modals.meeting.show }" class="modal">
		<div class="modal-background" v-on:click="clear_and_close_meeting_modal"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<span v-if="meetings.edit_index === -1" class="modal-card-title">Add Meeting</span>
				<span v-else class="modal-card-title">Edit Meeting</span>
				<button v-on:click="clear_and_close_meeting_modal" class="delete" aria-label="close"></button>
			</header>

			<section class="modal-card-body has-text-left">
				<InputBox input_type="text" v-model="meetings.modals.meeting.content.title"
						  v-bind:errors="meetings.modals.meeting.errors.title"
						  label="Title" />

				<InputBox input_type="datetime-local" v-model="meetings.modals.meeting.content.date_time"
						  v-bind:errors="meetings.modals.meeting.errors.date_time"
						  label="Date & Time" icon="fas fa-calendar" />

				<InputBox input_type="text" v-model="meetings.modals.meeting.content.url"
						  v-bind:errors="meetings.modals.meeting.errors.url"
						  label="URL" icon="fas fa-external-link-alt" />

				<InputBox input_type="textarea" v-model="meetings.modals.meeting.content.agenda"
						  v-bind:errors="meetings.modals.meeting.errors.agenda"
						  label="Agenda" icon="fas fa-info-circle"/>

				<FormErrors v-bind:errors="meetings.modals.meeting.errors.detail" />
				<FormErrors v-bind:errors="meetings.modals.meeting.errors.non_field_errors" />
			</section>

			<footer class="modal-card-foot">
				<div class="columns is-mobile" style="width: 100%;">
					<div class="column is-narrow has-text-left">
						<button v-if="meetings.edit_index >= 0" v-on:click="delete_meeting" class="button is-danger">Delete</button>
					</div>

					<div class="column has-text-right">
						<button v-if="meetings.edit_index >= 0" v-on:click="update_meeting" class="button is-success">Update</button>
						<button v-else v-on:click="add_meeting" class="button is-success">Add</button>

						<button v-on:click="clear_and_close_meeting_modal" class="button">Cancel</button>
					</div>
				</div>
			</footer>
		</div>
	</div>



	<!-- -------------------------------- -->
	<!-- ADD/UPDATE MEETING SUMMARY MODAL -->
	<!-- -------------------------------- -->
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

				<InputBox input_type="datetime-local" v-model="meeting_summaries.modals.summary.content.next_meeting_date"
						  v-bind:errors="meeting_summaries.modals.summary.errors.next_meeting_date"
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
import MeetingBox from "./MeetingBox";
import InputBox from "../FormHelpers/InputBox";
import FormErrors from "../FormHelpers/FormErrors";

export default {
	name: "Meetings",
	components: {
		MeetingBox,
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
			meetings: {
				request_token: {
					mentorship: "",
					creator: ""
				},

				errors: {},

				modals: {
					agenda: {
						show: false,
						content: {
							agenda: "",
						},
						errors: {}
					},

					meeting: {
						show: false,
						content: {
							title: "", // "" is important, as null=True is not allowed in back-end
							date_time: "",
							url: "",
							agenda: "",
						},
						errors: {}
					},
				},

				data: [
					{
						title: "",
						url: "",
						date_time: "",
						agenda: "",
					}
				],
				edit_index: -1
			},



			meeting_summaries: {
				request_token: {
					mentor: "",
					mentee: ""
				},

				errors: {},

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
							meeting: "", // The Meeting UID. Is set up in the template upon clicking [+]
							// TODO Make sure one summary per meeting
							date_time: "",
							duration: "",
							description: "",
							todos: "",
							next_meeting_date: "", // TODO Rename to next_meeting_date_time
							next_meeting_agenda: ""
						},
						errors: {}
					},
				},

				data: [
					{
						date_time: "",
						duration: "",
						description: "",
						todos: "",
						next_meeting_date: "",
						next_meeting_agenda: ""
					}
				],
				edit_index: -1
			},
		};
	},
	computed: {
		...mapState({
			user: "user"
		})
	},
	created()
	{
		this.meetings.request_token.mentorship = this.mentorship_uid;
		this.meetings.request_token.creator = this.user.uid;

		if (this.user.is_mentor) {
			this.meeting_summaries.request_token.mentor = this.user.profile_uid;
			this.meeting_summaries.request_token.mentee = this.profile_uid;
		}
		else {
			this.meeting_summaries.request_token.mentor = this.profile_uid;
			this.meeting_summaries.request_token.mentee = this.user.profile_uid;
		}

		this.get_meetings();
		this.get_meeting_summaries();
	},
	methods: {
		// --------------------------------------------------------------------
		// MEETINGS
		// --------------------------------------------------------------------
		clear_meeting_modal()
		{
			for (const key in this.meetings.modals.meeting.content) {
				this.meetings.modals.meeting.content[key] = "";
			}

			this.meetings.edit_index = -1; // Important
			this.meetings.modals.meeting.errors = {};
		},

		clear_and_close_meeting_modal()
		{
			this.clear_meeting_modal();
			this.meetings.modals.meeting.show = false;
		},

		show_meeting_agenda(index)
		{
			if (index >= this.meetings.data.length) { return; }
			this.meetings.modals.agenda.content.agenda = this.meetings.data[index].agenda;
			this.meetings.modals.agenda.show = true;
		},

		get_meetings()
		{
			axios
				.get("/api/mentorship/meeting/", {
					params: {
						...this.meetings.request_token
					}
				})
				.then(response => {
					this.meetings.data = response.data;
				})
				.catch(error => {
					this.meetings.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		add_meeting()
		{
			axios
				.post("/api/mentorship/meeting/", {
					...this.meetings.modals.meeting.content,
					...this.meetings.request_token,
				})
				.then(_ => {
					this.get_meetings();
					this.clear_and_close_meeting_modal();
				})
				.catch(error => {
					this.meetings.modals.meeting.errors = error.response.data;
				});
		},

		edit_meeting(index)
		{
			if (index < 0 || index >= this.meetings.length) { return; }

			this.meetings.edit_index = index;
			for (const key in this.meetings.modals.meeting.content) {
				this.meetings.modals.meeting.content[key] = this.meetings.data[this.meetings.edit_index][key];
			}

			this.meetings.modals.meeting.show = true;
		},

		update_meeting()
		{
			if (this.meetings.edit_index < 0 || this.meetings.edit_index >= this.meetings.length) { return; }

			axios
				.put(`/api/mentorship/meeting/${this.meetings.data[this.meetings.edit_index].uid}/`, {
					...this.meetings.modals.meeting.content,
					...this.meetings.request_token,
				})
				.then(_ => {
					this.get_meetings();
					this.clear_and_close_meeting_modal();
				})
				.catch(error => {
					this.meetings.modals.meeting.errors = error.response.data;
				});
		},

		delete_meeting()
		{
			if (this.meetings.edit_index < 0 || this.meetings.edit_index >= this.meetings.length) { return; }

			axios
				.delete(`/api/mentorship/meeting/${this.meetings[this.meetings.edit_index].uid}/`, {
					data: {
						...this.meetings.request_token
					}
				})
				.then(_ => { // No need to get meetings again as order remains unchanged
					this.meetings.data.splice(this.meetings.edit_index, 1);
					this.clear_and_close_meeting_modal();
				})
				.catch(error => {
					this.meetings.modals.meeting.errors = error.response.data;
				});
		},

		// --------------------------------------------------------------------
		// MEETING SUMMARIES
		// --------------------------------------------------------------------
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
			if (index >= this.meeting_summaries.length) { return; }
			this.meeting_summaries.modals.description.content.description = this.meeting_summaries[index].details;
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

		set_meeting_uid_for_summary(meeting) {
			this.meeting_summaries.modals.summary.content.meeting = meeting.uid;
		},

		add_meeting_summary()
		{
			// Must set content's meeting before calling this
			axios
				.post("/api/mentorship/meeting-summary/", {
					...this.meeting_summaries.modals.summary.content,
					...this.meeting_summaries.request_token,
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
			if (index < 0 || index >= this.meeting_summaries.length) { return; }

			this.meeting_summaries.edit_index = index;
			for (const key in this.meeting_summaries.modals.summary.content) {
				this.meeting_summaries.modals.summary.content[key] = this.meeting_summaries.data[this.meeting_summaries.edit_index][key];
			}

			this.meeting_summaries.modals.summary.content.meeting = this.meetings.data[index].uid;
			this.meeting_summaries.modals.summary.show = true;
		},

		update_meeting_summary()
		{
			if (this.meeting_summaries.edit_index < 0 || this.meeting_summaries.edit_index >= this.meeting_summaries.length) { return; }

			axios
				.put(`/api/mentorship/meeting-summary/${this.meeting_summaries[this.meeting_summaries.edit_index].uid}/`, {
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
			if (this.meeting_summaries.edit_index < 0 || this.meeting_summaries.edit_index >= this.meeting_summaries.length) { return; }

			axios
				.delete(`/api/mentorship/meeting_summary/${this.meeting_summaries[this.meeting_summaries.edit_index].uid}/`, {
					...this.meeting_summaries.request_token
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
