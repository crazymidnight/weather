let app = new Vue({
    el: '#app',
    data() {
        return {message: null};
    },
    mounted() {
        axios
        .get('http://localhost:8000/')
        .then(response => (this.message = response));
    }
});
