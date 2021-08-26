
likebutton = document.querySelectorAll('.likebutton')
const csrftoken = getCookie('csrftoken')

likebutton.forEach(element => {
    element.addEventListener('click', function() {
        let catid = element.getAttribute("data-cid");
        console.log(catid)

        fetch(`/likepost/`, {
            method: "post",
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({post_id: catid}),
        }).then(response => {
            if (response.status == 200) {
                return response.json()
            }
        })
        .then(data => {
            console.log(data)
            let total = document.querySelector(`#post${catid}`).getAttribute("data-total")
            if (document.querySelector(`#post${catid}`).getAttribute == 'Like') {
                document.querySelector(`#liked${catid}`).text((pasrseInt(total) + 1));
                document.querySelector(`#heart${catid}`).css('color', 'red')
                document.querySelector(`#post${catid}`).setAttribute("data-total", parseInt(total) + 1)
                document.querySelector(`#post${catid}`).setAttribute("data-value", 'unlike')
            } else {
                document.querySelector(`#liked${catid}`).text((parseInt(total) - 1));
                document.querySelector(`#heart${catid}`).css('color', 'black')
                document.querySelector(`#post${catid}`).setAttribute("data-total", parseInt(total) - 1)
                document.querySelector(`#post${catid}`).setAttribute("data-value", 'like')
            }
        })
    })
})

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