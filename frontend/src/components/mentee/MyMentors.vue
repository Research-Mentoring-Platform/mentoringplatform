<template>
<div class="container">
	<div class="title has-text-centered">
		My Mentors
	</div>

	<FormErrors v-bind:errors="mentorships.errors.detail" />

	<div class="columns is-centered">
		<div class="column is-5" style="max-height: min(600px, 60vh); overflow-y: auto;">
			<ul v-if="mentorships.data.length === 0">
				<li class="box has-text-centered is-centered has-text-weight-bold has-background-white">
					No mentors
				</li>
			</ul>
			<ul v-else>
				<li v-for="mentorship in mentorships.data" class="box is-rounded mb-4">
					<div class="columns is-vcentered">
						<div class="column">
							<router-link v-bind:to="{ name: 'MentorProfile', params: { profile_uid: mentorship.mentor } }"
										 class="hyperlink">
								{{ mentorship.mentor_name }}
							</router-link>
						</div>

						<div class="column is-narrow">
							<!-- TODO Change the following to router-link to the specific mentor-mentee page -->
							<router-link v-bind:to="{ name: 'Mentorship', params: { mentorship_uid: mentorship.uid } }"
										 class="button is-info">Mentorship Page</router-link>
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
import FormErrors from "../FormHelpers/FormErrors";

export default {
	name: "MyMentors",
	components: {
		FormErrors
	},
	computed: {
		...mapState({
			user: "user"
		})
	},
	data() {
		return {
			mentorships: {
				request_token: {
					// mentee: ""
				},

				errors: {},

				data: [
					// {
					// 	uid: "",
					// 	mentor: "",
					// 	mentee: "",
					// }
				]
			},
		};
	},
	created() {
		this.mentorships.request_token.mentee = this.user.profile_uid;
		this.get_mentorships();
	},
	methods: {
		get_mentorships()
		{
			axios
				.get("/api/mentorship/mentorship/", {
					params: {
						...this.mentorships.request_token
					}
				})
				.then(response => {
					this.mentorships.data = response.data;
				})
				.catch(error => {
					this.mentorships.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},
	}
}
</script>
