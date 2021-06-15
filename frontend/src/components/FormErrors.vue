<template>
<ul class="list help is-danger">
	<li v-for="error in error_list">
		{{ error }}
	</li>
</ul>
</template>


<script>
export default {
	props: {
		errors: {
			type: Array,
			required: true,
		}
	},
	data() {
		return {
			error_list: []
		};
	},
	watch: {
		errors: function(new_value, _) {
			this.error_list = new_value;
		},
	}
}
</script>
