window.addEventListener("load", () => {
  const alertElem = document.getElementById("alert");

  const emailElem = document.getElementById("email");
  const codeElem = document.getElementById("code");
  const submitElem = document.getElementById("submit");

  const setAlert = (text, isError) => {
    if (!text) {
      alertElem.className = "";
      return;
    }

    alertElem.innerText = text;
    alertElem.classList.toggle("success", !isError);
    alertElem.classList.toggle("error", isError);
    alertElem.classList.add("show");
  };

  submitElem.addEventListener("click", () => {
    if (!emailElem.value || !codeElem.value) {
      return setAlert("Please fill in all fields.", true);
    }

    submitElem.innerText = "Submitting...";
    submitElem.disabled = true;
    setAlert(null);

    fetch("/decal-attendance/track", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        email: emailElem.value,
        code: codeElem.value,
      }),
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.success) {
          setAlert("Attendance logged.", false);
        } else {
          console.error(res.error);
          setAlert(res.error, true);
        }
      })
      .catch((err) => {
        console.error(err);
        setAlert(`An error occurred: ${err}`, true);
      })
      .finally(() => {
        submitElem.innerText = "Submit";
        submitElem.disabled = false;
      });
  });
});
