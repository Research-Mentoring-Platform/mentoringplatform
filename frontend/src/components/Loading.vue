<template>
<div v-if="show_loading" class="loading-overlay">
	<div class="loader"></div>
</div>
</template>


<script>
import { mapState } from "vuex";

export default {
	computed: {
		...mapState({
			show_loading: "show_loading"
		})
	}
};
</script>


<style scoped>
.loading-overlay {
	position: absolute;
	width: 100vw !important;
	height: 100vh !important;
	z-index: 10000;
	background-color: rgba(0, 0, 0, 0.5);

	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

/* https://www.w3schools.com/howto/howto_css_loader.asp */
.loader {
	border: 16px solid #f3f3f3; /* Light grey */
	border-top: 16px solid dodgerblue;
	border-radius: 50%;
	width: 120px;
	height: 120px;
	animation: spin 2s linear infinite;
}

@keyframes spin {
	0% { transform: rotate(0deg); }
	100% { transform: rotate(360deg); }
}
</style>