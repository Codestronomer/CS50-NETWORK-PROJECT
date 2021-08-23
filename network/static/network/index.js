document.addEventListener('DOMContentLoaded', function() {
    const like_buttons = document.querySelectorAll('#likes_count')
    like_buttons.forEach(element => {
        let likes = 0;
        element.innerHTML = likes
    })

    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'like btn btn-danger') {
            let post = int(document.querySelector('#likes_count').innerHTML)
            post = post++
            document.querySelector('#likes_count').innerHTML = post
        }
    })
})




