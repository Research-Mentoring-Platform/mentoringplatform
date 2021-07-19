<template>
<div class="container">
	<div v-if="!is_loading" class="columns">
		<div class="column is-5">
			<Meetings v-bind:mentorship_uid="$route.params.mentorship_uid" />
		</div>

<!--		<div class="column is-4">-->
<!--			<MeetingSummaries v-bind:mentorship_uid="$route.params.mentorship_uid" />-->
<!--		</div>-->

		<div class="column is-offset-1 is-5">
			<Milestones v-bind:mentorship_uid="$route.params.mentorship_uid" />
		</div>
	</div>
</div>
</template>


<script>
import Meetings from "../../components/mentorship/Meetings";
import MeetingSummaries from "../../components/mentorship/MeetingSummaries";
import Milestones from "../../components/mentorship/Milestones";
import {mapGetters, mapState} from "vuex";
import axios from "../../api/my-axios";

export default {
	components: {
		Meetings,
		MeetingSummaries,
		Milestones
	},
	computed: {
		...mapState({
			user: "user"
		}),
		...mapGetters({
			role: "role"
		})
	},
	data() {
		return {
			is_loading: true
		};
	},
	created() {
		axios
			.get("/api/mentorship/mentorship/", {
				params: {
					uid: this.$route.params.mentorship_uid
				}
			})
			.then(response => {
				if (!response.data) {
					this.$router.replace({ name: "HomePage" });
				}

				// TODO Is the following check needed?
				// const mentorship = response.data[0];
				// if (mentorship[this.role] !== this.user.profile_uid) {
				// 	this.$router.replace({ name: "HomePage" });
				// }

				this.is_loading = false; // Important
			})
			.catch(error => {
				console.error(error);
				this.$router.replace({ name: "HomePage" });
			});
	}
}
</script>
