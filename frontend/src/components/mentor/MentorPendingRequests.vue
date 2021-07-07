<template>
<div class="container">
	<div class="title has-text-centered">
		Pending Requests
	</div>

	<FormErrors v-bind:errors="pending_requests.errors.detail" />


	<!-- PENDING REQUESTS -->
	<div class="columns is-centered">
		<div class="column is-5" style="max-height: min(600px, 60vh); overflow-y: auto;">
			<ul>
				<li v-for="(pending_request, index) in pending_requests.data" class="box is-rounded mb-4">
					<div class="columns is-vcentered">
						<div class="column">
							{{ pending_request.mentee }}
						</div>

						<div class="column is-narrow">
							<button v-on:click="show_request_details(index)" class="button is-info mr-2">
								<span class="icon"><i class="fas fa-info"></i></span>
							</button>
							<button v-on:click="accept_pending_request(index)" class="button is-success mr-2">
								<span class="icon"><i class="fas fa-check"></i></span>
							</button>
							<!-- TODO Rename reject to decline in backend and frontend -->
							<button v-on:click="show_reject_reason_modal(index)" class="button is-danger">
								<span class="icon"><i class="fas fa-times"></i></span>
							</button>
						</div>
					</div>
				</li>
			</ul>
		</div>
	</div>


	<!-- SPECIFY DECLINE REASON MODAL -->
	<div v-bind:class="{ 'is-active': pending_requests.modals.reject_reason.show }" class="modal">
		<div class="modal-background" v-on:click="clear_and_close_reject_reason_modal"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<span class="modal-card-title">Decline request</span>
				<button v-on:click="clear_and_close_reject_reason_modal" class="delete" aria-label="close"></button>
			</header>

			<section class="modal-card-body has-text-left">
				<InputBox input_type="textarea" v-model="pending_requests.modals.reject_reason.content.reject_reason"
						  v-bind:errors="pending_requests.modals.reject_reason.errors.reject_reason"
						  placeholder="Specify the reason for declining the request" label="Reject Reason"
						  icon="fas fa-info-circle" />

				<FormErrors v-bind:errors="pending_requests.modals.reject_reason.errors.detail" />
				<FormErrors v-bind:errors="pending_requests.modals.reject_reason.errors.non_field_errors" />
			</section>

			<footer class="modal-card-foot">
				<div class="columns is-mobile" style="width: 100%;">
					<div class="column has-text-right">
						<button v-on:click="reject_pending_request" class="button is-danger">Confirm</button>
						<button v-on:click="clear_and_close_reject_reason_modal" class="button">Close</button>
					</div>
				</div>
			</footer>
		</div>
	</div>


	<!-- VIEW PARTICULAR REQUEST DETAILS MODAL -->
	<div v-bind:class="{ 'is-active': pending_requests.modals.request_details.show }" class="modal">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Request details</p>
				<button v-on:click="pending_requests.modals.request_details.show=false" class="delete" aria-label="close"></button>
			</header>

			<div class="modal-card-body">
				<div class="content">
					<div>
						<strong>Statement of purpose</strong>
						<p>{{ pending_requests.modals.request_details.content.statement_of_purpose }}</p>
					</div>
					<hr/>
					<div>
						<strong>Commitment</strong>
						<p>{{ pending_requests.modals.request_details.content.commitment }}</p>
					</div>
					<hr/>
					<div>
						<strong>Expectations</strong>
						<p>{{ pending_requests.modals.request_details.content.expectations }}</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
</template>


<script>
import { mapGetters, mapState } from "vuex";
import axios from "../../api/my-axios";
import InputBox from "../FormHelpers/InputBox";
import FormErrors from "../FormHelpers/FormErrors";

export default {
	name: "MenteePendingRequests",
	components: {
		InputBox,
		FormErrors,
	},
	data() {
		return {
			pending_requests: {
				request_token: {

				},

				errors: {},

				delete_index: -1, // The index of the request in data being declined

				modals: {
					reject_reason: {
						show: false,
						content: {
							reject_reason: ""
						},
						errors: {},
					},

					request_details: {
						show: false,
						content: {
							statement_of_purpose: "",
							commitment: "",
							expectations: ""
						}
					}
				},

				data: [
					// {
					//
					// }
				],
			}
		};
	},
	computed: {
		...mapState({
			user: "user"
		}),
		// ...mapGetters({
		// 	role: "role"
		// })
	},
	created() {
		this.pending_requests.request_token.mentor = this.user.profile_uid;
		this.get_pending_mentorship_requests();
	},
	methods: {
		clear_reject_reason_modal()
		{
			for (const key in this.pending_requests.modals.reject_reason.content) {
				this.pending_requests.modals.reject_reason.content[key] = "";
			}

			this.pending_requests.modals.reject_reason.errors = {};
		},

		clear_and_close_reject_reason_modal()
		{
			this.clear_reject_reason_modal();
			this.pending_requests.modals.reject_reason.show = false;
		},

		show_request_details(index)
		{
			if (index < 0 || index >= this.pending_requests.data.length) { return; }

			for (const key in this.pending_requests.modals.request_details.content) {
				this.pending_requests.modals.request_details.content[key] = this.pending_requests.data[index][key];
			}

			this.pending_requests.modals.request_details.show = true;
		},

		show_reject_reason_modal(index)
		{
			if (index < 0 || index >= this.pending_requests.data.length) { return; }
			this.pending_requests.delete_index = index;
			this.pending_requests.modals.reject_reason.show = true;
		},

		get_pending_mentorship_requests()
		{
			axios
				.get("/api/mentorship/request/", {
					params: {
						...this.pending_requests.request_token
					}
				})
				.then(response => {
					console.log(response.data);
					this.pending_requests.data = response.data;
				})
				.catch(error => {
					this.pending_requests.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		accept_pending_request(index) {
			if (index < 0 || index >= this.pending_requests.data.length) { return; }

			// TODO Set the URL
			axios
				.delete(`/api/mentorship/request/respond/${this.pending_requests.data[index].uid}/`, {
					data: {
						mentee: this.pending_requests.data[index].mentee,
						...this.pending_requests.request_token,
					}
				})
				.then(_ => {
					this.pending_requests.data.splice(index, 1);
				})
				.catch(error => {
					this.pending_requests.errors = error.response.data;
				});
		},

		reject_pending_request() {
			if (this.pending_requests.delete_index < 0 || this.pending_requests.delete_index >= this.pending_requests.data.length) { return; }

			// TODO Set the URL
			axios
				.delete(`/api/mentorship/request/respond/${this.pending_requests.data[this.pending_requests.delete_index].uid}/`, {
					data: {
						mentee: this.pending_requests.data[this.pending_requests.delete_index].mentee,
						...this.pending_requests.request_token,
					}
				})
				.then(_ => {
					this.pending_requests.data.splice(this.pending_requests.delete_index, 1);
				})
				.catch(error => {
					this.pending_requests.errors = error.response.data;
				});
		}
	}
}
</script>

<style scoped>
.pending-requests td {
	border: none !important;
}
</style>
