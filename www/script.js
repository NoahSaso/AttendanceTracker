window.addEventListener("load", () => {
  const emailElem = document.getElementById("email");
  const codeElem = document.getElementById("code");

  document.getElementById("submit").addEventListener("click", () =>
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
          alert("Attendance logged.");
        } else {
          console.error(res.error);
          alert(`Something went wrong: ${res.error}.`);
        }
      })
      .catch((err) => {
        console.error(err);
        alert(`Something went wrong: ${err}.`);
      })
  );
});
