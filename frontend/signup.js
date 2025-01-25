const form = document.querySelector("#signup-form");

const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");

  if (password1 === password2) {
    return true;
  } else return false;
};

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const password = formData.get("password");

  // 비밀번호를 해시로 변환
  const hashedPassword = sha256(password);
  formData.set("password", hashedPassword);

  const div = document.querySelector("#info");

  if (checkPassword()) {
    try {
      const res = await fetch("/signup", {
        method: "POST",
        body: formData,
      });

      // 응답 데이터 확인
      if (res.ok) {
        alert("회원 가입에 성공했습니다.");
        window.location.pathname = "/login.html";
      } else {
        const data = await res.json();
        div.innerText = data.message || "회원 가입 중 오류가 발생했습니다.";
        div.style.color = "red";
      }
    } catch (error) {
      div.innerText = "서버와 통신 중 문제가 발생했습니다.";
      div.style.color = "red";
      console.error(error);
    }
  } else {
    div.innerText = "비밀번호가 같지 않습니다.";
    div.style.color = "red";
  }
};

form.addEventListener("submit", handleSubmit);
