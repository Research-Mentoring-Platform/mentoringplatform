<template>
<div class="container">
	<div class="tabs is-toggle is-fullwidth pt-0 pb-5">
		<ul >
			<li v-bind:class="{'is-active': to_show === 'Experience'}">
				<a v-on:click="to_show='Experience'">
					<span class="icon"><i class="fas fa-image" aria-hidden="true"></i></span>
					<span>Experience</span>
				</a>
			</li>
			<li v-bind:class="{'is-active': to_show === 'Education'}">
				<a v-on:click="to_show='Education'">
					<span class="icon"><i class="fas fa-image" aria-hidden="true"></i></span>
					<span>Education</span>
				</a>
			</li>
			<li v-bind:class="{'is-active': to_show === 'Research'}">
				<a v-on:click="to_show='Research'">
					<span class="icon"><i class="fas fa-image" aria-hidden="true"></i></span>
					<span>Research</span>
				</a>
			</li>
		</ul>
	</div>

	<div class="columns is-centered">
		<div class="column is-5">
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

<style>
.tabs.is-toggle li.is-active a, .hero.is-light .tabs.is-toggle li.is-active a:hover {
	background-color: #3298dc !important;
}
</style>
