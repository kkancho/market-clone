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

  console.log("액세스토큰!!", data);
  if (res.status === 200) {
    alert("로그인에 성공했습니다!!");
    window.location.pathname = "/";
  } else if (res.status === 401) {
    alert("id 혹은 password가 틀렸습니다.");
  }
};

form.addEventListener("submit", handleSubmit);
