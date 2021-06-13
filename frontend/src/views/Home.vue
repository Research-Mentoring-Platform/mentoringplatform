<template>
<div class="hero-body">
	<div class="container has-text-centered">
		<div v-if="logged_in">
			<p class="title">
				You are logged in
			</p>
			<p class="subtitle">

			</p>
		</div>
		<div v-else>
			<p class="title">
				You are logged out
			</p>
			<p class="subtitle">
			</p>
		</div>
	</div>
</div>
</template>


<script>
import { mapGetters } from "vuex";

export default {
	computed: {
		...mapGetters({
			logged_in: "logged_in"
		})
	}
}
</script>
