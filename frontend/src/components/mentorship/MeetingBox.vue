<template>
<div class="box p-4" style="overflow-wrap: anywhere;">
	<div class="columns is-vcentered mb-1">
		<div class="column">
			<div class="box has-background-light is-size-5 is-shadowless p-2">
				{{ meeting.title }}
			</div>
		</div>
	</div>

	<div class="columns">
		<div class="column has-text-left is-narrow">
			<div class="box is-italic has-background-info-light is-shadowless is-flex is-justify-content-center p-2">
				{{ meeting.date_time }}
			</div>
		</div>

		<div class="column has-text-right">
			<button v-on:click="$emit('add_meeting_summary')" class="button is-primary mr-2" title="Add meeting summary">
				<span class="icon">
					<i class="fas fa-plus"></i>
				</span>
			</button>

			<button v-on:click="$emit('show_meeting_agenda')" class="button is-info mr-2">
				<span class="icon">
					<i class="fas fa-info"></i>
				</span>
			</button>

			<a v-bind:href="meeting.url" target="_blank" class="button is-warning mr-2">
				<span class="icon">
					<i class="fas fa-external-link-alt"></i>
				</span>
			</a>

			<button v-on:click="$emit('edit_meeting')" class="button is-success">
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
	name: "MeetingBox",
	props: {
		meeting: {
			type: Object
			// Keys: Date_Time, Title, Agenda, URL
		}
	},
	emits: [
		"edit_meeting",
		"show_meeting_agenda",
		"add_meeting_summary"
	]
}
</script>
