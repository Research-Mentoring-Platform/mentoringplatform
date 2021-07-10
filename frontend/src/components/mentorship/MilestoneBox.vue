<template>
<div class="box p-4" style="overflow-wrap: anywhere;">
	<div class="columns is-vcentered mb-1">
		<div class="column">
			<div class="box has-background-light is-size-5 is-shadowless p-2">
				{{ milestone.title }}
			</div>
		</div>
	</div>

	<div class="columns is-vcentered">
		<div class="column has-text-left is-narrow">
			<div class="box is-italic has-background-info-light is-shadowless is-flex is-justify-content-center p-2">
				{{ milestone.date }}
			</div>
		</div>

		<div class="column has-text-right">
			<button v-on:click="$emit('show_milestone_description')" class="button is-info mr-2">
				<span class="icon">
					<i class="fas fa-info"></i>
				</span>
			</button>

			<button v-on:click="$emit('edit_milestone')" class="button is-success">
				<span class="icon">
					<i class="fas fa-edit"></i>
				</span>
			</button>
		</div>
	</div>
</div>
</template>


<script>
export default {
	name: "MilestoneBox",
	props: {
		milestone: {
			type: Object
			// Keys: Date, Description
		}
	},
	emits: [
		"edit_milestone",
		"show_milestone_description"
	]
}
</script>
