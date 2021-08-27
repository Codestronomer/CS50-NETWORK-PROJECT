
likebutton = document.querySelectorAll('.likebutton')
const csrftoken = getCookie('csrftoken')

likebutton.forEach(element => {
    element.addEventListener('click', function() {
        let catid = element.getAttribute("data-cid");
        console.log(catid)

        fetch('/like', {
            method: "POST",
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({'post_id': catid}),
        }).then(response => {
            if (response.status == 200) {
                let total = document.querySelector(`#post${catid}`).getAttribute("data-total")
            if (document.querySelector(`#post${catid}`).getAttribute("data-value") == 'Like') {
                document.querySelector(`#liked${catid}`).innerHTML = (parseInt(total) + 1);
                document.querySelector(`#heart${catid}`).style.color = 'red'
                document.querySelector(`#post${catid}`).setAttribute("data-total", parseInt(total) + 1)
                document.querySelector(`#post${catid}`).setAttribute("data-value", 'Unlike')
            } else {
                document.querySelector(`#liked${catid}`).innerHTML = (parseInt(total) - 1);
                document.querySelector(`#heart${catid}`).style.color = 'black'
                document.querySelector(`#post${catid}`).setAttribute("data-total", parseInt(total) - 1)
                document.querySelector(`#post${catid}`).setAttribute("data-value", 'Like')
            }
                return response.json()
            }
        })
        .then(data => {
            console.log(data["success"])
        })
    })
})

comment_button = document.querySelectorAll('.modal-button')
comment_button.forEach(element => {
    element.addEventListener('click', function() {
        let post_id = element.getAttribute("data-post");
        const comment = 

        fetch('/comment', {
            method: "POST", 
            headers: {"X-CSRFToken": csrftoken},
            body: JSON.stringify({
                post_id: post_id,
                content: comment
            })
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

const open = document.querySelectorAll('[data-modal-target]')
const close = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

open.forEach(element => {
    element.addEventListener('click', () => {
        const modal = document.querySelector(element.dataset.modalTarget)
        openModal(modal)
    })
});

overlay.addEventListener('click', () => {
    const modals = document.querySelectorAll('.my-modal.active')
    modals.forEach(modal => {
        closeModal(modal);
    })
})

close.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.my-modal');
        closeModal(modal);
    })
})

function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}
