<script>
  let hour = new Date().getHours();
  let min = new Date().getMinutes();
</script>

<header>
  <div class="info-bar">
    <div class="info-bar__time">{hour}:{min}</div>
    <div class="info-bar__icons">
      <img src="assets/chart-bar.svg" alt="chart-bar" />
      <img src="assets/wifi.svg" alt="wifi" />
      <img src="assets/battery.svg" alt="battery" />
    </div>
  </div>
  <div class="menu-bar">
    <div class="menu-bar__location">
      <div>역삼1동</div>
      <div class="menu-bar_location-icon">
        <img src="assets/arrow-down.svg" alt="arrow-down" />
      </div>
    </div>
    <div class="menu-bar__icons">
      <img src="assets/search.svg" alt="search" />
      <img src="assets/menu.svg" alt="menu" />
      <img src="assets/alert.svg" alt="alert" />
    </div>
  </div>
</header>

<main>
  <a class="write-btn" href="#/write">+ 글쓰기</a>
</main>

<footer>
  <div class="footer-block">
    <div class="footer-icons">
      <img src="assets/home.svg" alt="home" />
      <div>홈</div>
    </div>
    <div class="footer-icons">
      <img src="assets/doc.svg" alt="doc" />
      <div>동네생활</div>
    </div>
    <div class="footer-icons">
      <img src="assets/location.svg" alt="location" />
      <div>내 근처</div>
    </div>
    <div class="footer-icons">
      <img src="assets/chat.svg" alt="chat" />
      <div>채팅</div>
    </div>
    <div class="footer-icons">
      <img src="assets/user.svg" alt="user" />
      <div>나의 당근</div>
    </div>
  </div>
</footer>

<div class="media-info-msg">화면 사이즈를 줄여주세요.</div>

<style>
  @import "../css/reset.css";
  @import "../css/header.css";
  @import "../css/footer.css";
  @import "../css/main.css";

  :root {
    --button-primary: rgb(254, 111, 15);
    --button-hover: rgba(254, 111, 15, 0.8);
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo",
      "Pretendard Variable", Pretendard, Roboto, "Noto Sans KR", "Segoe UI",
      "Malgun Gothic", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol",
      sans-serif;
  }

  .media-info-msg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: salmon;
  }

  @media screen and (max-width: 500px) {
    .media-info-msg {
      display: none;
    }
  }
</style>
