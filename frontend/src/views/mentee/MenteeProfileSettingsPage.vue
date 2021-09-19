<template>
<div class="container">
	<div class="columns is-centered">
		<div class="column is-3 pl-3 pr-0">
			<Experience is_editable />
		</div>

		<!-- VERTICAL SEPARATOR -->
		<div class="column is-narrow pl-4"></div>
		<div class="column is-narrow pr-3 vertical-divider"></div>

		<div class="column is-4 px-0">
			<Education is_editable />
		</div>

		<!-- VERTICAL SEPARATOR -->
		<div class="column is-narrow pl-3"></div>
		<div class="column is-narrow pr-3 vertical-divider"></div>

		<div class="column is-4 px-0">
			<Research is_editable />
		</div>
	</div>
</div>
</template>


<script>
import Experience from "../../components/common/Experience";
import Education from "../../components/common/Education";
import Research from "../../components/common/Research";

export default {
	components: {
		Experience,
		Education,
		Research
	}
}
</script>

<style scoped>
@media (min-width: 769px) {
	.vertical-divider {
		border-left: lightgray dashed 1px;
	}
}
</style>
