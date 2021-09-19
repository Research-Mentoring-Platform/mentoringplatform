# Frontend

### Pre-requisites:
1. Node JS (for `npm`)

### Steps to setup:
1. `cd` into the `frontend` folder

2. Install the dependencies:
   `npm install`
   
3. Run the project in development mode:
   `npm run serve`.
   This will start the frontend server on `http://localhost:8080/`.

**NOTE:** To compile for production use `npm run build`.

### Project Structure
- The project configuration is in the `src/main.js` file.
- The `views` folder contains the pages (or routes).
- The Vue components used in the pages are in the `src/components` folder.
- The `views` and `components` folders have the following structure:
   - `common`: Files common to both mentor and mentee
   - `mentor`: Files unique to the mentor
   - `mentee`: Files unique to the mentee
   - `mentorship`: Files unique to the mentorship between mentors and mentees
   - Files directly inside the `views` and `components` folder are for users who are not signed in (i.e. visitors)
- The Vue Router configuration is in `src/router/index.js`.
- The Vue Store (Vuex) configuration is in `src/store/index.js`.
- The custom CSS files used are in the `src/assets/styles/` folder.
- The configuration for Axios (which is used for making various requests such as `GET`, `POST`, `DELETE` etc.) is in `api/my-axios.js`.

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
