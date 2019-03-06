// Google Analytics snippet
const analyticsSnippet = "https://fonts.googleapis.com/css?family=Tangerine";

// Create consent cookies, hide consent bar
let setConsent = () => {
    document.cookie = "cookie_consent=true;max-age=604800";
    document.cookie = "ga_consent=true;max-age=604800";

    if (location.href.match(/register/) || 
        location.href.match(/login/) || 
        location.href.match(/cookie_policy/)) {
        location.reload();
    } else {
        injectGA(analyticsSnippet);
        document.getElementById('cookie-consent-container').hidden = true;
    }
};

// Inject Google Analytics into page as first element in <head>
let injectGA = (snippet) => {
    let script = document.createElement('link'); // ändra till script
    script.rel = "stylesheet"; // ahh
    script.href = snippet;      // ahhh
    let head = document.head;
    head.insertBefore(script, head.firstElementChild);
};

document.getElementById('cookie-consent').onclick = setConsent;

