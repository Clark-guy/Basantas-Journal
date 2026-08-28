
async function loadWOTD(){
    try {
        const response = await fetch("/wotd.json");
        if(!response.ok){
            throw new Error(`WOTD failed to load`)
        }
        const data = await response.json();
        console.log(data);

        //This code ripped from stack exchange. There was another version that
        //corrected for daylight savings time but I couldn't be bothered to 
        //go through the extra trouble.
        var now = new Date();
        var start = new Date(now.getFullYear(), 0, 0);
        var diff = now - start;
        var oneDay = 1000 * 60 * 60 * 24;
        var day = Math.floor(diff / oneDay);
        console.log('Day of year: ' + day);

        var wotdIndex = day%data.length;
        console.log(wotdIndex);
        document.getElementById("WOTDNepaliRoman").innerHTML = data[wotdIndex].nepali
        document.getElementById("WOTDEnglish").innerHTML = data[wotdIndex].english
        if (data[wotdIndex].devanagari){
            document.getElementById("WOTDNepaliDevanagari").innerHTML = '(' + data[wotdIndex].devanagari + ')';
        }
        else {
            document.getElementById("WOTDNepaliDevanagari").innerHTML = ""
        }

    }
    catch (err){
        throw new Error(`WOTD failed to load ${err}`)
    }
};


fetch("/components/nav.html")
    .then(res => res.text())
    .then(data => {
        document.getElementById("nav").innerHTML = data
    });

fetch("/components/header.html")
    .then(res => res.text())
    .then(data => {
        document.getElementById("header").innerHTML = data
    });

fetch("/components/wordOfTheDay.html")
    .then(res => res.text())
    .then(data => {
        document.getElementById("wotd").innerHTML = data
        loadWOTD()
    });

fetch("/components/footer.html")
    .then(res => res.text())
    .then(data => {
        document.getElementById("footer").innerHTML = data
    });



function navHide() {
    var nav = document.getElementById("nav");
    if (nav.style.display === "inline-block" ){
        nav.style.display = "none";
    }
    else {
        nav.style.display = "inline-block";
    }
}

