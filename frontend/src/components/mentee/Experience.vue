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
				<select ref="selected_designation">
					<option v-for="designation in fields.designation"
							v-bind:key="designation.uid">
						{{ designation.label }}
					</option>
				</select>
			</div>
		</div>
	</div>

	<div class="field has-text-left">
		<label class="label">Department</label>
		<div class="control">
			<div class="select is-fullwidth">
				<select ref="selected_department">
					<option v-for="department in fields.department"
							v-bind:key="department.uid">
						{{ department.label }}
					</option>
				</select>
			</div>
		</div>
	</div>

	<div class="field has-text-left">
		<label class="label">Discipline</label>
		<div class="control">
			<div class="select is-fullwidth">
				<select ref="selected_discipline">
					<option v-for="discipline in fields.discipline"
							v-bind:key="discipline.uid">
						{{ discipline.label }}
					</option>
				</select>
			</div>
		</div>
	</div>

	<div class="field has-text-left">
		<label class="label">Specialization</label>
		<div class="control">
			<textarea v-model="specialization" class="textarea is-fullwidth"></textarea>
		</div>
	</div>

	<br/>

	<div class="control">
		<button v-on:click="save" class="button is-fullwidth is-success">Update</button>
	</div>
</div>
</template>


<script>
"use-strict";
import axios from "../../api/my-axios";

export default {
	data() {
		return {
			fields: {
				designation: [],
				department: [],
				discipline: []
			},
			specialization: "",
			selected_designation: 0,
			selected_department: 0,
			selected_discipline: 0,
		};
	},
	created() {
		for (let key in this.fields) {
			this.set_field_options(key, `/api/mentor/${key}`);
		}
	},
	methods: {
		set_field_options(key, url) {
			axios.get(url, {
				headers: { Authorization: `Bearer ${this.$store.state.access_token}` }
			}).
			then(response => {
				this.fields[key] = response.data;
			});
		},
		save() {
			const data = {
				designation: this.fields.designation[this.$refs.selected_designation.options.selectedIndex].uid,
				department: this.fields.department[this.$refs.selected_department.options.selectedIndex].uid,
				discipline: this.fields.discipline[this.$refs.selected_discipline.options.selectedIndex].uid,
				specialization: this.specialization,
			};

			// axios.post(`/api/mentor/${key}`, data);
			console.log(data);
		}
	}
}
</script>
