actualChatId = "{{chatId}}"

    async function sendLoginData() {
        let fd = new FormData();
        let token = '{{ csrf_token }}';
        
        fd.append('username', username.value);
        fd.append('password', password.value)
        fd.append('csrfmiddlewaretoken', token);
        
        try {
            let response = await fetch('/login/', {
                method: 'POST',
                body: fd
            });
            
            if(response.ok && response.redirected)
                window.location.replace(response.url);
            else{
                const error = await response;
                console.log(error)
                document.getElementById('p2').classList.add('d-none');
                document.getElementById('errorMessage').innerHTML = `<span style="color: red">Password or username incorrect <br/> please try again</span>`;
                username.value = '';
                password.value = '';
            }

        } catch (e) {
            console.error('An error occured', e);
    }
}

async function sendRegisterData() {
    document.getElementById('p2').classList.remove('d-none');
    let fd = new FormData();
    let token = '{{ csrf_token }}';
    
    fd.append('username', username.value);
    fd.append('email', email.value);
    fd.append('password1', password1.value)
    fd.append('password2', password2.value)
    fd.append('csrfmiddlewaretoken', token);
    
    try {
        
        let response = await fetch('/sign_up/', {
            method: 'POST',
            body: fd
        });
         
        if(response.ok && response.redirected)
        window.location.replace(response.url);
        else{
        const error = await response;
        console.log(error)
        document.getElementById('p2').classList.add('d-none');
        document.getElementById('errorMessage').innerHTML = `<span style="color: red">username or email are already taken or password does not fit the password rules <br/> please try again</span>`;
        username.value = '';
        email.value = "";
        password1.value = '';
        password2.value = '';
    }

    } catch (e) {
        console.error('An error occured', e);
    }
}


async function sendMessage() {
    document.getElementById('p2').classList.remove('d-none');
    let fd = new FormData();
    let token = '{{ csrf_token }}';
    let fetchUrl = "/chat/"+actualChatId+"/"
    let textfield =  messageField.value

    
    fd.append('textmessage', messageField.value);
    fd.append('csrfmiddlewaretoken', token);

    try {
    messageContainer.innerHTML += `
    <div id="deleteMessage">
        <div id="loggedInUserMessage">
            <div id="card">
                <div style="height: 30px; display: flex; justify-content: flex-start;">
                    <p style="font-size: 25px; height: 30px;">{{ request.user.username }}</p>
                </div>
                <div>
                    ${textfield}
                </div>
                <div id="createdAt">
                    <span>{{created}}</span>
                </div>
          </div>
        </div>
    
    </div>`;

        let response = await fetch(fetchUrl, {
            method: 'POST',
            body: fd
        });
        let json = await response.json();
        let jsonObject = JSON.parse(json);
        console.log('json is: ', jsonObject);
        document.getElementById('deleteMessage').remove();

        messageContainer.innerHTML += `
        <div>
            <div id="loggedInUserMessage">
                <div id="card" style="background-color: #E3F2FD">
                    <div style="height: 30px; display: flex; justify-content: flex-start;">
                        <p style="font-size: 25px; height: 30px;">{{ request.user.username }}</p>
                    </div>
                    <div>
                        ${textfield}
                    </div>
                    <div id="createdAt">
                        <span>today</span>
                    </div>
              </div>
            </div>
        
        </div>`;
        document.getElementById('p2').classList.add('d-none');
        messageField.value ='';

    } catch (e) {
        console.error('An error occured', e);
    }

}

function renderAllChats(){
    window.location.replace("/");
}

async function addChatFunction(userId){
    let fd = new FormData();
    let token = '{{ csrf_token }}';

    fd.append('userId', userId);
    fd.append('csrfmiddlewaretoken', token);
    try {
   
    let response = await fetch('/', {
            method: 'POST',
            body: fd
    });

    let json = await response.json();
    let responseObject = JSON.parse(json);
    console.log("hier ich worke", responseObject.pk)
    openChatFunction(responseObject.pk)

} catch (e) {
    console.error('An error occured', e);
}
}

function openChatFunction(chatId){
    console.log('Success!!');
    let url = "/chat/"+chatId
    window.location.replace(url);
}
