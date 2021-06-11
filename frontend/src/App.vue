<template>
	<section class="hero is-light is-fullheight">
		<Navbar/>
		<router-view/>
	</section>
</template>


<script>
import Navbar from "./components/Navbar";

export default {
	components: { Navbar }
}
</script>


<style></style>
