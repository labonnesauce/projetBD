let timeout = 4000;

if(document.getElementById("msg-erreur") != undefined) {
    setTimeout(() => {
        document.getElementById("msg-erreur").classList.add("fadeout");
    }, timeout)
}

if(document.getElementById("msg-succes") != undefined) {
    setTimeout(() => {
        document.getElementById("msg-succes").classList.add("fadeout");
    }, timeout)
}

