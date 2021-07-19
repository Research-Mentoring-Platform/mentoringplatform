<template>
<div class="container">
	<div class="title has-text-centered">
		Pending Requests
	</div>

	<FormErrors v-bind:errors="pending_requests.errors.detail" />

	<div class="columns is-centered">
		<div class="column is-5" style="max-height: min(600px, 60vh); overflow-y: auto;">
			<ul v-if="pending_requests.data.length === 0">
				<li class="box has-text-centered is-centered has-text-weight-bold has-background-white">
					No pending requests
				</li>
			</ul>
			<ul v-else>
				<li v-for="(pending_request, index) in pending_requests.data" class="box is-rounded mb-4">
					<div class="columns is-vcentered">
						<div class="column">
							<router-link v-bind:to="{ name: 'MentorProfilePage', params: { profile_uid: pending_request.mentor } }"
										 class="hyperlink">
								{{ pending_request.mentor_name }}
							 </router-link>
						</div>

						<div class="column is-narrow">
							<button v-on:click="cancel_pending_request(index)" class="button is-danger">Cancel</button>
						</div>
					</div>
				</li>
			</ul>
		</div>
	</div>
</div>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import axios from "../../api/my-axios";
import FormErrors from "../../components/FormHelpers/FormErrors";

export default {
	components: {
		FormErrors
	},
	computed: {
		...mapState({
			user: "user"
		}),
	},
	data() {
		return {
			pending_requests: {
				errors: {},

				data: [
					{

					}
				],
			}
		};
	},
	created() {
		this.get_pending_mentorship_requests();
	},
	methods: {
		get_pending_mentorship_requests()
		{
			axios
				.get("/api/mentorship/request/pending/", {
					params: {
						mentee: this.user.profile_uid
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

		cancel_pending_request(index) {
			if (index < 0 || index >= this.pending_requests.data.length) { return; }

			axios
				.delete(`/api/mentorship/request/${this.pending_requests.data[index].uid}/`, {
				})
				.then(_ => {
					this.pending_requests.data.splice(index, 1);
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
