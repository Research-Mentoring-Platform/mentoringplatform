<template>
<div class="container">
	<div class="columns is-vcentered">
		<div class="column is-offset-1 is-3">
			<div class="title has-text-centered">
				Mentor Profile
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
import Experience from "../common/Experience";
import Education from "../common/Education";
import Research from "../common/Research";
import MentorSettings from "./MentorSettings";

export default {
	name: "MentorProfile",
	components: {
		Experience,
		Education,
		Research,
		MentorSettings
	},
	data() {
		return {
			to_show: "Experience",
		};
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