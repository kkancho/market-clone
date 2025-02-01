<script>
  import Router from "svelte-spa-router";
  import Login from "./pages/Login.svelte";
  import Main from "./pages/Main.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import "./css/style.css";
  import { user$ } from "./store";
  import {
    getAuth,
    // GoogleAuthProvider,
    // signInWithCredential,
    onAuthStateChanged,
  } from "firebase/auth";
  import { onMount } from "svelte";
  import Loading from "./pages/\bLoading.svelte";
  import MyPage from "./pages/MyPage.svelte";

  let isLoading = true;

  const auth = getAuth();

  // const checkLogin = async () => {
  //   const token = localStorage.getItem("token");
  //   if (!token) return (isLoading = false);
  //   const credential = GoogleAuthProvider.credential(null, token);
  //   const result = await signInWithCredential(auth, credential);
  //   const user = result.user;
  //   user$.set(user);
  //   isLoading = false;
  // };

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "/my": MyPage,
    "*": NotFound,
  };

  // onMount(() => checkLogin());
  // Firebase가 로그인 상태를 자동 복원하도록 onAuthStateChanged 사용
  onMount(() => {
    onAuthStateChanged(auth, (user) => {
      user$.set(user);
      isLoading = false;
    });
  });
</script>

{#if isLoading}
  <Loading />
{:else if !$user$}
  <Login />
{:else}
  <Router {routes} />
{/if}
