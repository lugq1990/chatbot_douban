

function validate(){
    var username =  valueOf("username");
    var email = valueOf("email");
    var password = valueOf("password");
    var repassword = valueOf("repassword");

    vali_user = validateUsername(username);
    vali_email = validateEmail(email);
    vali_pass = validatePassword(password, repassword);

    // add with confirm
    confirmSignup();  
}

function validateLogin(){
    var username =  valueOf("username");
    var password = valueOf("password");

    vali_user = validateUsername(username);
    vali_pass = validateLoginPassword(password);
}


function validateLoginPassword(password){
    var errro_msg;

    if (password == ""){
        errro_msg = "Password must be provided!"
        alert_msg(errro_msg)
    }

    return errro_msg;
}
    

function confirmSignup(){
    var confirmInfor;
    if (confirm("Do you want to signup?") == true){
        confirmInfor = "Data saved";
    } else{
        confirmInfor = "Save fail";
    }
    document.getElementById("msg").innerHTML = confirmInfor
}


function isReal(obj){
    return !!obj
}

function alert_msg(msg){
    if (isReal(msg)){
        alert(msg)
    }
}


function validateUsername(username){
    var errro_msg;
    if (username == ''){
        errro_msg = "Username must be provided!"
        alert_msg(errro_msg)
    }
    
    return errro_msg;
}


function validateEmail(email){
    var errro_msg;
    if (email == ""){
        errro_msg = "Please provide a email!"
        alert_msg(errro_msg)
    }
    
    if (email.indexOf("@") == -1){
        errro_msg = "Email should be a validate email";
        alert_msg(errro_msg)
    }

    return errro_msg;
}


function validatePassword(password, repassword){
    var errro_msg;

    if (password == ""){
        errro_msg = "Password must be provided!"
        alert_msg(errro_msg)
    }
    
    if (password != repassword){
        errro_msg = "Password should be same"
        alert_msg(errro_msg)
    }

    return errro_msg;
}


function valueOf(name) {
	return document.getElementsByName(name)[0].value;
}