document.addEventListener('DOMContentLoaded', function() {

    if (document.querySelector('#user_details')) {
        let user_info = "/get_user/"
        fetch(user_info)
        .then(response => response.json())
        .then(i => {
            const UserDetails = document.querySelector('#user_details');
            const span = document.createElement('span');
            span.innerHTML = `Balance: $${i[0].account}`;
            UserDetails.append(span);
        })
    }
});