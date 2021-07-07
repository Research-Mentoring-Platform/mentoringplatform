<template>
<div class="content">
	<ul class="list help is-danger">
		<li v-for="error in error_list">
			{{ error }}
		</li>
	</ul>
</div>
</template>


<script>
export default {
	name: "FormErrors",
	props: {
		errors: {
			type: [Array, String]
		}
	},
	data() {
		return {
			error_list: []
		};
	},
	watch: {
		errors: function(new_value, _ /* old_value */) { // Cannot use () => {} as 'this' is required
			this.error_list = []; // Important, else the errors persist
			if (new_value) {
				this.error_list = Array.isArray(new_value) ? new_value : [new_value];
			}
		},
	}
}
</script>
