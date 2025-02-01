<script>
  import Nav from "../\bcomponents/Nav.svelte";
  //   import { user$ } from "../store";
  import { getAuth, signOut } from "firebase/auth";

  const auth = getAuth();

  const logout = async () => {
    // user$.set(null);
    // localStorage.removeItem("token");
    try {
      // Firebase의 signOut을 호출하면 onAuthStateChanged가 실행되어 user$가 null로 업데이트됨
      await signOut(auth);
    } catch (error) {
      console.error(error);
    }
  };
</script>

<div>나의 당근</div>
<button on:click={logout}>로그아웃</button>
<Nav location="my" />

<style>
  button {
    cursor: pointer;
    border: 1px solid rgba(0, 0, 0, 0.3);
  }
</style>
