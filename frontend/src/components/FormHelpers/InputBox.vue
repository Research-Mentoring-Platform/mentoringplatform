<template>
<div class="field">
	<!-- TODO For label, class="checkbox" | "radio" | "label" based on input_type -->
	<label v-if="label" class="label">{{ label }}</label>

	<div class="control" v-bind:class="{'has-icons-left': icon !== null}">
		<span v-if="input_type === 'textarea'">
			<textarea v-bind:value="modelValue"
					  v-on:input="$emit('update:modelValue', $event.target.value)"
				      v-bind:placeholder="placeholder"
					  v-bind:disabled="disabled"
					  class="input textarea"
			>
			</textarea>
		</span>
		<span v-else>
			<input v-bind:value="modelValue"
				   v-on:input="$emit('update:modelValue', $event.target.value)"
				   v-bind:type="input_type"
				   v-bind:placeholder="placeholder"
				   v-bind:disabled="disabled"
				   class="input"
			/>
		</span>

		<span v-if="icon" class="icon is-left">
			<i v-bind:class="icon"></i>
		</span>
	</div>

	<FormErrors v-bind:errors="error_list" />
</div>
</template>


<script>
import FormErrors from "./FormErrors";

export default {
	components: {
		FormErrors
	},
	props: {
		modelValue: { // Change to model-value for Vue 2
			required: true
		},
		errors: {
			type: [Array, String]
		},
		input_type: {
			type: String,
			default: "text"
		},
		label: {
			type: String,
			default: null
		},
		placeholder: {
			type: String,
			default: null
		},
		disabled: {
			type: Boolean,
			default: false
		},
		icon: {
			type: String,
			default: null
		},
	},
	data() {
		return {
			error_list: []
		}
	},
	watch: {
		errors: function(new_value, old_value) {
			this.error_list = []; // Important, else old values persist
			if (new_value) {
				this.error_list = Array.isArray(new_value) ? new_value : [new_value];
			}
		}
	}
}
</script>
