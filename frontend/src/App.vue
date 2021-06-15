<template>
<section class="hero is-light is-fullheight">
	<Navbar/>
	<div class="hero-body">
		<router-view/>
	</div>
</section>
</template>


<script>
import Navbar from "./components/Navbar";

export default {
	components: { Navbar }
}
</script>
