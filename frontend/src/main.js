import {createApp} from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

const app = createApp(App);


router.beforeEach((to, from, next) => {
	if (to.matched.some(record => record.meta.requires_auth)) {
		if (!store.getters.logged_in) {
			next({ name: 'Login' })
		}
		else {
			next()
		}
	}
	else if (to.matched.some(record => record.meta.requires_visitor)) {
		if (store.getters.logged_in) {
			next({ name: 'Home' })
		}
		else {
			next()
		}
	}
	else {
		next()
	}
});


app.use(store);
app.use(router);
app.mount('#app');

// createApp(App).use(store).use(router).mount('#app');
