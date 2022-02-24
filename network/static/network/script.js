edit = document.querySelectorAll(".btn-post");

edit.forEach((element) => {
    element.addEventListener("click", () => {
        console.log(element);
        btnEdit(element, element.dataset.post);
    })
})

function btnEdit(element, post) {
    editPost = document.getElementById(`post-edit-${post}`);
    content = document.getElementById(`${post}`);
    btnCanceling = document.getElementById(`btn-cancel-${post}`);


    if (element.innerHTML == "Edit") {
        btnCanceling.style.display = 'inline-block';
        btnCanceling.onclick = function () {
            btnCancel(element, btnCanceling);
        }

        editPost.innerHTML = `${post}`;
        editPost.style.display = 'block';
        content.style.display = 'none';
        element.innerHTML = "Save";
    }

    else if (element.innerHTML == "Save") {
        id = element.getAttribute("id")
        newPost = editPost.value;

        form = new FormData();
        form.append("id", id);
        form.append("post", newPost.trim());


        fetch("/edit_post/", {
            method: "POST",
            body: form,
        }).then((res) => {
            content.style.display = 'block';
            content.innerHTML = newPost;
            editPost.style.display = 'none';
            btnCanceling.style.display = 'none';
            element.innerHTML = "Edit";
            
        });


    }

    else {
        
        element.innerHTML = "Edit";
    
    }

}

function btnCancel(element, btnCanceling) {
    btnCanceling.style.display = 'none';
    content.style.display = 'block';
    editPost.style.display = 'none';

    element.innerHTML = "Edit"
}


//------------------------Likes----------------------------//

btnLikes = document.querySelectorAll(".fa");

btnLikes.forEach((element) => {
    element.addEventListener("click", () => {
        liked_posts(element, element.dataset.id);
    })
});

function liked_posts(element, id) {
    status_post = element.dataset.status;
    counting = document.querySelector(`#counting-${id}`);

    console.log(id)
    console.log(status_post)
    console.log(counting)

    form = new FormData();
    form.append("id", id);
    form.append("liked", status_post);


    fetch("/liked_post/", {
        method: "POST",
        body: form,
    })
        .then((res) => res.json())
        .then((res) => {
            if (res.status == 201) {
                if (res.status_post === "on") {
                    element.setAttribute("data-status", res.status_post);
                    element.src = "/media/001-like.png";
                    counting.textContent = res.likes_counting;
                } else {
                    element.setAttribute("data-status", res.status_post);
                    element.src = "/media/like (1).png";
                    counting.textContent = res.likes_counting;
                }
            }
        })
}

//-------------------------follow btn-----------------------------//

follow = document.querySelector("#btn-follow");

follow.addEventListener("click", (element) => {
    user = follow.getAttribute("data-profile");
    toggle = follow.textContent.trim();

    form = new FormData();
    form.append("id", user);
    form.append("follow", toggle);

    fetch("/follow_post/", {
        method: "POST",
        body: form,
    })
        .then((res) => res.json())
        .then((res) => {
            if (res.status == 201) {
                follow.textContent = res.toggle;
                document.querySelector("#countFollowers").textContent = `${res.follower} Followers`;
            }
        })
})

//-------------------------toggle following boxes--------------------------//

function followingBox() {

    document.querySelector('.followingBox').style.background = 'dimgrey'
    document.querySelector('.followersBox').style.background = 'none'
    document.querySelector('.containerFollows').style.background = 'none'


    followers = document.querySelectorAll('.btn-followers');
    followers.forEach((element) => {
        element.style.display = 'none';
    })

    following = document.querySelectorAll('.btn-following');
    following.forEach((element) => {
        element.style.display = 'inline-flex';
    })

    post = document.querySelectorAll('#followingPosts');
    post.forEach((element) => {
        element.style.display = 'none'
    })
}

function followerBox() {

    document.querySelector('.followingBox').style.background = 'none'
    document.querySelector('.followersBox').style.background = 'dimgrey'
    document.querySelector('.containerFollows').style.background = 'none'

    following = document.querySelectorAll('.btn-following');
    following.forEach((element) => {
        element.style.display = 'none';
    })
    
    followers = document.querySelectorAll('.btn-followers');
    followers.forEach((element) => {
        element.style.display = 'inline-flex';
    })

    post = document.querySelectorAll('#followingPosts');
    post.forEach((element) => {
        element.style.display = 'none'
    })
}

function followingPosts() {

    document.querySelector('.followingBox').style.background = 'none'
    document.querySelector('.followersBox').style.background = 'none'
    document.querySelector('.containerFollows').style.background = 'dimgrey'

    
    following = document.querySelectorAll('.btn-following');
    following.forEach((element) => {
        element.style.display = 'none';
    })
    
    followers = document.querySelectorAll('.btn-followers');
    followers.forEach((element) => {
        element.style.display = 'none';
    })

    post = document.querySelectorAll('#followingPosts');
    post.forEach((element) => {
        element.style.display = 'block'
    })

}