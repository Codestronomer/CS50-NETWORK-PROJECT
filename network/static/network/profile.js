


function getCookie(cookie_name) {
    let name = cookie_name + '=';
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

const csrftoken = getCookie('csrftoken')


// Handles follow functionality

follow_button = document.querySelector(".follow_button")
follow_button.addEventListener('click', () => {
    user_id = follow_button.getAttribute('data-id')
    action = follow_button.getAttribute("data-action")

    // Makes a post request to the server
    fetch('/follow', {
        method: "POST",
        headers: {"X-CSRFtoken": csrftoken},
        body: JSON.stringify({'user_id':user_id, 'action': action})
    }).then(response => {
        if (response.status == 200) {
            follow_button = document.querySelector(".follow_button")
            action = follow_button.getAttribute("data-action")
            let total_followers = parseInt(document.querySelector("#followers_count").innerHTML)
            if (action == "follow") {
                follow_button.setAttribute('data-action', 'unfollow')
                follow_button.innerHTML = "Following";
                document.querySelector("#followers_count").innerHTML = (parseInt(total_followers) + 1)
            } else {
                follow_button.setAttribute('data-action', 'follow');
                follow_button.innerHTML = "Follow";
                document.querySelector("#followers_count").innerHTML = (parseInt(total_followers) - 1)
            }
        }
    })
})
