const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  const password = formData.get("password");

  // 비밀번호를 해시로 변환
  const hashedPassword = sha256(password);
  formData.set("password", hashedPassword);

  const res = await fetch("/login", {
    method: "POST",
    body: formData,
  });

  const data = await res.json();
  const accessToken = data.access_token;
  window.localStorage.setItem("token", accessToken);
  alert("로그인되었습니다!!");

  window.location.pathname = "/";
};

form.addEventListener("submit", handleSubmit);
