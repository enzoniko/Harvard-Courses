//When the content is loaded
document.addEventListener('DOMContentLoaded', () => {

    //If the form for the name of the user is appearing
    if (document.querySelector('#formDisplay')){

        //When the form is submitted
        document.querySelector('#formDisplay').onsubmit = () => {

            //Create a new AJAX request
            let request = new XMLHttpRequest();

            //Get the name of the user
            let name = document.querySelector('#name').value;

            //Assign name value to submit
            let data = new FormData();
            data.append('name', name);

            //Open the existing request
            request.open('POST', '/name');

            //Send the request
            request.send(data)

            //When the response is received
            request.onload = () => {

                //If it returns success
                let data = JSON.parse(request.responseText);
                if (data.success){

                    //Hide the form
                    document.querySelector('#form').style.display = 'none';

                    //Create an 'h3' element welcoming the username
                    let h = document.createElement('h3');
                    h.style.color = '#fd65fd';
                    h.innerHTML = 'Welcome' + ' ' + data.name + '!';
                    

                    //Update the username data with the username name
                    document.querySelector('#user-data').dataset.username = data.name;

                    //Append the h3 element into the DisplayName div
                    document.querySelector('#DisplayName').append(h);

                    //Show the container that creates channels
                    document.querySelector('#channelContainer').style.display = '';
                }
                //If it was a failure
                else{
                    //Display an error message
                    document.querySelector('#DisplayName').innerHTML = 'Humm!, Unfortunaly there was an error. Please try again';
                }       
            }
            return false;
        }
    }
});