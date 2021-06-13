<template>
<div class="columns is-centered">
	<div class="column is-3 px-0">
		<Experience></Experience>
	</div>

	<!-- VERTICAL SEPARATOR -->
	<div class="column is-narrow pl-5"></div>
	<div class="column is-narrow pr-5" style="border-left: darkgray dotted 1px;"></div>

	<div class="column is-two-fifth px-0">
		<Education></Education>
	</div>

	<!-- VERTICAL SEPARATOR -->
	<div class="column is-narrow pl-5"></div>
	<div class="column is-narrow pr-5" style="border-left: darkgray dotted 1px;"></div>

	<div class="column is-two-fifth px-0">
		<div class="title has-text-centered">
			Research
			<button class="button is-primary"
					data-toggle="modal"
					data-target="#tnc-modal">
				<i class="fa fa-plus"></i>
			</button>
		</div>

		<div class="field">
			<label class="label">Discipline</label>
			<div class="control">
				<div class="select is-fullwidth">
					<select>
						<option>Select dropdown</option>
						<option>With options</option>
					</select>
				</div>
			</div>
		</div>
	</div>
</div>
</template>


<script>
import Experience from "../../components/mentee/Experience";
import Education from "../../components/mentee/Education";

export default {
	components: {
		"Experience": Experience,
		"Education": Education
	},
	data() {
		return {};
	}
}
</script>