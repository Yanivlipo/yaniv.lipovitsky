
function fetchUserExternal(e){
    e.preventDefault();
    id=document.getElementById("reqid").value;
    if (id){
        console.log(id);
        fetch(`https://reqres.in/api/users/${id}`)
        .then(response => response.json())
        .then(responseJSON => addToDOM(responseJSON.data))
        .catch(err => console.log(err));
    }
}


 function addToDOM(data){
    console.log(data);
    console.log(data.avatar);
    console.log(data.first_name);
    console.log(data.last_name);
    const main = document.querySelector("main")
    const section=document.createElement('section');
    section.innerHTML=`<img src="${data.avatar}"/>
    <h1>${data.first_name}</h1>
    <h1>${data.last_name}</h1>`;
    main.parentNode.insertBefore(section,main);

}
