<template>
<div class="box p-3" style="overflow-wrap: anywhere;">
	<div class="columns is-mobile mb-0">
		<div class="column is-two-fifths">
			<span style="height: 100%" class="box level has-text-weight-bold has-background-light is-shadowless p-2">
				{{ research.title }}
			</span>
		</div>
		<div class="column has-text-left pl-0">
			<span style="height: 100%;" class="box level has-background-light is-shadowless p-2">
				{{ research.organization }}
			</span>
		</div>
	</div>

	<div class="columns is-vcentered is-mobile">
		<div class="column has-text-left is-two-fifths">
			<div class="box is-italic has-background-info-light is-shadowless is-flex is-justify-content-center py-2 px-1">
				{{ research.start_date }} to {{ research.end_date || "Present" }}
			</div>
		</div>

		<div class="column has-text-right">
			<button v-on:click="$emit('show_research_details')" v-bind:class="is_editable ? 'mr-2' : 'mr-0'"
					class="button is-info px-4 py-0">
				<span class="icon">
					<i class="fas fa-info"></i>
				</span>
			</button>

			<button v-if="is_editable" v-on:click="$emit('edit_research')" class="button is-success px-4 py-0">
				<span class="icon">
					<i class="far fa-edit"></i>
				</span>
			</button>
		</div>
	</div>
</div>
</template>


<script>
export default {
	name: "ResearchBox",
	props: {
		is_editable: {
			type: Boolean,
			default: false
		},
		research: {
			type: Object
			// Keys: Title, Organization, Start Date, [End Date], [Details]
		}
	},
	emits: [
		"edit_research",
		"show_research_details"
	]
}
</script>
