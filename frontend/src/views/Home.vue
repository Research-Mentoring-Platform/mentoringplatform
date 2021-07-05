<template>
<div class="container has-text-centered">
	<div v-if="logged_in">
		<p class="title">
			Hi {{ user.first_name }} !
		</p>
		<p class="subtitle"></p>
	</div>
	<div v-else>
		<p class="title">
			Hi visitor !
		</p>
		<p class="subtitle"></p>
	</div>
</div>
</template>


<script>
import { mapGetters, mapState } from "vuex";

export default {
	computed: {
		...mapGetters({
			logged_in: "logged_in"
		}),
		...mapState({
			user: "user"
		})
	}
}
</script>
