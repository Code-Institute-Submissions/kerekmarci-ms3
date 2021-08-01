// Recipe upload page
const ingredientInputContainer = document.getElementById("ingredientInputContainer");
const ingredientsInput = document.getElementsByName("ingredients");
const methodInputContainer = document.getElementById("methodInputContainer");
const methodInput = document.getElementsByName("method");
const receipeName = document.getElementById("recipename");

// Adding and removing fields on Upload Receipe page
function addField(container, inputName) {
    event.preventDefault();
    let input = document.createElement("input");
    input.type = "text";
    input.name = inputName;
    input.className = "form-control mt-3";
    input.required = true;
    container.appendChild(input);
}

function removeField(container) {
    event.preventDefault();
    container.removeChild(container.lastChild);
}

// Maximum number of characters on Upload Receipe page
function maxInput(formId, maxChar, outputName) {
    let name = document.getElementById(formId).value;
    let remainingChar = maxChar-name.length;
    if (remainingChar < 6) {
        document.getElementById(outputName).innerHTML = remainingChar + " characters left.";
        remainingChar == 0 ? document.getElementById(outputName).style.color = "#DC3545" : document.getElementById(outputName).style.color = "#212529";
    } else {
        document.getElementById(outputName).innerHTML = "";
    }
}

// Form validation on Registration page
// Help found here: https://stackoverflow.com/questions/47088833/javascript-form-validation-check-for-all-letters-only

function validateForm(pattern, input, output, errorMsg) {
    let regex = new RegExp(pattern);
    let x = document.getElementById(input).value;
    let message = document.getElementById(output);
    if (x == null || x == "") {
        message.innerHTML = "";
        return false;
    } else if (!regex.test(x)) {
        message.innerHTML = errorMsg;
        return false;
    } else {
        message.innerHTML = "";
        return true;
    }
}