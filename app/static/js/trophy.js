let trophy = document.getElementById('trophy');

const setColor = (position) => {
    let color;
    switch (position) {
        case 1:
            color = "#C9AE5D"; /* "Bronze Gold" */
            break;
        case 2:
            color = "#BFC1C2"; /* "Silver Sand" */
            break;
        case 3:
            color = "#CD7F32"; /* Bronze */
            break;
        default:
            color = "#333"; /* Sexy almost-black */
    }
    trophy.style.color = color;
}