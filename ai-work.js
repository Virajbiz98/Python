function calculateBMI() {
    const height = parseFloat(document.getElementById("height").value);
    const weight = parseFloat(document.getElementById("weight").value);
  
    if (isNaN(height) || isNaN(weight)) {
      document.getElementById("result").textContent = "Please enter valid values for height and weight.";
    } else {
      const bmi = weight / ((height / 100) ** 2);
      document.getElementById("result").textContent = "Your BMI is: " + bmi.toFixed(2);
    }
  }
  
  function reset() {
    document.getElementById("height").value = "";
    document.getElementById("weight").value = "";
    document.getElementById("result").textContent = "";
  }
