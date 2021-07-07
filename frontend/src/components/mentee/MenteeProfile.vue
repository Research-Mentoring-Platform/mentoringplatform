<template>
<div class="container">
	<div class="columns is-vcentered">
		<div class="column is-offset-1 is-3">
			<div class="title has-text-centered">
				Mentee Profile
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
				<component v-bind:is="to_show" />
			</transition>
		</div>
	</div>
</div>
</template>


<script>
import Experience from "../common/Experience";
import Education from "../common/Education";
import Research from "../common/Research";

export default {
	name: "MenteeProfile",
	components: {
		Experience,
		Education,
		Research
	},
	data() {
		return {
			to_show: "Experience",
		};
	}
}
</script>
