/**
 * @author Daniel Reynolds
 * @description Library to make requests to ouy server
 * @dependencies uuid
 */

/**
* Builds the request then auto-calls @function makeRequest
* This is called by the request button
* @function buildRequest
* @returns {boolean} true if successful
*/
function buildRequest() {
    //first collect images as base64 and shove them into an array

    let DOMImages = document.getElementsByTagName("img");

    const ops = [{ "type": "upscale" }];
    const serverURL = document.getElementById("server").value;

    for (image of DOMImages) {
        if (!image.name) //images which have names are the ones to be upscaled
            continue;

        let namesArray = []; //names array for re-downloading
        let base64ImageArray = []; //array wrapper for image
        namesArray.push(image.name.split(".")[0]);
        base64ImageArray.push(image.src);

        makeRequest(serverURL, base64ImageArray, ops, namesArray);
    }


    for (let i = 0; i < DOMImages.length; i++) { //cant use iterator 
        if (!DOMImages[i].name) //images which have names are the ones to be upscaled
            continue;
        DOMImages[i].parentNode.parentNode.removeChild(DOMImages[i].parentNode); //lol
        i--; //removed an element so decrement iterator
    }

    return true; //return true cause success
}


/**
* Makes the ajax request to the server
* @function makeRequest
* @param {Array<string>} imageArray - Base 64 array of images
* @param {Array<Object>} operators - Operators to be performed on the images format {"type":"<type of op>", *}
* @param {Array<string>} namesArray - names of the files being uploaded, this is simply for downloading formality
* @returns {string} id of request sent
*/
function makeRequest(serverURL, imageArray, operators, namesArray) {
    const q = {
        "id": uuidv4(), //much secure
        "images": imageArray,
        "ops": operators
    }

    console.log("Sending a request: ");
    console.log(q);
    console.log("---------------");

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
        console.log("Received a response: ");
        console.log(data);
        console.log("---------------");
        downloadResponse(data.images, namesArray);
    }).catch(function (err) {
        // There was an error
        console.warn('Something went wrong.', err);
    });
}

/**
* Downloads the images
* @function makeRequest
* @param {Array<string>} imageArray - Base 64 array of images
* @param {Array<string>} namesArray - names of the files being downloaded, this is simply for downloading formality
*/
function downloadResponse(imageArray, namesArray) {
    for (let i = 0; i < imageArray.length; i++) {
        const a = document.createElement("a");
        a.href = imageArray[i];

        //header tells type of image
        header = imageArray[i].split(",")[0]
        img_type = header.split("/")[1]
        img_type = img_type.split(";")[0]
        if (img_type == "png") {
            a.download = `${namesArray[i]}_upscaled.png`;
        } else {
            a.download = `${namesArray[i]}_upscaled.jpeg`;
        }
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
}

