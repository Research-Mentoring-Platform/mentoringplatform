<template>
<section class="hero is-light is-fullheight">
	<Navbar/>
	<div class="hero-body pt-2">
		<router-view />
	</div>

	<Loading />
</section>
</template>


<script>
import Navbar from "./components/Navbar";
import Loading from "./components/Loading";

export default {
	components: {
		Navbar,
		Loading
	}
}
</script>
