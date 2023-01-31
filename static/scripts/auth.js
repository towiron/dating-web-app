const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const auth_container = document.getElementById('auth_container');

signUpButton.addEventListener('click', () => {
	auth_container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	auth_container.classList.remove("right-panel-active");
});