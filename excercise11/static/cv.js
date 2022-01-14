function say_hello(){
   console.log('hello');
}


fetch('/users')
  .then(response => response.json())
  .then(users => {
        const users_html = users.users.map(user => {
            return `<li>Name: ${user.name}, Email: ${user.email}, Nickname: ${user.nickname} </li>`
        }).join('');

        const html = `Users: <ol> ${users_html} </ol>`
        document.querySelector("#users").insertAdjacentHTML("afterbegin", html);
   }).catch(error => console.log(error));
