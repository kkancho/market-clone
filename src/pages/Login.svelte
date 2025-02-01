<script>
  import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
  import { user$ } from "../store";

  const provider = new GoogleAuthProvider();
  const auth = getAuth();

  const loginWithGoogle = async () => {
    //   try {
    //     const result = await signInWithPopup(auth, provider);
    //     const credential = GoogleAuthProvider.credentialFromResult(result);
    //     const token = credential.accessToken;
    //     const user = result.user;
    //     user$.set(user);
    //     localStorage.setItem("token", token);
    //   } catch (error) {
    //     console.error(error);
    //   }
    try {
      const result = await signInWithPopup(auth, provider);
      // 로그인 성공 시 Firebase가 인증 상태를 유지하므로 추가 토큰 저장이 필요없음
      const user = result.user;
      user$.set(user);
    } catch (error) {
      console.error(error);
    }
  };
</script>

<div>
  <div>로그인하기</div>
  <button class="login-btn" on:click={loginWithGoogle}>
    <img
      class="google-img"
      src="https://cdn4.iconfinder.com/data/icons/logos-brands-7/512/google_logo-google_icongoogle-512.png"
      alt=""
    />
    <div>Google로 로그인하기</div>
  </button>
</div>

<style>
  .login-btn {
    width: 200px;
    height: 50px;
    border: 1px solid gray;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    border-radius: 3px;
  }

  .google-img {
    width: 20px;
  }
</style>
