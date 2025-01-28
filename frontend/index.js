const calcTime = (timestamp) => {
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const hour = time.getHours();
  const minute = time.getMinutes();
  const second = time.getSeconds();

  if (hour > 0) return `${hour}시간 전`;
  else if (minute > 0) return `${minute}분 전`;
  else if (second > 0) return `${second}초 전`;
  else return "방금 전";
};

const renderData = (data) => {
  const main = document.querySelector("main");

  if (data.length === 0) {
    main.innerHTML = "<p>표시할 데이터가 없습니다.</p>";
    return;
  }

  data.reverse().forEach(async (obj) => {
    const div = document.createElement("div");
    div.className = "items-list";

    const imgDiv = document.createElement("div");
    imgDiv.className = "items-list__img";

    const img = document.createElement("img");
    try {
      const res = await fetch(`/images/${obj.id}`);
      if (res.ok) {
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        img.src = url;
      } else {
        img.src = "assets/no-image.png"; // Fallback image
      }
    } catch {
      img.src = "assets/no-image.png"; // Fallback image
    }

    const InfoDiv = document.createElement("div");
    InfoDiv.className = "items-list__info";

    const InfoTitleDiv = document.createElement("div");
    InfoTitleDiv.className = "items-list__info-title";
    InfoTitleDiv.innerText = obj.title;

    const InfoMetaDiv = document.createElement("div");
    InfoMetaDiv.className = "items-list__info-meta";
    InfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAt);

    const InfoPriceDiv = document.createElement("div");
    InfoPriceDiv.className = "items-list__info-price";
    InfoPriceDiv.innerText = `${obj.price}원`;

    imgDiv.appendChild(img);
    InfoDiv.appendChild(InfoTitleDiv);
    InfoDiv.appendChild(InfoMetaDiv);
    InfoDiv.appendChild(InfoPriceDiv);
    div.appendChild(imgDiv);
    div.appendChild(InfoDiv);
    main.appendChild(div);
  });
};

const fetchList = async () => {
  const accessToken = window.localStorage.getItem("token");
  if (!accessToken) {
    alert("로그인이 필요합니다.");
    window.location.pathname = "/login.html";
    return;
  }

  try {
    const res = await fetch("/items", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    if (!res.ok) {
      alert("로그인이 필요합니다.");
      window.location.pathname = "/login.html";
      return;
    }

    const data = await res.json();
    renderData(data);
  } catch (error) {
    console.error("API 요청 중 오류 발생:", error);
  }
};

fetchList();
