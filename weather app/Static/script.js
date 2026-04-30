function showLoading(){
    document.getElementById("loading").style.display = "block";
}

function toggleMode(){
    document.body.classList.toggle("dark");

    if(document.body.classList.contains("dark")){
        localStorage.setItem("theme", "dark");
    } else {
        localStorage.setItem("theme", "light");
    }
}

window.onload = function(){
    if(localStorage.getItem("theme") === "dark"){
        document.body.classList.add("dark");
    }
}

function getLocation(){
    navigator.geolocation.getCurrentPosition(function(pos){
        window.location.href = `/location?lat=${pos.coords.latitude}&lon=${pos.coords.longitude}`;
    });
}

setInterval(() => {
    let timeEl = document.getElementById("time");
    if(timeEl){
        timeEl.innerText = new Date().toLocaleString();
    }
}, 1000);