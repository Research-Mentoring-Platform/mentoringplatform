<template>
<div class="container is-fullwidth">
	<div class="columns">
		<div class="column is-4 is-offset-1">
			<div class="title has-text-centered">
				Find Mentor
			</div>

			<table class="table has-background-light search-options">
				<tbody>
					<tr>
						<td class="is-vcentered is-fullheight">
							<label class="label">Search key</label>
						</td>
						<td class="is-vcentered is-fullheight">
							<div class="control is-fullwidth">
								<input v-model="search_text" class="input" type="text" placeholder="Enter username or name...">
							</div>
						</td>
					</tr>

					<tr>
						<td class="is-vcentered is-fullheight">
							<label class="label">Designation</label>
						</td>
						<td class="is-vcentered is-fullheight">
							<div class="select is-fullwidth">
								<select v-model="selected_uid.designation">
									<option value="" selected="selected">Any designation</option>
									<option v-for="designation in field_options.designation"
											v-bind:key="designation.uid"
											v-bind:value="designation.uid">
										{{ designation.label }}
									</option>
								</select>
							</div>
						</td>
					</tr>

					<tr>
						<td class="is-vcentered is-fullheight">
							<label class="label">Department</label>
						</td>
						<td class="is-vcentered is-fullheight">
							<div class="select is-fullwidth">
								<select v-model="selected_uid.department">
									<option value="" selected="selected">Any department</option>
									<option v-for="department in field_options.department"
											v-bind:key="department.uid"
											v-bind:value="department.uid">
										{{ department.label }}
									</option>
								</select>
							</div>
						</td>
					</tr>

					<tr>
						<td class="is-vcentered is-fullheight">
							<label class="label">Discipline</label>
						</td>
						<td class="is-vcentered is-fullheight">
							<div class="select is-fullwidth">
								<select v-model="selected_uid.discipline">
									<option value="" selected="selected">Any discipline</option>
									<option v-for="discipline in field_options.discipline"
											v-bind:key="discipline.uid"
											v-bind:value="discipline.uid">
										{{ discipline.label }}
									</option>
								</select>
							</div>
						</td>
					</tr>
					<tr>
						<td colspan="2" class="is-centered">
							<button class="button is-primary is-fullwidth" v-on:click="find_mentors">Search</button>
						</td>
					</tr>
				</tbody>
			</table>
		</div>


		<!-- SEARCH RESULTS -->
		<div class="column is-offset-1 is-5">
			<div class="title has-text-centered">
				Search Results
			</div>

			<div v-if="search_results.length === 0">
				<span class="box is-centered has-text-centered has-text-weight-bold has-background-white">
					No data
				</span>
			</div>
			<div v-else class="px-3" style="max-height: min(600px, 60vh); overflow-y: auto;">
				<ul>
					<li v-for="(mentor, index) in search_results" class="box py-4 my-3">
						<div class="columns is-mobile is-vcentered">
							<div class="column">
								<router-link v-bind:to="{ name: 'MentorProfile', params: { profile_uid: mentor.uid } }" class="hyperlink">
									{{ mentor.first_name }} {{ mentor.last_name }}
								</router-link>

								<div class="is-italic">
									{{ mentor.designation_label }}, {{ mentor.discipline_label }}
								</div>
							</div>

							<div class="column is-narrow">
								<button v-on:click="show_send_request_modal=true; selected_mentor_index=index;" class="button is-primary">
									Request
								</button>
							</div>
						</div>
					</li>
				</ul>
			</div>
		</div>

		<!-- SEND REQUEST MODAL -->
		<div v-bind:class="{ 'is-active': show_send_request_modal }" class="modal">
			<div class="modal-background" v-on:click="clear_and_close_send_request_modal"></div>
			<div class="modal-card">
				<header class="modal-card-head">
					<p class="modal-card-title">Send Request</p>
					<button v-on:click="clear_and_close_send_request_modal" class="delete" aria-label="close"></button>
				</header>

				<section class="modal-card-body">
					<InputBox input_type="textarea" v-model="modal.statement_of_purpose" v-bind:errors="modal_errors.statement_of_purpose"
							  label="Statement of Purpose" />

					<InputBox input_type="textarea" v-model="modal.commitment" v-bind:errors="modal_errors.commitment"
							  label="Commitment" />

					<InputBox input_type="textarea" v-model="modal.expectations" v-bind:errors="modal_errors.expectations"
							  label="Expectations" />
				</section>

				<footer class="modal-card-foot">
					<div class="columns is-mobile" style="width: 100%;">
						<div class="column has-text-right">
							<button v-on:click="send_mentorship_request" class="button is-success">Send</button>
							<button v-on:click="clear_and_close_send_request_modal" class="button">Cancel</button>
						</div>
					</div>
				</footer>
			</div>
		</div>
	</div>
</div>
</template>

<script>
import axios from "../../api/my-axios";
import InputBox from "../FormHelpers/InputBox";
import FormErrors from "../FormHelpers/FormErrors";
import {mapState} from "vuex";

export default {
	name: "FindMentor",
	components: {
		FormErrors,
		InputBox
	},
	computed: {
		...mapState({
			user: "user"
		})
	},
	data() {
		return {
			search_text: "",
			field_options: {
				designation: [],
				department: [],
				discipline: []
			},

			selected_uid: {
				designation: "",
				department: "",
				discipline: "",
			},

			show_send_request_modal: false,
			modal: {
				statement_of_purpose: "",
				commitment: "",
				expectations: "",
			},
			selected_mentor_index: -1,

			search_results: [], // TODO Should only consist of non-pending requests

			modal_errors: {},
		};
	},
	created()
	{
		// TODO Try to fetch all three field options in one-go
		this.get_field_options();
	},
	methods: {
		clear_send_request_modal()
		{
			for (const key in this.modal) {
				this.modal[key] = "";
			}

			this.modal_errors = {};
			this.selected_mentor_index = -1;
		},

		clear_and_close_send_request_modal()
		{
			this.clear_send_request_modal();
			this.show_send_request_modal = false;
		},

		get_field_options() {
			for (const field in this.field_options) {
				axios
					.get(`/api/mentor/${field}/`)
					.then(response => {
						this.field_options[field] = response.data;
					})
					.catch(error => {
						this.errors = error.response.data;
					});
			}
		},

		find_mentors() {
			axios
				.get("/api/mentor/mentor/find_for_mentorship/", {
					params: {
						search: this.search_text,
						designation: this.selected_uid.designation,
						department: this.selected_uid.department,
						discipline: this.selected_uid.discipline
					}
				})
				.then(response => {
					this.search_results = response.data;
				})
				.catch(error => {
					console.error(error);
					this.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		send_mentorship_request()
		{
			axios
				.post("/api/mentorship/request/", {
					mentee: this.user.profile_uid,
					mentor: this.search_results[this.selected_mentor_index].uid, // Here, uid -> profile_uid, user -> user uid
					...this.modal
				})
				.then(_ => {
					this.search_results.splice(this.selected_mentor_index, 1);
					this.clear_and_close_send_request_modal();
				})
				.catch(error => {
					this.modal_errors = error.response.data;
				});
		},
	}
}
</script>

<style scoped>
.search-results td,
.search-options td {
	border: none !important;
}
</style>
