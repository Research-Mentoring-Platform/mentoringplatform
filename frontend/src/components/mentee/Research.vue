<template>
<div>
	<div class="title level">
		<div class="level-item has-text-centered">Research</div>
		<button v-on:click="show_research_modal = true"
				class="button px-4 is-rounded is-primary"
				data-toggle="modal"
				data-target="#research-modal">
			<span class="icon">
				<i class="fa fa-plus"></i>
			</span>
		</button>
	</div>


	<!-- RESEARCH RECORDS -->
	<div v-for="(research, index) in researches" class="box pt-4 pb-3 px-4" style="overflow-wrap: anywhere;">
		<div class="columns is-variable is-1 mb-1">
			<div class="column is-one-third">
				<span style="height: 100%;" class="box level has-text-weight-bold pt-1 pb-2 px-2 has-background-light is-shadowless">
					{{ research.title }}
				</span>
			</div>
			<div class="column has-text-left">
				<span style="height: 100%;" class="box level pt-1 pb-2 px-2 has-background-light is-shadowless">
					{{ research.organization }}
				</span>
			</div>
		</div>

		<div class="columns is-vcentered">
			<div class="column has-text-left is-italic">
				{{ research.start_date }} to

				<span v-if="research.is_ongoing">Present</span>
				<span v-else>{{ research.end_date  }}</span>
			</div>

			<div class="column has-text-right">
				<button v-on:click="show_research_details(index)"
						class="button px-4 py-0 mr-2 is-info"
						data-toggle="modal"
						data-target="#research-details-modal">
					<span class="icon">
						<i class="fas fa-info"></i>
					</span>
				</button>

				<button v-on:click="edit_research(index)" class="button px-4 py-0 is-primary">
					<span class="icon">
						<i class="far fa-edit"></i>
					</span>
				</button>
			</div>
		</div>
	</div>


	<!-- VIEW PARTICULAR RESEARCH DETAILS MODAL -->
	<div v-bind:class="{ 'is-active': show_research_details_modal }" id="research-details-modal" class="modal is-rounded">
		<div class="modal-background"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Research details</p>
				<button v-on:click="show_research_details_modal = false" class="delete" aria-label="close"></button>
			</header>

			<div class="modal-card-body">
				<p class="content is-medium has-text-left">{{ research_details }}</p>
			</div>
		</div>
	</div>


	<!-- ADD/UPDATE RESEARCH MODAL -->
	<div v-bind:class="{ 'is-active': show_research_modal }" id="research-modal" class="modal">
		<div class="modal-background" v-on:click="clear_and_close_research_modal"></div>
		<div class="modal-card">
			<header class="modal-card-head">
				<p class="modal-card-title">Add Research</p>
				<button v-on:click="clear_and_close_research_modal" class="delete" aria-label="close">
				</button>
			</header>

			<section class="modal-card-body">
				<div class="content">

					<div class="field has-text-left">
						<label class="label">Title</label>
						<div class="control has-icons-left">
							<input v-model="modal.title" class="input" type="text" required>
							<span class="icon is-small is-left">
							  	<i class="fas fa-heading"></i>
							</span>
						</div>
					</div>

					<div class="field has-text-left">
						<label class="label">Organization</label>
						<div class="control has-icons-left">
							<input v-model="modal.organization" class="input" type="text" required>
							<span class="icon is-small is-left">
							  	<i class="fas fa-school"></i>
							</span>
						</div>
					</div>

					<div class="columns">
						<div class="column field has-text-left">
							<label class="label">Start date</label>
							<div class="control has-icons-left">
								<input v-model="modal.start_date" class="input" type="month" required>
								<span class="icon is-small is-left">
									<i class="fas fa-calendar"></i>
								</span>
							</div>
						</div>

						<div class="column field has-text-left pb-0">
							<label class="label">End date</label>
							<div class="control has-icons-left">
								<input v-model="modal.end_date"
									   v-bind:disabled="modal.is_ongoing"
									   class="input"
									   type="month">
								<span class="icon is-small is-left">
									<i class="fas fa-calendar"></i>
								</span>
							</div>

							<label class="checkbox mt-2">
								<input v-model="modal.is_ongoing" type="checkbox"> Is ongoing
							</label>
						</div>
					</div>

					<div class="field has-text-left pt-0">
						<label class="label">Details</label>
						<div class="control has-icons-left">
							<textarea v-model="modal.details" class="input textarea"></textarea>
							<span class="icon is-small is-left">
							  	<i class="fas fa-info-circle"></i>
							</span>
						</div>
					</div>

				</div>
			</section>

			<footer class="modal-card-foot">
				<div class="columns is-mobile" style="width: 100%;">
					<div class="column is-narrow has-text-left">
						<button v-on:click="delete_research" class="button is-danger">Delete</button>
					</div>

					<div class="column has-text-right">
						<button v-if="research_edit_index >= 0" v-on:click="update_research" class="button is-success">Update</button>
						<button v-else v-on:click="add_research" class="button is-success">Add</button>

						<button v-on:click="clear_and_close_research_modal" class="button">Cancel</button>
					</div>
				</div>
			</footer>
		</div>
	</div>
</div>
</template>


<script>
import axios from "@/api/my-axios";

export default {
	data() {
		return {
			show_research_details_modal: false,
			research_details: null,

			show_research_modal: false,
			research_edit_index: -1, // For #research-modal

			modal: {
				title: null,
				organization: null,
				start_date: null,
				end_date: null,
				is_ongoing: false,
				details: null
			},

			// TODO Sort by start-date
			researches: [] // List of researches of this user
		};
	},
	created()
	{
		this.get_researches();
	},
	methods: {
		clear_research_modal()
		{
			this.modal.title = null;
			this.modal.organization = null;
			this.modal.start_date = null;
			this.modal.end_date = null;
			this.modal.is_ongoing = false;
			this.modal.details = null;
			this.research_edit_index = -1; // Important
		},

		clear_and_close_research_modal()
		{
			this.clear_research_modal();
			this.show_research_modal = false;
		},

		show_research_details(index)
		{
			if (index >= this.researches.length) { return; }
			this.research_details = this.researches[index].details;
			this.show_research_details_modal = true;
		},

		get_researches()
		{
			axios
				.get("/api/mentorship/research/", {
					uid: this.$store.state.current_user.uid
				})
				.then(response => {
					this.researches.push(...response.data);
				})
				.catch(error => {
					console.error(error);
				});
		},

		add_research()
		{
			axios
				.post("/api/mentorship/research/", {
					user: this.$store.state.current_user.uid,
					...this.modal
				})
				.then(_ => {
					this.researches.push({...this.modal}); // Make sure to push a copy
					this.clear_and_close_research_modal();
				})
				.catch(error => {
					console.error(error);
				});
		},

		edit_research(index)
		{
			if (index >= this.researches.length) { return; }

			this.research_edit_index = index;
			this.modal = {...this.researches[this.research_edit_index]};
			this.show_research_modal = true;
		},

		update_research()
		{
			if (this.research_edit_index < 0 || this.research_edit_index >= this.researches.length) { return; }

			axios
				.put(`/api/mentorship/research/${this.researches[this.research_edit_index].uid}/`, {
					user: this.$store.state.current_user.uid, // TODO Change to profile_uid after back-end is done
					...this.modal
				})
				.then(_ => {
					this.researches[this.research_edit_index] = {...this.modal};
					this.clear_and_close_research_modal();
				});
		},

		delete_research()
		{
			if (this.research_edit_index < 0 || this.research_edit_index >= this.researches.length) { return; }

			axios
				.delete(`/api/mentorship/research/${this.researches[this.research_edit_index].uid}`, {
					user: this.$store.state.current_user.uid,
				})
				.then(_ => {
					this.researches.splice(this.research_edit_index, 1);
					this.clear_and_close_research_modal();
				});
		}
	}
}
</script>
