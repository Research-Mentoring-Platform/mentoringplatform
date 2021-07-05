<template>
<div>
	<div class="title is-3 has-text-centered">
		Experience
	</div>

	<FormErrors v-bind:errors="fields.errors.detail" />

	<div class="field">
		<label class="label">Designation</label>
		<div class="control">
			<div v-if="allow_editing" class="select is-fullwidth">
				<select v-model="fields.selected.designation.uid">
					<option v-for="designation in fields.options.designation" v-bind:value="designation.uid">
						{{ designation.label }}
					</option>
				</select>
			</div>
			<div v-else class="box is-rounded p-3">
				{{ fields.selected.designation.value }}
			</div>

			<FormErrors v-bind:errors="fields.errors.designation" />
		</div>
	</div>

	<div class="field">
		<label class="label">Department</label>
		<div class="control">
			<div v-if="allow_editing" class="select is-fullwidth">
				<select v-model="fields.selected.department.uid">
					<option v-for="department in fields.options.department" v-bind:value="department.uid">
						{{ department.label }}
					</option>
				</select>
			</div>
			<div v-else class="box is-rounded p-3">
				{{ fields.selected.department.value }}
			</div>

			<FormErrors v-bind:errors="fields.errors.department" />
		</div>
	</div>

	<div class="field">
		<label class="label">Discipline</label>
		<div class="control">
			<div v-if="allow_editing" class="select is-fullwidth">
				<select v-model="fields.selected.discipline.uid">
					<option v-for="discipline in fields.options.discipline" v-bind:value="discipline.uid">
						{{ discipline.label }}
					</option>
				</select>
			</div>
			<div v-else class="box is-rounded p-3">
				{{ fields.selected.discipline.value }}
			</div>

			<FormErrors v-bind:errors="fields.errors.discipline" />
		</div>
	</div>

	<div class="field has-text-left">
		<label class="label">Specialization</label>
		<div class="control">
			<textarea v-if="allow_editing" v-model="fields.selected.specialization.value" class="textarea is-fullwidth"></textarea>
			<div v-else class="box is-rounded p-3">
				{{ fields.selected.specialization.value }}
			</div>
		</div>

		<FormErrors v-bind:errors="fields.errors.specialization" />
	</div>

	<div v-if="allow_editing" class="control pt-2">
		<button v-on:click="save" class="button is-fullwidth is-success">Update</button>
	</div>
</div>
</template>


<script>
import { mapGetters, mapState } from "vuex";
import axios from "../../api/my-axios";
import FormErrors from "../FormHelpers/FormErrors";
import InputBox from "../FormHelpers/InputBox";

export default {
	name: "Experience",
	components: {
		InputBox,
		FormErrors
	},
	props: {
		is_editable: {
			type: Boolean,
			default: false
		},
		profile_uid: {
			type: String,
			default: null
		},
		user_role: { // "mentor" or "mentee"
			type: String,
			default: null
		}
	},
	computed: {
		...mapState({
			user: "user"
		}),
		...mapGetters({
			role: "role" // "mentor" or "mentee"
		})
	},
	data() {
		return {
			allow_editing: false,
			to_show_user_role: this.user_role,
			to_show_profile_uid: this.profile_uid,

			fields: {
				request_token: {
					// mentor or mentee: ""
				},

				errors: {},

				options: {
					designation: [],
					department: [],
					discipline: [],
				},

				selected: {
					designation: {
						uid: "",
						value: ""
					},
					department: {
						uid: "",
						value: ""
					},
					discipline: {
						uid: "",
						value: ""
					},
					specialization: {
						value: ""
					},
				}
			},
		};
	},
	created()
	{
		// TODO Try to fetch all three field options in one-go
		/* TODO Due to concurrent requests, selected options part may run before all options have been fetched
		 * leading to empty boxes. Use promises (axios.all()) or async-await to ensure proper run order
		 * */

		this.to_show_profile_uid = this.profile_uid ? this.profile_uid : this.user.profile_uid;
		this.to_show_user_role = this.user_role ? this.user_role : this.role;
		this.allow_editing = this.is_editable ? (this.to_show_profile_uid === this.user.profile_uid) : false;

		this.get_field_options();
		this.get_currently_selected_options();
	},
	methods: {
		get_field_options()
		{
			for (const field in this.fields.options) {
				axios
					.get(`/api/${this.to_show_user_role}/${field}/`)
					.then(response => {
						this.fields.options[field] = response.data;
					})
					.catch(error => {
						this.fields.errors[field] = error.response ? error.response.data : {"detail": [error.message]};
					});
			}
		},

		get_currently_selected_options()
		{
			axios
				.get(`/api/${this.to_show_user_role}/${this.to_show_user_role}/${this.to_show_profile_uid}/`)
				.then(response => { // Response contains the selected UIDs
					for (const field in this.fields.options) {
						this.fields.selected[field].uid = response.data[field];

						const obj = this.fields.options[field].find(e => e.uid === response.data[field]);
						this.fields.selected[field].value = obj ? obj.label : "";
					}

					this.fields.selected.specialization.value = response.data.specialization;
				})
				.catch(error => {
					this.fields.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		},

		save()
		{
			if (!this.allow_editing) { return; }

			axios
				.patch(`/api/${this.role}/${this.role}/${this.user.profile_uid}/`, {
					designation: this.fields.selected.designation.uid,
					department: this.fields.selected.department.uid,
					discipline: this.fields.selected.discipline.uid,
					specialization: this.fields.selected.specialization.value,
				})
				.catch(error => {
					this.fields.errors = error.response ? error.response.data : {"detail": [error.message]};
				});
		}
	}
}
</script>
