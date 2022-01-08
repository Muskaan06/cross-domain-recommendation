document.getElementById('generate').onclick = function() {

    var values = ["dog", "cat", "parrot", "rabbit"];

    var select = document.createElement("select");
    select.name = "pets";
    select.id = "pets";


    var label = document.createElement("label");
    label.innerHTML = "Choose your pets: "
    label.htmlFor = "pets";

    document.getElementById("container").appendChild(label).appendChild(select);
}