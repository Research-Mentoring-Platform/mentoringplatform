<template>
<MentorSettings v-bind:profile_uid="$route.params.profile_uid" v-bind:is_editable="is_editable" />
</template>

<script>
import MentorSettings from "../../components/mentor/MentorSettings";

export default {
	components: {
		MentorSettings
	},
	props: {
		is_editable: {
			type: Boolean,
			default: false,
		},
	}
}
</script>
