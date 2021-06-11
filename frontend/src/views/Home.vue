<template>
	<div class="hero-body">
		<div class="container has-text-centered">
			<p class="title">
				Title
			</p>
			<p class="subtitle">
				Subtitle
			</p>
		</div>
	</div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
	computed: {
		...mapGetters({
			logged_in: 'logged_in'
		})
	}
}
</script>
