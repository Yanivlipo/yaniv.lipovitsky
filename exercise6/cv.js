function check_validation(){
    let phoneOK = document.getElementById("tel").checkValidity()
    let phMsg = ""
    if (phoneOK){
        phMsg = "OK";
    }
    else{
        phMsg = "Not OK";
    }
    document.getElementById("phoneVM").innerHTML = phMsg;
    let emailOK = document.getElementById("email").checkValidity()
    let emailMsg = ""
    if (emailOK){
        emailMsg = "OK";
    }
    else{
        emailMsg = "Not OK";
    }
    document.getElementById("emailVM").innerHTML = emailMsg;
    if (emailOK && phoneOK){
        alert("Information OK!")
    }
}

function move_to_contact(){
    window.location.href = "cv2.html";
}

function move_to_cv(){
    window.location.href = "cv1.html";
}