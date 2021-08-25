document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#like').onclick(function() {
        let catid = document.querySelector(this).data("cid");

        fetch(`/likepost`, {
            method: "GET",
            body: JSON.stringify({post_id: catid})
        }).then(response => response.data())
        .then(data => {
            let total = document.querySelector(`#${catid}`).attributes("data-total")
            if (document.querySelector(`#${data-value}`) == 'Like') {
                document.querySelector(`#like${catid}`).text((pasrseInt(total) + 1));
                document.querySelector(`#heart${catid}`).css('color', 'red')
                document.querySelector(`#${catid}`).attributes("data-total", parseInt(total) + 1)
                document.querySelector(`#${catid}`).attributes("data-value", 'unlike')
            } else {
                    document.querySelector(`#like${catid}`).text((parseInt(total) - 1));
                    document.querySelector(`heart${catid}`).css('color', 'black')
                    document.querySelector(`#${catid}`).attributes("data-total", parseInt(total) - 1)
                    document.querySelector(`#${catid}`).attributes("data-value", 'like')
                }
            })
        })
    })




