document.addEventListener("DOMContentLoaded", function () {
    //Bind form submission event
    document.getElementById("calculation_Form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent form default submission behavior
        // Get form data
        const input1 = document.getElementById("input1").value;
        const input2 = document.getElementById("input2").value;
        const input3 = document.getElementById("input3").value;
        const input4 = document.getElementById("input4").value;
        // Build request URL
        const requestURL = `/calculate_sunscreen?input1=${input1}&input2=${input2}&input3=${input3}&input4=${input4}`;

        fetch(requestURL)
            .then(response => response.json())
            .then(data => {
                //Update the results on the page
                document.getElementById("result").textContent = data.result;
            })
            .catch(error => console.error('Error:', error));
    });
});

