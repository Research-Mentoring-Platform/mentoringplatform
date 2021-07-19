<template>
<div class="container">
	<div v-if="!is_loading" class="columns is-vcentered">
		<div class="column is-offset-1 is-3">
			<div class="title has-text-centered">
				{{ mentee.first_name }} {{ mentee.last_name }}'s Profile
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
		</div>

		<div class="column is-offset-2 is-5 px-0">
			<transition name="fade">
				<component v-bind:is="to_show" v-bind:profile_uid="$route.params.profile_uid" user_role="mentee" />
			</transition>
		</div>
	</div>
</div>
</template>


<script>
import Experience from "../../components/common/Experience";
import Education from "../../components/common/Education";
import Research from "../../components/common/Research";
import axios from "../../api/my-axios";
import {mapState} from "vuex";

export default {
	components: {
		Experience,
		Education,
		Research
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
		if (this.user.is_mentee) {
			this.mentee = this.user;
			this.is_loading = false;
		}
		else { // Mentor is accessing
			this.get_mentee_details();
		}
	},
	methods: {
		get_mentee_details()
		{
			axios
				.get(`/api/mentee/mentee/${this.$route.params.profile_uid}/`)
				.then(response => {
					this.mentee = response.data;
					this.is_loading = false; // Important
				})
				.catch(error => {
					console.error(error);
				});
		}
	}
}
</script>
