<template>
<div>
	<div class="title is-3 has-text-centered">
		<span>
			Experience
		</span>
	</div>

	<div class="field has-text-left">
		<label class="label">Designation</label>
		<div class="control">
			<div class="select is-fullwidth">
				<select v-model="selected_uid.designation">
					<option v-for="designation in field_options.designation"
							v-bind:key="designation.uid"
							v-bind:value="designation.uid">
						{{ designation.label }}
					</option>
				</select>
			</div>

			<div class="content">
				<FormErrors v-bind:errors="errors.designation" />
			</div>
		</div>
	</div>

	<div class="field has-text-left">
		<label class="label">Department</label>
		<div class="control">
			<div class="select is-fullwidth">
				<select v-model="selected_uid.department">
					<option v-for="department in field_options.department"
							v-bind:key="department.uid"
							v-bind:value="department.uid">
						{{ department.label }}
					</option>
				</select>
			</div>

			<div class="content">
				<FormErrors v-bind:errors="errors.department" />
			</div>
		</div>
	</div>

	<div class="field has-text-left">
		<label class="label">Discipline</label>
		<div class="control">
			<div class="select is-fullwidth">
				<select v-model="selected_uid.discipline">
					<option v-for="discipline in field_options.discipline"
							v-bind:key="discipline.uid"
							v-bind:value="discipline.uid">
						{{ discipline.label }}
					</option>
				</select>
			</div>

			<div class="content">
				<FormErrors v-bind:errors="errors.discipline" />
			</div>
		</div>
	</div>

	<div class="field has-text-left">
		<label class="label">Specialization</label>
		<div class="control">
			<textarea v-model="specialization" class="textarea is-fullwidth"></textarea>
		</div>

		<div class="content">
			<FormErrors v-bind:errors="errors.specialization" />
		</div>
	</div>

	<br/>

	<div class="control">
		<button v-on:click="save" class="button is-fullwidth is-success">Update</button>
	</div>
</div>
</template>


<script>
import axios from "@/api/my-axios";
import FormErrors from "@/components/FormErrors";

export default {
	components: {
		FormErrors
	},
	data() {
		return {
			field_options: {
				designation: [],
				department: [],
				discipline: []
			},

			selected_uid: {
				designation: null,
				department: null,
				discipline: null,
			},
			specialization: "",

			errors: {
				designation: [],
				department: [],
				discipline: [],
				specialization: [],
			},
		};
	},
	created()
	{
		// TODO Try to fetch all three field options in one-go
		for (const key in this.field_options) {
			this.get_field_options(key, `/api/mentee/${key}`);
		}
		this.get_currently_selected_options();
	},
	methods: {
		get_field_options(key, url)
		{
			axios
				.get(url)
				.then(response => { this.field_options[key] = response.data; });
		},

		get_currently_selected_options()
		{
			axios
				.get(`/api/mentee/mentee/${this.$store.state.current_user.profile_uid}`)
				.then(response => {
					for (let field in this.field_options) {
						this.selected_uid[field] = response.data[field];
					}
					this.specialization = response.data.specialization;
				});
		},

		save()
		{
			const data = {
				designation: this.selected_uid.designation,
				department: this.selected_uid.department,
				discipline: this.selected_uid.discipline,
				specialization: this.specialization,
			};

			axios
				.patch(`/api/mentee/mentee/${this.$store.state.current_user.profile_uid}/`, data)
				.catch(error => { this.errors = {...error.response.data}; });
		}
	}
}
</script>
