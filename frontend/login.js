const form = document.querySelector("#login-form");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);

  try {
    const res = await fetch("/login", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      alert("로그인에 실패했습니다. 아이디와 비밀번호를 확인하세요.");
      return;
    }

    const data = await res.json();
    const accessToken = data.access_token;

    localStorage.setItem("token", accessToken);
    alert("로그인되었습니다.");
    window.location.pathname = "/";
  } catch (error) {
    console.error("로그인 중 오류 발생:", error);
    alert("서버와 통신 중 오류가 발생했습니다.");
  }
};

form.addEventListener("submit", handleSubmit);
