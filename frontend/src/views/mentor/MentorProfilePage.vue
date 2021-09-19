<template>
<div class="container">
	<div v-if="!is_loading" class="columns is-vcentered">
		<div class="column is-offset-1 is-3">
			<div class="title has-text-centered">
				{{ mentor.first_name }} {{ mentor.last_name }}'s Profile
			</div>

			<button v-on:click="to_show='Experience'" class="button is-primary is-fullwidth mb-3">
				Experience
			</button>

			<button v-on:click="to_show='Education'" class="button is-primary is-fullwidth mb-3">
				Education
			</button>

			<button v-on:click="to_show='Research'" class="button is-primary is-fullwidth mb-3">
				Research
			</button>

			<button v-on:click="to_show='MentorSettings'" class="button is-primary is-fullwidth mb-3">
				Mentor Settings
			</button>
		</div>

		<div class="column is-offset-2 is-5 px-2 scrollable">
			<transition name="fade">
				<component v-bind:is="to_show" v-bind:profile_uid="$route.params.profile_uid" user_role="mentor" />
			</transition>
		</div>
	</div>
</div>
</template>


<script>
import { mapState } from "vuex";
import axios from "../../api/my-axios";
import Experience from "../../components/common/Experience";
import Education from "../../components/common/Education";
import Research from "../../components/common/Research";
import MentorSettings from "../../components/mentor/MentorSettings";

export default {
	components: {
		Experience,
		Education,
		Research,
		MentorSettings
	},
	computed: {
		...mapState({
			user: "user"
		})
	},
	data() {
		return {
			mentee: {},
			is_loading: true,
			to_show: "Experience",
		};
	},
	created()
	{
		if (this.user.is_mentor) {
			this.mentor = this.user;
			this.is_loading = false;
		}
		else { // Mentee is accessing
			this.get_mentor_details();
		}
	},
	methods: {
		get_mentor_details()
		{
			axios
				.get(`/api/mentor/mentor/${this.$route.params.profile_uid}/`)
				.then(response => {
					this.mentor = response.data;
					this.is_loading = false; // Important
				})
				.catch(error => {
					console.error(error);
				});
		}
	}
}
</script>

<style scoped>
@media (min-width: 769px) {
	.scrollable {
		max-height: min(700px, 70vh);
		overflow-y: auto;
	}
}
</style>