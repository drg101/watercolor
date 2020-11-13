/**
 * @author Daniel Reynolds
 * @description Library to make requests to ouy server
 * @dependencies uuid
 */

/**
* Builds the request then auto-calls @function makeRequest
* This is called by the request button
* @function buildRequest
* @returns {Object} an object with the serverURL, imageArray, and Operators
*/
function buildRequest() {
    //first collect images as base64 and shove them into an array
    let base64ImageArray = []; //make array

    let DOMImages = document.getElementsByTagName("img");

    for (image of DOMImages)
        base64ImageArray.push(image.src);
    


    if (base64ImageArray.length == 0) { //if image array is empty, block further execution
        return false;
    }
    else { //clear out the images we just collected
        for (let i = 0; i < DOMImages.length; i++) { //cant use iterator 
            image.parentNode.parentNode.removeChild(DOMImages[i].parentNode); //lol
            i--; //removed an element so decrement iterator
        }
    }

    //now collect the ops
    let ops = [];
    ops.push({ "type": document.getElementById("operations").value });
    //to-add: the dropdown should allow multiple op solection

    //now get the serverURL
    const serverURL = document.getElementById("server").value;


    //auto make request:
    makeRequest(serverURL, base64ImageArray, ops);

    //return stuff
    return { images: base64ImageArray, ops: ops, serverURL: serverURL };
}


/**
* Makes the ajax request to the server
* @function makeRequest
* @param {Array<string>} imageArray - Base 64 array of images
* @param {Array<Object>} operators - Operators to be performed on the images format {"type":"<type of op>", *}
* @returns {string} id of request sent
*/
function makeRequest(serverURL, imageArray, operators) {
    const q = {
        "id": uuidv4(), //much secure
        "images": imageArray,
        "ops": operators
    }


    fetch(serverURL, {
        method: 'POST', // fetch doesnt allow GET to have a body so gotta do POST
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(q),
    }
    ).then(function (response) {
        // The API call was successful!
        if (response.ok) {
            return response.json();
        } else {
            return Promise.reject(response);
        }
    }).then(function (data) {
        // This is the JSON from our response
        console.log(data);
    }).catch(function (err) {
        // There was an error
        console.warn('Something went wrong.', err);
    });
}


