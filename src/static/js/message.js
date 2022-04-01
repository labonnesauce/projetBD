let timeout = 2000;

if(document.getElementById("msg-erreur") != undefined) {
    setTimeout(() => {
        document.getElementById("msg-erreur").style.opacity = "0";
    }, timeout)
}

if(document.getElementById("msg-succes") != undefined) {
    setTimeout(() => {
        document.getElementById("msg-succes").style.opacity = "0";
    }, timeout)
}

