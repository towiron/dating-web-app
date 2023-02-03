const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const auth_container = document.getElementById('auth_container');

signUpButton.addEventListener('click', () => {
	auth_container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	auth_container.classList.remove("right-panel-active");
});

// Сохранение данных при перезагрузке страницы
let formData = {};
const form = document.querySelector('form');
const LS = localStorage;

// Получение данных из input

form.addEventListener('input', function(event){
  formData[event.target.name] = event.target.value;
  LS.setItem('formData', JSON.stringify(formData));
});

// Восстановление данных
if (LS.getItem('formData')){
	formData = JSON.parse(LS.getItem('formData'));
	// console.log(formData)
	for (let key in formData){
		form.elements[key].value = formData[key];
	}
}