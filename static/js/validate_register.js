

function validate(){
    email_result = validateEmail();
    alert(email_result)

    password_result = validatePassword();
    alert(password_result)
}


function validateEmail(){
    var email = valueOf("email");

    if (email == ""){
        return "Please provide a email!"
    }
    if (email.indexOf("@" == -1)){
        return "Email should be a validate email";
    }
    return ""
}


function validatePassword(){
    var password = valueOf("password");
    var repassword = valueOf("repassword");

    if (password == ""){
        return "Password must be provided!"
    }

    if (password != repassword){
        return "Password should be same"
    }
}

function valueOf(name) {
	return document.getElementsByName(name)[0].value;
}