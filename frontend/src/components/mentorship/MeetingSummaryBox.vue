<template>
<div class="box p-4" style="overflow-wrap: anywhere;">
	<div class="columns is-vcentered">
		<div class="column is-3">
			<div class="box has-background-light is-shadowless py-2 px-3">
				{{ meeting_summary.date_time }}
			</div>
		</div>

		<div class="column">
			<div class="is-size-5 meeting-summary-title">
				{{ meeting_summary.duration }}
			</div>
		</div>

		<div class="column is-narrow">
			<button v-on:click="$emit('show_meeting_summary_details')" class="button is-info mr-2">
				<span class="icon">
					<i class="fas fa-info"></i>
				</span>
			</button>

			<a v-bind:href="meeting_summary.url" target="_blank" class="button is-warning mr-2">
				<span class="icon">
					<i class="fas fa-external-link-alt"></i>
				</span>
			</a>

			<button v-on:click="$emit('edit_meeting_summary')" class="button is-success mr-2">
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
	name: "MeetingSummaryBox",
	props: {
		meeting_summary: {
			type: Object
			// Keys: DateTime, Duration, Description, Todos, NextMeetingDateTime, NextMeetingAgenda
		}
	},
	emits: [
		"edit_meeting_summary",
		"show_meeting_summary_details"
	]
}
</script>
