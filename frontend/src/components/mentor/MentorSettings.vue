<template>
<div class="container">
	<div class="title has-text-centered">
		Mentor Settings
	</div>

	<div>
		<div class="field">
			<label class="label">Expected minimum mentorship duration</label>
			<div class="control">
				<div v-if="allow_editing" class="select is-fullwidth">
					<select v-model="settings.selected.expected_min_mentorship_duration">
						<option v-bind:value="null" selected="selected">No minimum duration</option>
						<option v-for="min_duration in 18" v-bind:value="min_duration">
							{{ min_duration }} months
						</option>
					</select>
				</div>
				<div v-else class="box is-rounded p-3">
					{{ settings.selected.expected_min_mentorship_duration || "No minimum duration" }}
				</div>

				<FormErrors v-bind:errors="settings.errors.expected_min_mentorship_duration" />
			</div>
		</div>

		<div class="field">
			<label class="label">Expected maximum mentorship duration</label>
			<div class="control">
				<div v-if="allow_editing" class="select is-fullwidth">
					<select v-model="settings.selected.expected_max_mentorship_duration">
						<option v-bind:value="null" selected="selected">No maximum duration</option>
						<option v-for="max_duration in 18" v-bind:value="max_duration">
							{{ max_duration }} months
						</option>
					</select>
				</div>
				<div v-else class="box is-rounded p-3">
					{{ settings.selected.expected_max_mentorship_duration || "No maximum duration" }}
				</div>

				<FormErrors v-bind:errors="settings.errors.expected_max_mentorship_duration" />
			</div>
		</div>

		<div class="field">
			<div class="control py-2">
				<div v-if="allow_editing">
					<label class="checkbox">
						<input type="checkbox" v-model="settings.selected.is_accepting_mentorship_requests">
						Are you accepting new mentees?
					</label>
				</div>
				<div v-else class="box">
					<div class="columns is-vcentered">
						<div class="column p-1">
							<strong>Is accepting mentorship requests?</strong>
						</div>
						<div class="column is-narrow p-1">
							<span v-if="settings.selected.is_accepting_mentorship_requests" class="box has-background-success is-shadowless py-1">
								Yes
							</span>
							<span v-else class="box has-background-danger is-shadowless py-1">
								No
							</span>
						</div>
					</div>
				</div>
			</div>
		</div>

		<div class="field">
			<label class="label">Accepted mentee types</label>
			<div class="control">
				<div v-if="allow_editing">
					<ul>
						<li v-for="mentee_type in settings.options.accepted_mentee_types">
							<label class="checkbox pb-2">
								<input type="checkbox" v-bind:value="mentee_type.uid"
									   v-model="settings.selected.accepted_mentee_types">
								{{ mentee_type.label }}
							</label>
						</li>
					</ul>
				</div>
				<div v-else class="content">
					<ul v-if="settings.selected.accepted_mentee_types.length === 0" style="list-style: none;">
						<li class="has-text-centered has-text-weight-bold p-3">
							No accepted mentee types
						</li>
					</ul>
					<ul v-else>
						<li v-for="mentee_type in settings.selected.accepted_mentee_type_labels" class="pb-2">
							{{ mentee_type }}
						</li>
					</ul>
				</div>
			</div>
		</div>

		<div class="field">
			<label class="label">Responsibilities</label>
			<div class="control">
				<div v-if="allow_editing">
					<ul>
						<li v-for="responsibility in settings.options.responsibilities">
							<label class="checkbox pb-2">
								<input type="checkbox" v-bind:value="responsibility.uid"
									   v-model="settings.selected.responsibilities">
								{{ responsibility.description }}
							</label>
						</li>
					</ul>
				</div>
				<div v-else class="content">
					<ul v-if="settings.selected.responsibilities.length === 0">
						<li class="box has-text-centered has-text-weight-bold p-3">
							No responsibilities
						</li>
					</ul>
					<ul v-else>
						<li v-for="responsibility in settings.selected.responsibility_descriptions" class="pb-2">
							{{ responsibility }}
						</li>
					</ul>
				</div>
			</div>
		</div>

		<div class="field">
			<label class="label">Other responsibilities</label>
			<div class="control">
				<div v-if="allow_editing">
					<textarea class="textarea" v-model="settings.selected.other_responsibility"></textarea>
				</div>
				<div v-else class="box p-3">
					{{ settings.selected.other_responsibility }}
				</div>
			</div>
		</div>

		<div v-if="allow_editing" class="control">
			<button v-on:click="save" class="button is-fullwidth is-success">Update</button>
		</div>
	</div>
</div>
</template>


<script>
import { mapState } from "vuex";
import axios from "../../api/my-axios";
import FormErrors from "../FormHelpers/FormErrors";

export default {
	components: {
		FormErrors,
	},
	props: {
		is_editable: {
			type: Boolean,
			default: false,
		},
		profile_uid: {
			type: String,
			default: null
		}
	},
	computed: {
		...mapState({
			user: "user"
		})
	},
	data() {
		return {
			allow_editing: true,
			to_show_profile_uid: this.profile_uid,

			settings: {
				request_token: {
					mentor: ""
				},

				errors: {},

				options: {
					accepted_mentee_types: [

					],
					responsibilities: [

					]
				},

				selected: {
					expected_min_mentorship_duration: "",
					expected_max_mentorship_duration: "",
					is_accepting_mentorship_requests: true,
					accepted_mentee_types: [], // UIDs of the mentee types
					accepted_mentee_type_labels: [], // Labels of the mentee types
					responsibilities: [], // UIDs of the responsibilities
					responsibility_descriptions: [], // Labels of the responsibilities
					other_responsibility: "",
				}
			}
		};
	},
	created() {
		this.to_show_profile_uid = this.profile_uid ? this.profile_uid : this.user.profile_uid;
		this.allow_editing = this.is_editable ? (this.to_show_profile_uid === this.user.profile_uid) : false;
		this.get_field_options();
		this.get_currently_selected_options();
	},
	methods: {
		get_field_options()
		{
			axios
				.get("/api/mentee/designation/")
				.then(response => {
					this.settings.options.accepted_mentee_types = response.data;
				})
				.catch(error => {
					this.settings.errors.accepted_mentee_types = error.response ? error.response.data : {"detail": [error.message]};
				});

			axios
				.get("/api/mentor/responsibility/")
				.then(response => {
					console.log(response.data);
					this.settings.options.responsibilities = response.data;
				})
				.catch(error => {
					this.settings.errors.responsibilities = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		get_currently_selected_options()
		{
			axios
				.get(`/api/mentor/mentor/${this.to_show_profile_uid}/`)
				.then(response => {
					console.log(response.data);
					for (const field in this.settings.selected) {
						this.settings.selected[field] = response.data[field];
					}
				})
				.catch(error => {
					console.error(error);
					this.settings.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		save()
		{
			if (!this.allow_editing) { return; }

			if (!this.settings.selected.expected_min_mentorship_duration) {
				this.settings.selected.expected_min_mentorship_duration = null;
			}

			if (!this.settings.selected.expected_max_mentorship_duration) {
				this.settings.selected.expected_max_mentorship_duration = null;
			}

			axios
				.patch(`/api/mentor/mentor/${this.user.profile_uid}/`, {
					...this.settings.selected
				})
				.catch(error => {
					console.error(error);
				});
		}
	}
}
</script>
