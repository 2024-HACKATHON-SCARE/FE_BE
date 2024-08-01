let radios = document.querySelectorAll(".sel");

for (let i = 0; i < 2; i++) {
  if (radios[i].checked) {
    let label = document.querySelector(`label[for=${radios[i].id}]`);
    label.style.border = "1px solid #C999F9";
  }
}

radios.forEach((radio) => {
  radio.addEventListener("change", () => {
    radios.forEach((r) => {
      let label = document.querySelector(`label[for=${r.id}]`);
      label.style.border = "1px solid black";
    });

    if (radio.checked) {
      let checkedLabel = document.querySelector(`label[for=${radio.id}]`);
      checkedLabel.style.border = "1px solid #C999F9";
    }
  });
});

let samePW1 = document.getElementById("id_password1");
let samePW2 = document.getElementById("id_password2");
let errorMessage = document.getElementById("pwError");

samePW2.addEventListener("change", (e) => {
  if (samePW1.value !== samePW2.value) {
    errorMessage.style.display = "flex";
    samePW2.style.border = "1px solid #d91818";
    samePW2.style.backgroundColor = "rgba(217, 24, 24, 0.11)";
  } else {
    errorMessage.style.display = "none";
    samePW2.style.border = "1px solid black";
    samePW2.style.backgroundColor = "";
  }
});
