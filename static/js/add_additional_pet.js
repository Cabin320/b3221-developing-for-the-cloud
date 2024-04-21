const dogOwnerCheckbox = document.getElementById("dogOwnerCheckbox");
const dogWalkerCheckbox = document.getElementById("dogWalkerCheckbox");
const dogInputs = document.getElementById("dog-inputs");
const additionalPetButtons = document.getElementById("additional-pet-buttons");

dogOwnerCheckbox.addEventListener("change", function () {
    if (this.checked) {
        dogWalkerCheckbox.checked = false;
    }
    dogInputs.style.display = this.checked ? "block" : "none";
    additionalPetButtons.style.display = this.checked ? "flex" : "none";
    if (!this.checked) {
        clearAdditionalDogs();
    }
});

dogWalkerCheckbox.addEventListener("change", function () {
    if (this.checked) {
        dogOwnerCheckbox.checked = false;
        dogInputs.style.display = "none";
        additionalPetButtons.style.display = "none";
        clearAdditionalDogs();
    }
});

document.getElementById("add-dog").addEventListener("click", function () {
    const newInput = document.createElement("div");
    newInput.innerHTML = `
<div class="form-group" style="display: flex; align-items: center;">
  <input type="text" class="form-control dog-input" name="name" placeholder="Pet name" 
         style="flex: 1; margin-right: 5px;" required>
  <input type="text" class="form-control dog-input" name="breed" placeholder="Breed" 
         style="flex: 1; margin-right: 5px;" required>
  <input type="number" class="form-control dog-input" name="age" placeholder="Age" 
         style="flex: 1; margin-right: 5px;" min="0" max="40" required>
  <button type="button" class="btn btn-danger delete-dog">Delete</button>
</div>
`;
    dogInputs.appendChild(newInput);
});

document.getElementById("dog-form").addEventListener("click", function (event) {
    if (event.target.classList.contains("delete-dog")) {
        event.target.parentElement.remove();
    }
});

document.getElementById("clear-all").addEventListener("click", function () {
    clearAdditionalDogs();
});

function clearAdditionalDogs() {
    while (dogInputs.children.length > 1) {
        dogInputs.removeChild(dogInputs.lastChild);
    }
}